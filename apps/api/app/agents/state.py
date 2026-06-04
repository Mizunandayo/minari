"""MinariState"""





from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.diagnosis import Diagnosis





class MinariState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    #inputs
    run_id: str
    project_id: str
    file_path: str
    test_name: str
    ref: str = "main"
    pipeline_id: int | None = None

    # evidence
    test_source: str | None = None
    pipeline_log: str | None = None
    git_blame: str | None = None
    similar_examples: list[str] = Field(default_factory=list)

    # detected metadata + embedding (real fields so they survive model_validate)
    language: str | None = None
    framework: str | None = None
    embedding: list[float] | None = None

    # scoring / routing
    pfs_score: float = 50.0
    model_used: str | None = None

    # outputs
    diagnosis: Diagnosis | None = None
    status: str = "running"        
    error: str | None = None