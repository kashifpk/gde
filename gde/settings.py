from functools import lru_cache

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from . import PROJECT_ROOT


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / ".env", env_file_encoding="utf-8", extra='allow')

    app_name: str = "GDE"
    environment: str = Field(..., env="ENVIRONMENT")
    # base_url: str = Field(..., env="WEBSITE_BASE_URL")

    debug: bool = False

    @validator("debug", pre=True)
    def determine_debug_mode(cls, v: bool | None, values: dict) -> bool:
        if isinstance(v, bool):
            return v

        if values["environment"] == "development":
            return True

        return False


@lru_cache
def get_settings():
    return Settings()
