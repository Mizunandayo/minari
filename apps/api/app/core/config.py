"""Application Configuration
All secrets are typed as ``SecretStr`` to prevent appearing in logs."""



from __future__ import annotations
from functools import lru_cache
from typing import Annotated, Literal
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict




class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MINARI_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )



    # APP
    env: Literal["development", "production", "test"] = "development"
    demo_api_key: SecretStr

    # CORS — NoDecode skips pydantic-settings' JSON decoding so a plain
    # comma-separated env value (e.g. "http://localhost:3000,https://app.vercel.app")
    # is passed raw to the _split_origins validator below.
    cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:3000"]
    )

    # DATASTORES
    database_url: SecretStr
    redis_url: SecretStr

    # GITLAB MCP
    gitlab_mcp_url: str
    gitlab_token: SecretStr
    demo_project_id: str
    demo_test_file: str = "tests/test_checkout_flow.py"

    # LLM 
    gemini_api_key: SecretStr | None = None
    deepseek_api_key: SecretStr | None = None

    # OBSERVABILITY
    langfuse_public_key: SecretStr | None = None
    langfuse_secret_key: SecretStr | None = None
    langfuse_host: str = "https://cloud.langfuse.com"




    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: object) -> object:
        if isinstance(value, str):
            origins = [o.strip() for o in value.split(",") if o.strip()]
        else:
            origins = value 
        if isinstance(origins, list) and "*" in origins:
            raise ValueError("Wildcard CORS origin is forbidden — list exact origins.")
        return origins

    @property
    def is_production(self) -> bool:
        return self.env == "production"
    

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached singleton"""
    return Settings() 


