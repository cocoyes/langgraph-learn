from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


Approval = Literal["approve", "revise", "reject"]
Decision = Literal["execute", "revise_plan", "stop"]


class GraphState(TypedDict):
    requirement: str
    draft_plan: str
    revision_notes: str
    approval: Approval
    revision_count: int
    max_revisions: int
    result: str


def plan_node(state: GraphState) -> GraphState:
    requirement = state["requirement"]
    revision_notes = state["revision_notes"].strip()
    base = f"执行方案：围绕“{requirement}”拆分任务、分配责任、按日跟踪。"
    if revision_notes:
        base += f" 已按审批意见修订：{revision_notes}"
    return {"draft_plan": base}


def approval_node(state: GraphState) -> GraphState:
    # 教学示例：通过 revision_count 模拟审批结果变化
    if state["revision_count"] == 0:
        return {"approval": "revise", "revision_notes": "补充风险清单和回滚策略。"}
    if state["revision_count"] == 1:
        return {"approval": "approve", "revision_notes": ""}
    return {"approval": "reject", "revision_notes": "修订次数过多，终止流程。"}


def decide_after_approval(state: GraphState) -> Decision:
    if state["approval"] == "approve":
        return "execute"
    if state["approval"] == "revise" and state["revision_count"] < state["max_revisions"]:
        return "revise_plan"
    return "stop"


def revise_node(state: GraphState) -> GraphState:
    return {"revision_count": state["revision_count"] + 1}


def execute_node(state: GraphState) -> GraphState:
    return {"result": f"审批通过，开始执行：{state['draft_plan']}"}


def stop_node(state: GraphState) -> GraphState:
    return {"result": f"流程终止，最终审批状态：{state['approval']}。"}


def main() -> None:
    builder = StateGraph(GraphState)
    builder.add_node("plan", plan_node)
    builder.add_node("approval", approval_node)
    builder.add_node("revise", revise_node)
    builder.add_node("execute", execute_node)
    builder.add_node("stop", stop_node)

    builder.add_edge(START, "plan")
    builder.add_edge("plan", "approval")
    builder.add_conditional_edges(
        "approval",
        decide_after_approval,
        {"execute": "execute", "revise_plan": "revise", "stop": "stop"},
    )
    builder.add_edge("revise", "plan")
    builder.add_edge("execute", END)
    builder.add_edge("stop", END)

    graph = builder.compile()
    final_state = graph.invoke(
        {
            "requirement": "上线 LangGraph 智能客服",
            "draft_plan": "",
            "revision_notes": "",
            "approval": "revise",
            "revision_count": 0,
            "max_revisions": 2,
            "result": "",
        }
    )
    print(final_state["result"])


if __name__ == "__main__":
    main()
