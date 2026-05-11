#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from config import load_config
from llm_client import DeepSeekClient
from repository import RunRepository


class GraphState(TypedDict):
    user_query: str
    answer: str
    run_id: int
    history: str


def build_answer_node(client: DeepSeekClient):
    def answer_node(state: GraphState) -> GraphState:
        answer = client.invoke(
            system_prompt="你是生产化架构顾问，请输出可执行建议。",
            user_prompt=(
                "请围绕该问题给建议，要求包含：架构、观测、容错、上线步骤。\n"
                "问题：" + state["user_query"]
            ),
        )
        return {"answer": answer}

    return answer_node


def build_persist_node(repo: RunRepository):
    def persist_node(state: GraphState) -> GraphState:
        run_id = repo.save(user_query=state["user_query"], answer=state["answer"])
        return {"run_id": run_id if run_id is not None else 0}

    return persist_node


def build_history_node(repo: RunRepository):
    def history_node(_: GraphState) -> GraphState:
        items = repo.list_recent(limit=5)
        if not items:
            return {"history": "最近无历史记录。"}
        lines = ["最近记录："]
        for item in items:
            lines.append("- #{} {} {}".format(item["id"], item["created_at"], item["user_query"]))
        return {"history": "\n".join(lines)}

    return history_node


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
    repo = RunRepository(db_path=config.db_path)

    builder = StateGraph(GraphState)
    builder.add_node("answer_node", build_answer_node(client))
    builder.add_node("persist_node", build_persist_node(repo))
    builder.add_node("history_node", build_history_node(repo))
    builder.add_edge(START, "answer_node")
    builder.add_edge("answer_node", "persist_node")
    builder.add_edge("persist_node", "history_node")
    builder.add_edge("history_node", END)
    graph = builder.compile()

    result = graph.invoke(
        {
            "user_query": "LangGraph 怎么做生产级可观测？",
            "answer": "",
            "run_id": 0,
            "history": "",
        }
    )
    print("run_id:", result["run_id"])
    print(result["history"])


if __name__ == "__main__":
    main()
