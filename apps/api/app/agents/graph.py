"""LangGraph swarm wiring"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.agents.nodes.detective import detective_node
from app.agents.nodes.fixer import fixer_node
from app.agents.nodes.merger import merger_node
from app.agents.nodes.validator import validator_node
from app.agents.state import MinariState


def _after_detective(state: MinariState) -> str:
    if state.diagnosis is not None and state.diagnosis.is_confident:
        return "fixer"
    return END




def _after_fixer(state: MinariState) -> str:

    if state.fixes is not None and state.fixes.candidates:
        return "validator"
    return END


def _after_validator(state: MinariState) -> str:
    if (state.status == "verified"
            and state.verification is not None
            and state.verification.gate_passed):
        return "merger"
    return END


def build_graph():
    g = StateGraph(MinariState)
    g.add_node("detective", detective_node)
    g.add_node("fixer", fixer_node)
    g.add_node("validator", validator_node)
    g.add_node("merger", merger_node)
    g.add_edge(START, "detective")
    g.add_conditional_edges("detective", _after_detective, {"fixer": "fixer", END: END})
    g.add_conditional_edges("fixer", _after_fixer, {"validator": "validator", END: END})
    g.add_conditional_edges("validator", _after_validator, {"merger": "merger", END: END})
    g.add_edge("merger", END)
    return g.compile()





GRAPH = build_graph()
