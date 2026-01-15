from textwrap import dedent

from langchain_core.messages import SystemMessage

from app.agents.copilot.config import model
from app.agents.copilot.schemas import UIAction, UIActionList
from app.agents.copilot.state import CopilotState


def call_model(state: CopilotState) -> dict:
    SYSTEM_PROMPT = dedent(f"""
        You are an AI copilot that helps users interact with a web application's UI.
        You will be provided with a description of the user's intent and the current state of the UI.
        Based on this information, determine the appropriate action to take in the UI.

        Respond with a message followed by the UIActionList JSON in a XML tag as shown below:

        ---
        Some message to the user.
        <ui-action-list>
        {UIActionList(ui_actions=[UIAction(field_name="name_of_field", new_value="new_value", reason="explanation")]).model_dump_json()}
        </ui-action-list>
        ---

        UIActionList JSON Schema:
        {UIActionList.model_json_schema()}
    """)

    response = model.invoke([SystemMessage(content=SYSTEM_PROMPT)] + state["messages"])
    return {"messages": response}
