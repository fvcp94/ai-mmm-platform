import streamlit as st
from agents.graph import build_graph

st.title("💬 AI Chat Assistant")
graph = build_graph()

q = st.text_area("Ask a marketing analytics question")
if st.button("Run") and q:
    result = graph.invoke({"user_question": q})
    st.write(result["final"])
