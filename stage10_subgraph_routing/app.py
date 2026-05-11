#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

RouteType = Literal["fast_track", "deep_track"]


class GraphState(TypedDict):
    question: str
    route: RouteType
    notes: str
    answer: str


def route_node(state: GraphState) -> GraphState:
    question = state["question"].strip()
    route: RouteType = "deep_track" if len(question) >= 25 else "fast_track"
    return {"route": route}


def select_track(state: GraphState) -> str:
    return state["route"]


def fast_summary_node(state: GraphState) -> GraphState:
    notes = "快速轨道：给出简短步骤，优先快速落地。"
    return {"notes": notes}


def deep_research_node(state: GraphState) -> GraphState:
    notes = "深度轨道：补充架构、风险、观测指标与回滚方案。"
    return {"notes": notes}


def answer_node(state: GraphState) -> GraphState:
    answer = "问题：{}\n路径：{}\n结果：{}".format(state["question"], state["route"], state["notes"])
    return {"answer": answer}


def build_fast_subgraph():
    sub_builder = StateGraph(GraphState)
    sub_builder.add_node("fast_summary_node", fast_summary_node)
    sub_builder.add_edge(START, "fast_summary_node")
    sub_builder.add_edge("fast_summary_node", END)
    return sub_builder.compile()


def build_deep_subgraph():
    sub_builder = StateGraph(GraphState)
    sub_builder.add_node("deep_research_node", deep_research_node)
    sub_builder.add_edge(START, "deep_research_node")
    sub_builder.add_edge("deep_research_node", END)
    return sub_builder.compile()


def main() -> None:
    fast_subgraph = build_fast_subgraph()
    deep_subgraph = build_deep_subgraph()

    builder = StateGraph(GraphState)
    builder.add_node("route_node", route_node)
    builder.add_node("fast_flow", fast_subgraph)
    builder.add_node("deep_flow", deep_subgraph)
    builder.add_node("answer_node", answer_node)

    builder.add_edge(START, "route_node")
    builder.add_conditional_edges(
        "route_node",
        select_track,
        {"fast_track": "fast_flow", "deep_track": "deep_flow"},
    )
    builder.add_edge("fast_flow", "answer_node")
    builder.add_edge("deep_flow", "answer_node")
    builder.add_edge("answer_node", END)

    graph = builder.compile()

    examples = [
        "怎么快速写一个 LangGraph demo？",
        "我想做一个可扩展的 LangGraph 生产系统，需要节点拆分和容错策略，怎么设计？",
    ]
    for question in examples:
        result = graph.invoke({"question": question, "route": "fast_track", "notes": "", "answer": ""})
        print("\n====")
        print(result["answer"])


if __name__ == "__main__":
    main()
