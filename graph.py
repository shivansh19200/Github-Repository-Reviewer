from typing import TypedDict

from langgraph.graph import StateGraph

from agents.architecture import architecture_agent
from agents.code_quality_agent import code_quality_agent


# This is the shared state that every agent can access
class GraphState(TypedDict):

    repo: list

    architecture_review: str

    code_quality_review: str

builder = StateGraph(GraphState)


builder.add_node("Architecture Reviewer", architecture_agent)
builder.add_node("Code Quality Reviewer", code_quality_agent)

builder.set_entry_point("Architecture Reviewer")


builder.add_edge("Architecture Reviewer", "Code Quality Reviewer")

graph = builder.compile()
