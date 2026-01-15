from pydantic import BaseModel, Field


class UIAction(BaseModel):
    field_name: str = Field(..., description="The field to be updated in the UI")
    new_value: str = Field(..., description="The new value to set for the field")
    reason: str = Field(..., description="The reason for this UI action")


class UIActionList(BaseModel):
    ui_actions: list[UIAction]
