"""Fix candidate schema"""




from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class FixCategory(str, Enum):
    # Must match the fixes
    SYNC = "sync"
    WAIT = "wait"
    ISOLATE = "isolate"
    TIMEOUT = "timeout"
    RESOURCE = "resource"












class FixDraft(BaseModel):
    # EXACTLY what Gemini authors. No defaulted fields — the google-genai
    # response_schema converter rejects any field that emits a JSON-schema
    # "default" ("Default value is not supported in the response schema").
    rank: int = Field(ge=1, le=3)
    fix_category: FixCategory
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str = Field(min_length=10, max_length=900)
    fixed_source: str = Field(min_length=1, max_length=20_000)


class FixDrafts(BaseModel):
    candidates: list[FixDraft] = Field(min_length=1, max_length=3)


class FixCandidate(FixDraft):
    # Server-enriched candidate: the draft fields plus our computed, validated
    # fields. These carry defaults — fine, because this model is NEVER sent to
    # Gemini as a response_schema (only FixDrafts is).
    fix_diff: str = Field(default="", max_length=24_000)
    syntax_valid: bool = Field(default=False)
    assertions_safe: bool = Field(default=False)

    @property
    def is_safe(self) -> bool:
        return self.syntax_valid and self.assertions_safe











class FixCandidates(BaseModel):
    candidates: list[FixCandidate] = Field(min_length=1, max_length=3)














