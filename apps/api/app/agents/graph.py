"""LangGraph swarm wiring"""





from __future__ import annotations
from langgraph.graph import END, START, StateGraph
from app.agents.nodes.detective import detective_node
from app.agents.nodes.fixer import fixer_node
from app.agents.nodes.merger import merger_node
from app.agents.nodes.validator import validator_node
from app.agents.state import MinariState







def build_graph():
    g = StateGraph(MinariState)
    g.add_node("detective", detective_node)
    g.add_node("fixer", fixer_node)
    g.add_node("validator", validator_node)
    g.add_node("merger", merger_node)

    g.add_edge(START, "detective")
    g.add_edge("detective", END)
    return g.compile()




GRAPH = build_graph()

