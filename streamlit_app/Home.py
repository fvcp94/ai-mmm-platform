import os
import sys
from pathlib import Path
import streamlit as st

# Ensure repo root is on path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

st.set_page_config(page_title="AI MMM Platform", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
    .tile {
        border: 1px solid rgba(49,51,63,.2);
        border-radius: 16px;
        padding: 18px;
        background: rgba(255,255,255,.02);
        height: 180px;
    }
    .tile h3 { margin-top: 0px; }
    .muted { color: rgba(250,250,250,.65); }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📊 AI-Powered Marketing Mix Modeling Platform")
st.caption("Multi-agent MMM + Causal + RAG (Free OpenRouter models)")

api_key = st.secrets.get("OPENROUTER_API_KEY", os.environ.get("OPENROUTER_API_KEY", ""))
c1, c2, c3 = st.columns(3)
c1.metric("OpenRouter API Key", "✅ Set" if api_key else "⚠️ Missing")
c2.metric("Mode", "Cloud" if os.environ.get("STREAMLIT_SERVER_HEADLESS") else "Local")
c3.metric("Version", "v0.1 Demo")

st.divider()

st.subheader("Start Here")
st.write("Pick a module below. If you don’t have data, use **Demo Mode** in MMM Dashboard.")

colA, colB, colC = st.columns(3)

with colA:
    st.markdown(
        """
        <div class="tile">
        <h3>💬 Chat Assistant</h3>
        <p class="muted">Ask questions, get insights, and generate recommendations (agent workflow).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Chat_Assistant.py", label="Open Chat Assistant →", icon="💬")

with colB:
    st.markdown(
        """
        <div class="tile">
        <h3>📈 MMM Dashboard</h3>
        <p class="muted">Upload CSV → ROI by channel, contribution charts, diagnostics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_MMM_Dashboard.py", label="Open MMM Dashboard →", icon="📈")

with colC:
    st.markdown(
        """
        <div class="tile">
        <h3>🧪 Experiment Designer</h3>
        <p class="muted">A/B & Geo-test sample size, MDE, power, and timeline plan.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/3_Experiment_Designer.py", label="Open Experiment Designer →", icon="🧪")

st.divider()

with st.expander("✅ Recommended CSV Format"):
    st.code(
        """date,revenue,tv_spend,search_spend,social_spend
2024-01-01,120000,5000,3000,1500
2024-01-08,125000,5200,3100,1400
...""",
        language="text",
    )
