"""Reasoning-panel""" 

from __future__ import annotations

import asyncio
import time
from typing import Literal

from pydantic import BaseModel, Field


def _now_ms() -> int:
    return int(time.time() * 1000)


class _Base(BaseModel):
    type: str
    stage: str            
    ts_ms: int = Field(default_factory=_now_ms)



class MCPCallEvent(_Base):
    type: Literal["mcp_call"] = "mcp_call"
    tool: str
    params_summary: str

class MCPResultEvent(_Base):
    type: Literal["mcp_result"] = "mcp_result"
    tool: str
    bytes: int
    latency_ms: int

class ReasonEvent(_Base):
    type: Literal["reason"] = "reason"
    text: str



class DecideEvent(_Base):
    type: Literal["decide"] = "decide"
    text: str


class FixEvent(_Base):
    type: Literal["fix"] = "fix"
    rank: int
    fix_category: str
    confidence: float
    explanation: str
    fix_diff: str
    language: str
    syntax_valid: bool
    assertions_safe: bool



class VerifyEvent(_Base):
    type: Literal["verify"] = "verify"
    run_index: int
    total_runs: int
    passed: bool
    duration_ms: float
    gate_passed: bool = False
    variance_reduction_pct: float = 0.0


class HealEvent(_Base):
    type: Literal["heal"] = "heal"
    attempt: int
    reason: str


class DoneEvent(_Base):
    type: Literal["done"] = "done"
    confidence: float
    category: str



class ErrorEvent(_Base):
    type: Literal["error"] = "error"
    message: str



class MergeEvent(_Base):
    type: Literal["merge"] = "merge"
    mr_iid: int | None = None
    mr_url: str | None = None
    assigned_to: str | None = None
    detection_confidence: float = 0.0
    diagnosis_confidence: float = 0.0
    fix_confidence: float = 0.0
    verification_confidence: float = 0.0
    overall_confidence: float = 0.0




Event = (
    MCPCallEvent | MCPResultEvent | ReasonEvent | DecideEvent
    | FixEvent | VerifyEvent | HealEvent | MergeEvent | DoneEvent | ErrorEvent
)




class EventBus:
    """Single-run pub/sub backed by asyncio.queue"""

    _SENTINEL = object()


    def __init__(self, maxsize: int = 256) -> None:
        self._q: asyncio.Queue = asyncio.Queue(maxsize=maxsize)


    async def emit(self, event: Event) -> None:
        try:
            self._q.put_nowait(event)
        except asyncio.QueueFull:
            _ = self._q.get_nowait()        
            self._q.put_nowait(event)


    async def close(self) -> None:
        await self._q.put(self._SENTINEL)


    async def stream(self):
        while True:
            item = await self._q.get()
            if item is self._SENTINEL:
                return
            yield item



RUNS: dict[str, EventBus] = {}