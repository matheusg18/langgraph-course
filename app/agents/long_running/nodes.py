from langchain_core.messages.utils import count_tokens_approximately
from langmem.short_term import SummarizationNode
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage

from app.agents.long_running.state import LLMInputState, State
from app.agents.long_running.config import summarization_model, model

summarization_node = SummarizationNode(
    token_counter=count_tokens_approximately,
    model=summarization_model,
    max_tokens=256,
    max_tokens_before_summary=256,
    max_summary_tokens=128,
)


@tool
def search_brazilian_state_capital(state: str) -> str:
    """Search for the capital of a Brazilian state given the state name.

    Args:
        state (str): The name of the Brazilian state.

    Returns:
        str: The capital city of the given Brazilian state.
    """
    return "teste capital for " + state


def call_model(state: LLMInputState) -> dict:
    system_message = SystemMessage(
        content="You are an expert in geography. If asked about Brazilian states, use the tool to find their capitals also responde some text in Portuguese."
    )
    response = model.bind_tools([search_brazilian_state_capital]).invoke(
        [system_message] + state["summarized_messages"]
    )
    return {"messages": response}
