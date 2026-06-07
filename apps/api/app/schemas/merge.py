"""Merge-request delivery record"""



from __future__ import annotations

from pydantic import BaseModel, Field


class MergeReport(BaseModel):
    mr_iid: int | None = None
    mr_url: str | None = None
    source_branch: str
    target_branch: str = "main"
    assigned_to: str | None = None
    labels: list[str] = Field(default_factory=list)


    # Confidence cascade computed once server-side
    detection_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    diagnosis_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    fix_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    verification_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    overall_confidence: float = Field(default=0.0, ge=0.0, le=1.0)

    status: str = "created"   # "created" | "failed"



    @property
    def summary(self) -> str:
        if self.mr_iid is None:
            return "MR not created"
        return (f"MR !{self.mr_iid} - confidence "
                f"{self.overall_confidence * 100:.0f}% - "
                f"reviewer {self.assigned_to or 'unassigned'}")

