import sys
from pathlib import Path

# ---------------------------------------
# Add repo root to PYTHONPATH
# ---------------------------------------
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ---------------------------------------
# Imports
# ---------------------------------------
import streamlit as st
import pandas as pd

from analytics.experiments import (
    ab_test_sample_size_per_group,
    geo_test_mde,
)

# ---------------------------------------
# Page config
# ---------------------------------------
st.set_page_config(page_title="Experiment Designer", page_icon="🧪", layout="wide")

st.title("🧪 Causal Experiment Designer")
st.caption("Design A/B tests and Geo experiments")

tab1, tab2 = st.tabs(["A/B Test", "Geo Test"])

# ============================================================
# A/B TEST
# ============================================================
with tab1:

    st.subheader("A/B Test Sample Size")

    c1, c2, c3, c4 = st.columns(4)

    baseline = c1.number_input("Baseline Rate", value=0.05)
    mde_pct = c2.slider("MDE %", 1.0, 50.0, 10.0)
    alpha = c3.selectbox("Alpha", [0.1, 0.05, 0.01], index=1)
    power = c4.selectbox("Power", [0.7, 0.8, 0.9], index=1)

    n = ab_test_sample_size_per_group(
        baseline=baseline,
        mde_pct=mde_pct,
        alpha=alpha,
        power=power,
    )

    st.success(f"Required sample size ≈ {n:,} per group")

# ============================================================
# GEO TEST
# ============================================================
with tab2:

    st.subheader("Geo Test MDE")

    c1, c2, c3 = st.columns(3)

    baseline_geo = c1.number_input("Weekly KPI per Geo", value=100000.0)
    weeks = c2.slider("Weeks", 1, 12, 4)
    geos = c3.slider("Geos per Arm", 5, 200, 20)

    result = geo_test_mde(
        baseline=baseline_geo,
        weeks=weeks,
        n_geos_per_arm=geos,
    )

    st.success(
        f"MDE ≈ ${result.mde_abs:,.0f} "
        f"({result.mde_pct:.2f}%)"
    )

    st.info(result.notes)
