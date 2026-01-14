from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-5-mini")
summarization_model = init_chat_model("openai:gpt-5-nano")
