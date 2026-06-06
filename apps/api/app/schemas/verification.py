"""Verification meta test result schemas"""


from __future__ import annotations

from pydantic import BaseModel, Field


class RunResult(BaseModel):
    """One of the 5 isolated ci runs."""
    index: int = Field(ge=1)
    passed: bool
    duration_ms: float = Field(ge=0.0)




class VerificationReport(BaseModel):
    branch_name: str
    pipeline_id: int | None = None
    chosen_rank: int | None = None   
    run_results: list[RunResult] = Field(default_factory=list)
    pass_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    variance_before: float = Field(default=0.0, ge=0.0)
    variance_after: float = Field(default=0.0, ge=0.0)
    variance_reduction_pct: float = Field(default=0.0)  
    gate_passed: bool = False
    healing_attempts: int = Field(default=0, ge=0, le=2)
    issue_url: str | None = None       

    @property
    def summary(self) -> str:
        passed = sum(1 for r in self.run_results if r.passed)
        return (f"{passed}/{len(self.run_results)} passed · "
                f"variance −{self.variance_reduction_pct * 100:.0f}% · "
                f"gate {'PASSED' if self.gate_passed else 'FAILED'}")