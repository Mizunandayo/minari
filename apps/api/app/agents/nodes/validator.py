from __future__ import annotations

from app.agents.state import MinariState


async def validator_node(state: MinariState) -> MinariState:
    # Day 4: branch + push + 5x isolated CI run + safety gate.
    return state
