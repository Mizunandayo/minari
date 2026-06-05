"""Request/response models for the diagnosis API."""


from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.diagnosis import Diagnosis


class DiagnoseRequest(BaseModel):
    model_config = {"extra": "forbid"}

    project_id: str = Field(min_length=1, max_length=200)
    file_path: str = Field(min_length=1, max_length=400)
    test_name: str = Field(min_length=1, max_length=300)
    pipeline_id: int | None = Field(default=None, ge=1)
    ref: str = Field(default="main", max_length=200)



class DiagnoseAccepted(BaseModel):
    run_id: str
    stream_path: str
    stream_token: str



class DiagnosisResult(BaseModel):
    run_id: str
    status: str
    model_used: str | None = None
    pfs_score: float | None = None
    diagnosis: Diagnosis | None = None
    latency_ms: int | None = None
    error: str | None = None


class TestListItem(BaseModel):
    """One row in the dashboard test list (test + its latest diagnosis)."""
    id: str
    test_name: str
    file_path: str
    language: str | None = None
    pfs_score: float | None = None
    category: str | None = None
    confidence: float | None = None



