#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class GraphState(TypedDict):
    requirement: str
    context: str
    draft_answer: str
    review_comment: str
    final_answer: str


def planning_node(state: GraphState) -> GraphState:
    return {"context": "需求已拆解为目标、约束、验收标准三部分。"}


def collect_context_node(state: GraphState) -> GraphState:
    context = state["context"] + " 子图补充：优先保证可运行与可验证。"
    return {"context": context}


def write_draft_node(state: GraphState) -> GraphState:
    draft = "围绕需求「{}」给出初稿：先实现主流程，再补充异常处理。".format(state["requirement"])
    return {"draft_answer": draft}


def review_node(state: GraphState) -> GraphState:
    comment = "评审建议：补充输入输出示例与失败场景。"
    return {"review_comment": comment}


def finalize_node(state: GraphState) -> GraphState:
    final_answer = "{}\n{}".format(state["draft_answer"], state["review_comment"])
    return {"final_answer": final_answer}


def build_drafting_subgraph():
    sub_builder = StateGraph(GraphState)
    sub_builder.add_node("collect_context_node", collect_context_node)
    sub_builder.add_node("write_draft_node", write_draft_node)
    sub_builder.add_edge(START, "collect_context_node")
    sub_builder.add_edge("collect_context_node", "write_draft_node")
    sub_builder.add_edge("write_draft_node", END)
    return sub_builder.compile()


def main() -> None:
    drafting_subgraph = build_drafting_subgraph()

    builder = StateGraph(GraphState)
    builder.add_node("planning_node", planning_node)
    builder.add_node("drafting_flow", drafting_subgraph)
    builder.add_node("review_node", review_node)
    builder.add_node("finalize_node", finalize_node)

    builder.add_edge(START, "planning_node")
    builder.add_edge("planning_node", "drafting_flow")
    builder.add_edge("drafting_flow", "review_node")
    builder.add_edge("review_node", "finalize_node")
    builder.add_edge("finalize_node", END)

    graph = builder.compile()
    result = graph.invoke(
        {
            "requirement": "设计一个 LangGraph 学习计划",
            "context": "",
            "draft_answer": "",
            "review_comment": "",
            "final_answer": "",
        }
    )
    print(result["final_answer"])


if __name__ == "__main__":
    main()
