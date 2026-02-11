import sys
from pathlib import Path

# ---------------------------------------
# Add repo root to PYTHONPATH (Cloud fix)
# ---------------------------------------
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ---------------------------------------
# Imports
# ---------------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from analytics.mmm import (
    detect_columns,
    prepare_mmm_design,
    fit_mmm_ols,
    channel_contributions,
    roi_by_channel,
)

# ---------------------------------------
# Page config
# ---------------------------------------
st.set_page_config(page_title="MMM Dashboard", page_icon="📈", layout="wide")

st.title("📈 Marketing Mix Modeling Dashboard")
st.caption("Upload marketing data → Estimate ROI & channel contributions")

# ---------------------------------------
# Sidebar
# ---------------------------------------
with st.sidebar:
    st.header("Data Controls")

    demo_mode = st.toggle("Demo Mode", value=True)

    uploaded = None
    if not demo_mode:
        uploaded = st.file_uploader("Upload CSV", type=["csv"])

    st.divider()

    st.header("Model Controls")

    adstock_alpha = st.slider("Adstock Alpha", 0.0, 0.95, 0.50, 0.05)
    use_saturation = st.checkbox("Use saturation", value=True)

# ---------------------------------------
# Demo dataset
# ---------------------------------------
def load_demo_df():
    rng = np.random.default_rng(7)
    dates = pd.date_range("2024-01-01", periods=52, freq="W")

    tv = rng.normal(6000, 1200, len(dates)).clip(500)
    search = rng.normal(3500, 700, len(dates)).clip(300)
    social = rng.normal(1800, 500, len(dates)).clip(200)

    base = 90000 + 4000 * np.sin(np.linspace(0, 2 * np.pi, len(dates)))
    revenue = base + 3.2 * tv + 5.1 * search + 2.0 * social + rng.normal(0, 6000, len(dates))

    return pd.DataFrame(
        {
            "date": dates,
            "revenue": revenue,
            "tv_spend": tv,
            "search_spend": search,
            "social_spend": social,
        }
    )

# ---------------------------------------
# Load data
# ---------------------------------------
if demo_mode:
    df = load_demo_df()
else:
    if uploaded is None:
        st.info("Upload a CSV or enable Demo Mode.")
        st.stop()

    df = pd.read_csv(uploaded)

# ---------------------------------------
# Preview
# ---------------------------------------
st.subheader("📄 Data Preview")
st.dataframe(df.head(15), use_container_width=True)

date_col, target_col, spend_cols = detect_columns(df)

st.write(
    {
        "Date Column": date_col,
        "Target Column": target_col,
        "Spend Columns": spend_cols,
    }
)

if not target_col or not spend_cols:
    st.error("Could not detect required columns.")
    st.stop()

# ---------------------------------------
# Model
# ---------------------------------------
X, y, meta = prepare_mmm_design(
    df=df,
    date_col=date_col,
    target_col=target_col,
    spend_cols=spend_cols,
    adstock_alpha=adstock_alpha,
    use_saturation=use_saturation,
)

res = fit_mmm_ols(X, y)
contrib = channel_contributions(X, res.params)
roi = roi_by_channel(df.loc[X.index], contrib, spend_cols)

# ---------------------------------------
# KPI Cards
# ---------------------------------------
st.subheader("📊 Model Summary")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", int(res.nobs))
c2.metric("R²", f"{res.rsquared:.3f}")
c3.metric("Adj R²", f"{res.rsquared_adj:.3f}")
c4.metric("Channels", len(spend_cols))

# ---------------------------------------
# Tabs
# ---------------------------------------
tab1, tab2 = st.tabs(["ROI", "Contributions"])

with tab1:
    st.subheader("💰 ROI by Channel")
    st.dataframe(roi, use_container_width=True)

    fig = px.bar(roi, x="channel", y="roi", title="ROI by Channel")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("📊 Channel Contributions")

    totals = contrib.sum().reset_index()
    totals.columns = ["feature", "contribution"]

    fig = px.bar(totals, x="feature", y="contribution")
    st.plotly_chart(fig, use_container_width=True)
