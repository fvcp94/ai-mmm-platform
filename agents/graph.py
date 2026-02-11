from __future__ import annotations

import os
from typing import Dict, Any

import streamlit as st

# NOTE:
# We keep this minimal so it runs on Streamlit Cloud.
# If OPENROUTER_API_KEY is not set, it falls back to a local "mock" answer.


def _call_openrouter(prompt: str) -> str:
    """
    Minimal OpenRouter chat call (no external SDK).
    Uses requests (already common in Streamlit env).
    """
    import requests

    api_key = None
    try:
        api_key = st.secrets.get("OPENROUTER_API_KEY")
    except Exception:
        api_key = None

    api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")

    if not api_key:
        return (
            "⚠️ OPENROUTER_API_KEY not set.\n\n"
            "Mock answer:\n"
            f"- You asked: {prompt}\n"
            "- Add your key in Streamlit Cloud → Settings → Secrets\n"
        )

    # Choose a free model you like. (You can change this later.)
    model = os.environ.get("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # Optional headers (nice to have; safe if blank):
        "HTTP-Referer": os.environ.get("OPENROUTER_SITE_URL", ""),
        "X-Title": os.environ.get("OPENROUTER_APP_NAME", "ai-mmm-platform"),
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful marketing analytics assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()

    return data["choices"][0]["message"]["content"]


def build_graph():
    """
    Returns a simple object with invoke() so the Streamlit page can call it.

    We keep 'graph' lightweight (no heavy LangGraph dependencies required),
    while preserving your "agentic workflow" idea.
    """

    class SimpleGraph:
        def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
            question = (state or {}).get("question", "").strip()

            if not question:
                return {"answer": "Ask a question to start."}

            # "Multi-agent" style: 3-step chain
            analyst_prompt = f"""
You are Agent 1 (Data Analyst). Provide a concise analysis plan and what data you'd need.
Question: {question}
Return 3 bullets.
"""
            analyst = _call_openrouter(analyst_prompt)

            strategist_prompt = f"""
You are Agent 4 (Business Strategist). Turn the analysis into actionable recommendations.
Question: {question}

Context from Analyst:
{analyst}

Return:
- 3 executive bullets
- 3 recommended actions
"""
            strategist = _call_openrouter(strategist_prompt)

            return {
                "answer": strategist,
                "analyst_notes": analyst,
            }

    return SimpleGraph()
