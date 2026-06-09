"""Resilience decorator — every graph node degrades gracefully.

Wrapping a node guarantees the graph always reaches END and the SSE stream always
closes: an exception inside a node becomes a logged ErrorEvent + status='error' on
the state, never a mid-stream 500 or a hung browser EventSource.
"""


from __future__ import annotations

import functools
from collections.abc import Awaitable, Callable

from app.agents.events import RUNS, ErrorEvent
from app.agents.state import MinariState
from app.core.logging import get_logger

log = get_logger("minari.agents")
NodeFn = Callable[[MinariState], Awaitable[MinariState]]



def resilient_node(stage: str) -> Callable[[NodeFn], NodeFn]:
    def decorator(fn: NodeFn) -> NodeFn:
        @functools.wraps(fn)
        async def wrapper(state: MinariState) -> MinariState:
            try:
                return await fn(state)
            except Exception as exc: 
                log.error("node.failed", stage=stage, run_id=state.run_id,
                          error=str(exc), exc_info=True)
                bus = RUNS.get(state.run_id)
                if bus is not None:
                    await bus.emit(ErrorEvent(
                        stage=stage,
                        message=f"{stage} stage could not complete; pipeline halted safely.",
                    ))
                state.status = "error"
                state.error = f"{stage}: {type(exc).__name__}"
                return state
        return wrapper
    return decorator