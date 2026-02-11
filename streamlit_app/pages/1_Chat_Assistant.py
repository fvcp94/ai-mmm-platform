import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from agents.graph import build_graph

st.set_page_config(page_title="Chat Assistant", page_icon="💬", layout="wide")

st.title("💬 Chat Assistant")
st.caption("Lightweight multi-agent workflow (OpenRouter). Works even if API key is missing (mock mode).")

graph = build_graph()

q = st.text_area("Ask a question", value="Summarize what this MMM app does and what I should do next.")
run = st.button("Run")

if run:
    with st.spinner("Thinking..."):
        out = graph.invoke({"question": q})

    st.subheader("Answer")
    st.write(out.get("answer", ""))

    with st.expander("Analyst notes"):
        st.write(out.get("analyst_notes", ""))
