from functools import lru_cache

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from . import PROJECT_ROOT


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / ".env", env_file_encoding="utf-8", extra='allow')

    app_name: str = "GDE"
    environment: str = Field(..., env="ENVIRONMENT")
    website_base_url: str = Field(..., env="WEBSITE_BASE_URL")
    dev_js_server: str = Field("", env="DEV_JS_SERVER")
    static_url: str = Field(..., env="STATIC_URL")

    db_hosts: str = Field(..., env="DB_HOSTS")
    db_username: str = Field(..., env="DB_USERNAME")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_name: str = Field(..., env="DB_NAME")

    debug: bool = False

    @validator("debug", pre=True)
    def determine_debug_mode(cls, v: bool | None, values: dict) -> bool:
        if isinstance(v, bool):
            return v

        if values["environment"] == "development":
            return True

        return False


@lru_cache
def get_settings() -> Settings:
    return Settings()
