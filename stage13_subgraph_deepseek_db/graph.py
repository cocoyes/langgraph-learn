from langgraph.graph import END, START, StateGraph

from db.repository import LearningRunRepository
from enums import QualityDecision, RouteType
from llm.deepseek_client import DeepSeekClient
from nodes.execution import (
    build_research_node,
    build_writer_direct_node,
    build_writer_with_research_node,
)
from nodes.intake import build_intake_node
from nodes.persist import build_persist_node
from nodes.planning import build_plan_node
from nodes.review import build_review_node, finalize_node, rewrite_round_node
from state import GraphState


def route_after_planning(state: GraphState) -> str:
    if state["route"] == RouteType.RESEARCH_AND_WRITE.value:
        return RouteType.RESEARCH_AND_WRITE.value
    return RouteType.DIRECT_WRITE.value


def route_after_review(state: GraphState) -> str:
    if state["quality_decision"] == QualityDecision.REWRITE.value:
        return QualityDecision.REWRITE.value
    return QualityDecision.PASS.value


def build_planning_subgraph(client: DeepSeekClient):
    builder = StateGraph(GraphState)
    builder.add_node("plan_node", build_plan_node(client))
    builder.add_edge(START, "plan_node")
    builder.add_edge("plan_node", END)
    return builder.compile()


def build_research_write_subgraph(client: DeepSeekClient):
    builder = StateGraph(GraphState)
    builder.add_node("research", build_research_node(client))
    builder.add_node("writer_with_research", build_writer_with_research_node(client))
    builder.add_edge(START, "research")
    builder.add_edge("research", "writer_with_research")
    builder.add_edge("writer_with_research", END)
    return builder.compile()


def build_direct_write_subgraph(client: DeepSeekClient):
    builder = StateGraph(GraphState)
    builder.add_node("writer_direct", build_writer_direct_node(client))
    builder.add_edge(START, "writer_direct")
    builder.add_edge("writer_direct", END)
    return builder.compile()


def build_main_graph(client: DeepSeekClient, repository: LearningRunRepository):
    planning_subgraph = build_planning_subgraph(client)
    research_write_subgraph = build_research_write_subgraph(client)
    direct_write_subgraph = build_direct_write_subgraph(client)

    builder = StateGraph(GraphState)
    builder.add_node("intake", build_intake_node(client))
    builder.add_node("planning_flow", planning_subgraph)
    builder.add_node("research_and_write_flow", research_write_subgraph)
    builder.add_node("direct_write_flow", direct_write_subgraph)
    builder.add_node("review", build_review_node(client))
    builder.add_node("rewrite_round_node", rewrite_round_node)
    builder.add_node("finalize", finalize_node)
    builder.add_node("persist", build_persist_node(repository))

    builder.add_edge(START, "intake")
    builder.add_edge("intake", "planning_flow")

    builder.add_conditional_edges(
        "planning_flow",
        route_after_planning,
        {
            RouteType.RESEARCH_AND_WRITE.value: "research_and_write_flow",
            RouteType.DIRECT_WRITE.value: "direct_write_flow",
        },
    )
    builder.add_edge("research_and_write_flow", "review")
    builder.add_edge("direct_write_flow", "review")
    builder.add_conditional_edges(
        "review",
        route_after_review,
        {
            QualityDecision.PASS.value: "finalize",
            QualityDecision.REWRITE.value: "rewrite_round_node",
        },
    )
    builder.add_edge("rewrite_round_node", "planning_flow")
    builder.add_edge("finalize", "persist")
    builder.add_edge("persist", END)

    return builder.compile()
