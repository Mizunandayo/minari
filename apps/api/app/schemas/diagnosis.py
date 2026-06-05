"""Diagnosis schema"""


from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, field_validator


class RootCause(str, Enum):
    ASYNC = "async"
    RACE = "race"
    RESOURCE = "resource"
    NETWORK = "network"
    DATA = "data"







class ReasoningStep(BaseModel):
    step: int = Field(ge=1, le=12)
    observation: str = Field(min_length=3, max_length=600)







class Diagnosis(BaseModel):
    # NOTE: no extra="forbid" — it makes Pydantic emit `additionalProperties: false`,
    # which google-genai 1.2.0's response_schema converter rejects. Not needed:
    # Gemini structured output is schema-constrained (can't add keys), and any
    # stray keys from a free-form model are harmlessly ignored at validation.
    category: RootCause
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning_chain: list[ReasoningStep] = Field(min_length=1, max_length=12)
    triggering_lines: list[int] = Field(default_factory=list, max_length=20)
    affected_operations: str = Field(min_length=3, max_length=400)
    recommended_fix_category: str = Field(min_length=2, max_length=40)


    @field_validator("triggering_lines")
    @classmethod
    def _positive_lines(cls, v: list[int]) -> list[int]:
        if any(n < 1 for n in v):
            raise ValueError("line numbers are 1-based and must be positive")
        return v

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.6








