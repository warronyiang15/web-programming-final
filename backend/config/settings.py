from functools import lru_cache
from typing import Any

from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore[import-untyped]


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="Backend Service", description="Service name")
    app_version: str = Field(default="0.1.0", description="Service semantic version")
    api_prefix: str = Field(default="/api/v1", description="Base prefix for all API routes")
    host: str | None = Field(default="0.0.0.0", description="Host interface for the ASGI server")
    port: int | None = Field(default=8080, description="Port for the ASGI server")
    reload: bool | None = Field(default=False, description="Enable auto-reload in development")
    firebase_project_id: str | None = Field(
        default=None,
        description="Explicit Firestore project id. Defaults to credentials project.",
        validation_alias=AliasChoices("FIREBASE_PROJECT_ID", "GOOGLE_CLOUD_PROJECT"),
    )
    firebase_credentials_file: str | None = Field(
        default=None,
        description="Path to a service-account JSON for Firestore access.",
        validation_alias=AliasChoices("FIREBASE_CREDENTIALS_FILE", "GOOGLE_APPLICATION_CREDENTIALS"),
    )
    firestore_health_collection: str = Field(
        default="health_checks",
        description="Collection used for Firestore connectivity checks.",
    )
    llm_api_key: str = Field(
        default="dev-dummy-key",
        description="Secret key for authenticating LLM callbacks.",
        validation_alias=AliasChoices("LLM_API_KEY"),
    )

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
                "firestore_health_collection": ("FIRESTORE_HEALTH_COLLECTION",),
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
