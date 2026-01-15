import json
from textwrap import dedent
from typing import Annotated, AsyncGenerator
from uuid import uuid4

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessageChunk

from app.agents.copilot.agent import builder
from app.config.database import get_checkpointer


Checkpointer = Annotated[AsyncSqliteSaver, Depends(get_checkpointer)]

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    fields: list[dict] = []
    thread_id: str | None = None


async def event_generator(body: ChatRequest, checkpointer: AsyncSqliteSaver) -> AsyncGenerator[str, None]:
    graph = builder.compile(name="copilot_agent", checkpointer=checkpointer)

    USER_PROMPT = dedent(f"""
        {body.message}

        Actual state of the UI:
        {json.dumps(body.fields)}
    """)

    async for token, metadata in graph.astream(
        {"messages": [HumanMessage(content=USER_PROMPT)]},
        config={
            "configurable": {
                "thread_id": body.thread_id if body.thread_id else uuid4().hex
            }
        },
        stream_mode="messages",
    ):
        if isinstance(token, AIMessageChunk):
            content_safe = token.text.replace("\n", "\\n")
            yield f"TYPE:TEXT|{content_safe}\n"


@router.post("/")
async def chat_endpoint(
    request: Request, body: ChatRequest, checkpointer: Checkpointer
):
    return StreamingResponse(
        event_generator(body, checkpointer),
        media_type="text/event-stream",
    )
