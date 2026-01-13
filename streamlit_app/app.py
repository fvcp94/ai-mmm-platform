import os
import sys
from pathlib import Path

import streamlit as st

# --- Ensure repo root is on PYTHONPATH (Streamlit Cloud runs from streamlit_app/) ---
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

st.set_page_config(
    page_title="AI MMM Platform",
    page_icon="📊",
    layout="wide",
)

st.title("📊 AI-Powered Marketing Mix Modeling Platform")
st.caption("Multi-agent MMM + Causal + RAG (Free OpenRouter models)")

# Quick health checks
api_key = st.secrets.get("OPENROUTER_API_KEY", os.environ.get("OPENROUTER_API_KEY", ""))
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("OpenRouter API Key", "✅ Set" if api_key else "⚠️ Missing")
with col2:
    st.metric("Environment", "Streamlit Cloud" if os.environ.get("STREAMLIT_SERVER_HEADLESS") else "Local")
with col3:
    st.metric("Repo Root in Path", "✅ Yes" if str(REPO_ROOT) in sys.path else "❌ No")

st.markdown(
    """
### What to do next
Use the left sidebar to open:

- **Chat Assistant** (agentic workflow)
- **MMM Dashboard** (upload CSV → ROI + contributions)
- **Causal Experiment Designer** (A/B + geo-test power/MDE)

### If you don't see pages
Make sure the repo has:
- `streamlit_app/pages/1_Chat_Assistant.py`
- `streamlit_app/pages/2_MMM_Dashboard.py`
- `streamlit_app/pages/3_Experiment_Designer.py`
"""
)

with st.expander("Troubleshooting", expanded=not api_key):
    st.write("**ModuleNotFoundError: No module named 'agents'** is fixed by adding repo root to PYTHONPATH and adding `agents/__init__.py`.")
    st.write("If the API key is missing, go to Streamlit Cloud → App → Settings → Secrets and add:")
    st.code('OPENROUTER_API_KEY="your_key_here"', language="toml")
