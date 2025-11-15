from functools import lru_cache
from typing import Any

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict 


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(..., description="Service name")
    app_version: str = Field(..., description="Service semantic version")
    api_prefix: str = Field(..., description="Base prefix for all API routes")
    host: str | None = Field(default=None, description="Host interface for the ASGI server")
    port: int | None = Field(default=None, description="Port for the ASGI server")
    reload: bool | None = Field(default=None, description="Enable auto-reload in development")

    @model_validator(mode="before")
    @classmethod
    def apply_env_aliases(cls, data: Any) -> Any:

        if isinstance(data, dict):
            alias_map = {
                "app_name": ("APP_NAME",),
                "app_version": ("APP_VERSION",),
                "api_prefix": ("API_PREFIX",),
                "host": ("APP_HOST", "HOST"),
                "port": ("APP_PORT", "PORT"),
                "reload": ("APP_RELOAD", "RELOAD"),
            }
            for field, aliases in alias_map.items():
                if field in data and data[field] is not None:
                    continue
                for alias in aliases:
                    if alias in data and data[alias] is not None:
                        data[field] = data.pop(alias)
                        break
        return data


@lru_cache(maxsize=1)
def get_settings() -> Settings:

    return Settings()

