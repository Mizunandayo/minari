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




class DoneEvent(_Base):
    type: Literal["done"] = "done"
    confidence: float
    category: str




class ErrorEvent(_Base):
    type: Literal["error"] = "error"
    message: str






Event = (
    MCPCallEvent | MCPResultEvent | ReasonEvent | DecideEvent | DoneEvent | ErrorEvent
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