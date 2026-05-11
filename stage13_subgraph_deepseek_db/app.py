#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import load_config
from db.repository import LearningRunRepository
from graph import build_main_graph
from llm.deepseek_client import DeepSeekClient


def main() -> None:
    config = load_config()
    client = DeepSeekClient(
        api_key=config.deepseek_api_key,
        base_url=config.deepseek_base_url,
        model=config.deepseek_model,
        thinking_type=config.deepseek_thinking_type,
        connect_timeout_seconds=config.deepseek_connect_timeout_seconds,
        read_timeout_seconds=config.deepseek_read_timeout_seconds,
        max_retries=config.deepseek_max_retries,
    )
    repository = LearningRunRepository(db_path=config.db_path)
    graph = build_main_graph(client=client, repository=repository)

    user_query = "请给我一套 LangGraph 学习到生产落地的进阶方案，包含子图、数据库记忆和真实大模型接入。"
    result = graph.invoke(
        {
            "user_query": user_query,
            "intent": "",
            "route": "",
            "plan": "",
            "research_notes": "",
            "draft_answer": "",
            "final_answer": "",
            "quality_score": 0,
            "quality_decision": "",
            "rewrite_round": 0,
            "max_rewrite_rounds": config.max_rewrite_rounds,
            "persisted_id": 0,
        }
    )

    print("\n===== Stage 13 Result =====")
    print("intent:", result["intent"])
    print("route:", result["route"])
    print("quality_score:", result["quality_score"])
    print("persisted_id:", result["persisted_id"])
    print("\nfinal_answer:\n")
    print(result["final_answer"])

    print("\n===== Recent Runs =====")
    recent_runs = repository.list_recent(limit=5)
    for item in recent_runs:
        print(
            "#{} | intent={} | score={} | {}".format(
                item["id"], item["intent"], item["quality_score"], item["created_at"]
            )
        )


if __name__ == "__main__":
    main()
