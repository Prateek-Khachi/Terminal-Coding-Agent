from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    model: str = "gpt-4o-mini"
    openai_api_key: str | None = None
    workspace: str = "."
    max_iterations: int = 20
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )