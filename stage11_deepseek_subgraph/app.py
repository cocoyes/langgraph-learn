#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from config import load_config
from llm_client import DeepSeekClient


class GraphState(TypedDict):
    user_query: str
    plan: str
    answer: str


def build_plan_node(client: DeepSeekClient):
    def plan_node(state: GraphState) -> GraphState:
        content = client.invoke(
            system_prompt="你是方案设计师，请输出执行计划。",
            user_prompt=state["user_query"],
        )
        return {"plan": content}

    return plan_node


def build_answer_node(client: DeepSeekClient):
    def answer_node(state: GraphState) -> GraphState:
        content = client.invoke(
            system_prompt="你是高级工程师，请根据计划输出可执行答案。",
            user_prompt="需求：{}\n计划：{}".format(state["user_query"], state["plan"]),
        )
        return {"answer": content}

    return answer_node


def build_generation_subgraph(client: DeepSeekClient):
    sub_builder = StateGraph(GraphState)
    sub_builder.add_node("plan_node", build_plan_node(client))
    sub_builder.add_node("answer_node", build_answer_node(client))
    sub_builder.add_edge(START, "plan_node")
    sub_builder.add_edge("plan_node", "answer_node")
    sub_builder.add_edge("answer_node", END)
    return sub_builder.compile()


def main() -> None:

    

    config = load_config()
    client = DeepSeekClient(
        api_key=config.api_key,
        base_url=config.base_url,
        model=config.model,
        thinking_type=config.thinking_type,
        connect_timeout_seconds=config.connect_timeout_seconds,
        read_timeout_seconds=config.read_timeout_seconds,
        max_retries=config.max_retries,
    )

    generation_subgraph = build_generation_subgraph(client)

    builder = StateGraph(GraphState)
    builder.add_node("generation_flow", generation_subgraph)
    builder.add_edge(START, "generation_flow")
    builder.add_edge("generation_flow", END)
    graph = builder.compile()

    result = graph.invoke(
        {"user_query": "给我一套 LangGraph 子图学习路线", "plan": "", "answer": ""}
    )
    print(result["answer"])


if __name__ == "__main__":
    main()
