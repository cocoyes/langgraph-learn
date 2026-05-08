from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


Decision = Literal["retry", "fallback", "format"]


class GraphState(TypedDict):
    user_id: str
    attempts: int
    max_attempts: int
    profile: str
    error: str
    source: str
    response: str


def fetch_primary(state: GraphState) -> GraphState:
    attempts = state["attempts"] + 1
    # 模拟不稳定服务：前两次失败，第三次成功
    if attempts < 3:
        return {"attempts": attempts, "error": f"primary timeout (attempt={attempts})"}
    return {
        "attempts": attempts,
        "profile": f"user={state['user_id']}, plan=pro, score=92",
        "error": "",
        "source": "primary",
    }


def decide_after_primary(state: GraphState) -> Decision:
    if not state["error"]:
        return "format"
    if state["attempts"] < state["max_attempts"]:
        return "retry"
    return "fallback"


def fallback_cache(state: GraphState) -> GraphState:
    return {
        "profile": f"user={state['user_id']}, plan=basic, score=70 (cached)",
        "source": "fallback_cache",
        "error": "",
    }


def format_response(state: GraphState) -> GraphState:
    response = (
        f"数据来源：{state['source']}；"
        f"尝试次数：{state['attempts']}；"
        f"画像结果：{state['profile']}"
    )
    return {"response": response}


def main() -> None:
    builder = StateGraph(GraphState)
    builder.add_node("fetch_primary", fetch_primary)
    builder.add_node("fallback_cache", fallback_cache)
    builder.add_node("format_response", format_response)

    builder.add_edge(START, "fetch_primary")
    builder.add_conditional_edges(
        "fetch_primary",
        decide_after_primary,
        {
            "retry": "fetch_primary",
            "fallback": "fallback_cache",
            "format": "format_response",
        },
    )
    builder.add_edge("fallback_cache", "format_response")
    builder.add_edge("format_response", END)

    graph = builder.compile()
    final_state = graph.invoke(
        {
            "user_id": "u-1001",
            "attempts": 0,
            "max_attempts": 3,
            "profile": "",
            "error": "",
            "source": "",
            "response": "",
        }
    )
    print(final_state["response"])


if __name__ == "__main__":
    main()
