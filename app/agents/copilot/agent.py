from langgraph.graph import StateGraph, START, END

from app.agents.copilot.nodes import call_model
from app.agents.copilot.state import CopilotState


builder = StateGraph(CopilotState)

builder.add_node(call_model)

builder.add_edge(START, "call_model")
builder.add_edge("call_model", END)
