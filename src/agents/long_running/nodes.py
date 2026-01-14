from langchain_core.messages.utils import count_tokens_approximately
from langmem.short_term import SummarizationNode

from agents.long_running.state import LLMInputState
from src.agents.long_running.config import summarization_model, model

summarization_node = SummarizationNode(
    token_counter=count_tokens_approximately,
    model=summarization_model,
    max_tokens=256,
    max_tokens_before_summary=256,
    max_summary_tokens=128,
)


def call_model(state: LLMInputState):
    response = model.invoke(state["summarized_messages"])
    return {"messages": [response]}
