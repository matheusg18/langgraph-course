import sqlite3
from langgraph.graph import StateGraph, START, END

from agents.long_running.nodes import call_model, summarization_node
from agents.long_running.state import State
from langgraph.checkpoint.sqlite import SqliteSaver


builder = StateGraph(State)

builder.add_node(call_model)
builder.add_node("summarize", summarization_node)

builder.add_edge(START, "summarize")
builder.add_edge("summarize", "call_model")
builder.add_edge("call_model", END)

conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)
graph = builder.compile(checkpointer=memory)
