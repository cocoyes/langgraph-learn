from typing import Literal, TypedDict
from langgraph.graph import END, START, StateGraph


Decision = Literal["revise", "finish"]


class GraphState(TypedDict):
    topic: str
    draft: str
    feedback: str
    score: int
    iteration: int
    max_iterations: int


def draft_content(state: GraphState) -> GraphState:
    topic = state["topic"]
    iteration = state["iteration"]

    if iteration == 0:
        draft = f"{topic} 入门说明：先理解核心概念，再通过小例子动手实践。"
    else:
        draft = (
            state["draft"]
            + f" 第 {iteration + 1} 轮补充：增加边界条件、错误处理和可观测性说明。"
        )

    return {"draft": draft}


def review_content(state: GraphState) -> GraphState:
    draft = state["draft"]

    score = 60
    if "边界条件" in draft:
        score += 20
    if "错误处理" in draft:
        score += 10
    if "可观测性" in draft:
        score += 10

    feedback = "达到发布标准。" if score >= 90 else "内容还不够完整，需要继续补充工程细节。"

    return {"score": score, "feedback": feedback}


def decide_next_step(state: GraphState) -> Decision:
    reached_quality = state["score"] >= 90
    reached_limit = state["iteration"] >= state["max_iterations"]
    return "finish" if reached_quality or reached_limit else "revise"


def revise_content(state: GraphState) -> GraphState:
    return {"iteration": state["iteration"] + 1}


def main() -> None:
    builder = StateGraph(GraphState)

    # ⚠️ 关键修改：node 名称不要叫 draft / review / revise（避免和字段冲突更安全）
    builder.add_node("draft_node", draft_content)
    builder.add_node("review_node", review_content)
    builder.add_node("revise_node", revise_content)

    builder.add_edge(START, "draft_node")
    builder.add_edge("draft_node", "review_node")

    builder.add_conditional_edges(
        "review_node",
        decide_next_step,
        {"revise": "revise_node", "finish": END},
    )

    builder.add_edge("revise_node", "draft_node")

    graph = builder.compile()

    final_state = graph.invoke(
        {
            "topic": "LangGraph 实战指南",
            "draft": "",
            "feedback": "",
            "score": 0,
            "iteration": 0,
            "max_iterations": 2,
        }
    )

    print("最终迭代轮次：", final_state["iteration"] + 1)
    print("最终评分：", final_state["score"])
    print("评审反馈：", final_state["feedback"])
    print("最终草稿：", final_state["draft"])


if __name__ == "__main__":
    main()