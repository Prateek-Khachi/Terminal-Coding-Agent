from functools import lru_cache

from coding_agent.config.settings import Settings


@lru_cache
def get_settings() -> Settings:
    """Return the application settings."""
    return Settings()