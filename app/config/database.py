from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


async def get_checkpointer():
    async with AsyncSqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
        yield checkpointer
