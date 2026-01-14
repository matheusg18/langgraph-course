from langgraph.graph import StateGraph, START, END

from agents.long_running.nodes import call_model, summarization_node
from agents.long_running.state import State


builder = StateGraph(State)

builder.add_node(call_model)
builder.add_node("summarize", summarization_node)

builder.add_edge(START, "summarize")
builder.add_edge("summarize", "call_model")
builder.add_edge("call_model", END)

graph = builder.compile()
