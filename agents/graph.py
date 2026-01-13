from langgraph.graph import StateGraph, END
from agents.llm import openrouter_chat

def build_graph():
    def analyst(s): 
        s["final"] = openrouter_chat("meta-llama/llama-3.1-8b-instruct:free", [{"role":"user","content":s["user_question"]}])
        return s

    g = StateGraph(dict)
    g.add_node("analyst", analyst)
    g.set_entry_point("analyst")
    g.add_edge("analyst", END)
    return g.compile()
