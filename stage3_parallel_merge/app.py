import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


def smart_merge(old: list[str], new: list[str]) -> list[str]:
    # 1. 合并
    merged = old + new

    # 2. 去重（保持顺序）
    merged = list(dict.fromkeys(merged))

    # 3. 过滤空值
    merged = [x for x in merged if x.strip()]

    return merged

class GraphState(TypedDict):
    topic: str
    notes: Annotated[list[str], smart_merge]
    summary: str


def collect_core_concept(state: GraphState) -> GraphState:
    topic = state["topic"]
    return {"notes": [f"{topic} 核心：基于有向图编排节点与状态流转。"]}


def collect_use_case(state: GraphState) -> GraphState:
    topic = state["topic"]
    return {"notes": [f"{topic} 场景：适合多步骤 Agent、分支逻辑、可恢复执行流程。"]}


def collect_use_case2(state: GraphState) -> GraphState:
    topic = state["topic"]
    return {"notes": [f"{topic} 场景2：适合多步骤 Agent、分支逻辑、可恢复执行流程。2"]}    


def build_summary(state: GraphState) -> GraphState:
    summary = "；".join(state["notes"])
    return {"summary": summary}


def main() -> None:
    builder = StateGraph(GraphState)
    builder.add_node("core_concept", collect_core_concept)
    builder.add_node("use_case", collect_use_case)
    builder.add_node("use_case2", collect_use_case2)
    builder.add_node("summarize_node", build_summary)

    builder.add_edge(START, "core_concept")
    builder.add_edge(START, "use_case")
    builder.add_edge(START, "use_case2")
    builder.add_edge("core_concept", "summarize_node")
    builder.add_edge("use_case", "summarize_node")
    builder.add_edge("use_case2", "summarize_node")
    builder.add_edge("summarize_node", END)

    graph = builder.compile()
    final_state = graph.invoke({"topic": "LangGraph", "notes": [], "summary": ""})

    print("并行收集结果：")
    for item in final_state["notes"]:
        print("-", item)
    print("最终摘要：", final_state["summary"])


if __name__ == "__main__":
    main()
