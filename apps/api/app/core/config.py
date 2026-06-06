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

    # CORS
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
    gemini_use_vertex: bool = False
    gcp_project: str | None = None
    gcp_location: str = "asia-northeast1"
    gemini_api_key: SecretStr | None = None
    gemini_flash_model: str = "gemini-2.5-flash"
    gemini_pro_model: str = "gemini-2.5-pro"
    gemini_embed_model: str = "gemini-embedding-001"
    deepseek_model: str = "deepseek-reasoner"
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    deepseek_api_key: SecretStr | None = None

    #Streaming auth
    stream_token_ttl_seconds: int = 120


    # VALIDATOR
    validator_dry_run: bool = False
    validator_runs: int = 5
    validator_poll_seconds: int = 5
    validator_timeout_seconds: int = 300
    validator_max_heals: int = 2
    validator_variance_reduction_min: float = 0.80  
    validator_runtime_tolerance: float = 1.50     
    validator_ci_image: str = "python:3.12-slim"
    allowed_project_ids: Annotated[list[str], NoDecode] = Field(default_factory=list)



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

    @field_validator(
        "gemini_api_key", "deepseek_api_key",
        "langfuse_public_key", "langfuse_secret_key",
        mode="before",
    )
    @classmethod
    def _blank_to_none(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @property
    def is_production(self) -> bool:
        return self.env == "production"
    
    @field_validator("allowed_project_ids", mode="before")
    @classmethod
    def _split_project_ids(cls, value: object) -> object:
        if isinstance(value, str):
            return [p.strip() for p in value.split(",") if p.strip()]
        return value

    @property
    def write_allowlist(self) -> frozenset[str]:
        """Projects the Validator is permitted to branch/push/trigger against."""
        ids = set(self.allowed_project_ids)
        ids.add(self.demo_project_id)       
        return frozenset(ids)

    

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached singleton"""
    return Settings() 


