import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    LANGSMITH_TRACING: str
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str

    OPENAI_API_KEY: str

    TAVILY_API_KEY: str


settings = Settings.model_validate({})

for key, value in settings.model_dump().items():
    if value is not None:
        print(f"Setting env var {key}")
        os.environ[key] = value
