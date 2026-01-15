from typing import TypedDict

from langchain.messages import AnyMessage
from langgraph.graph import MessagesState
from langmem.short_term import RunningSummary


class State(MessagesState):
    context: dict[str, RunningSummary]


class LLMInputState(TypedDict):
    summarized_messages: list[AnyMessage]
    context: dict[str, RunningSummary]
