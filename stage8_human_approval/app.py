#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

try:
    from typing import TypedDict
except Exception:
    try:
        from typing_extensions import TypedDict
    except Exception:
        TypedDict = None

try:
    from langgraph.graph import END, START, StateGraph
except Exception:
    END = None
    START = None
    StateGraph = None


APPROVAL_APPROVE = "approve"
APPROVAL_REVISE = "revise"
APPROVAL_REJECT = "reject"

DECISION_EXECUTE = "execute"
DECISION_REVISE_PLAN = "revise_plan"
DECISION_STOP = "stop"

if TypedDict is not None:
    GraphState = TypedDict(
        "GraphState",
        {
            "requirement": str,
            "draft_plan": str,
            "revision_notes": str,
            "approval": str,
            "revision_count": int,
            "max_revisions": int,
            "result": str,
        },
    )
else:
    GraphState = dict


def plan_node(state):
    requirement = state["requirement"]
    revision_notes = state["revision_notes"].strip()
    base = "执行方案：围绕“{}”拆分任务、分配责任、按日跟踪。".format(requirement)
    if revision_notes:
        base += " 已按审批意见修订：{}".format(revision_notes)
    return {"draft_plan": base}


def approval_node(state):
    # 教学示例：通过 revision_count 模拟审批结果变化
    if state["revision_count"] == 0:
        return {"approval": APPROVAL_REVISE, "revision_notes": "补充风险清单和回滚策略。"}
    if state["revision_count"] == 1:
        return {"approval": APPROVAL_APPROVE, "revision_notes": ""}
    return {"approval": APPROVAL_REJECT, "revision_notes": "修订次数过多，终止流程。"}


def decide_after_approval(state):
    if state["approval"] == APPROVAL_APPROVE:
        return DECISION_EXECUTE
    if state["approval"] == APPROVAL_REVISE and state["revision_count"] < state["max_revisions"]:
        return DECISION_REVISE_PLAN
    return DECISION_STOP


def revise_node(state):
    return {"revision_count": state["revision_count"] + 1}


def execute_node(state):
    return {"result": "审批通过，开始执行：{}".format(state["draft_plan"])}


def stop_node(state):
    return {"result": "流程终止，最终审批状态：{}。".format(state["approval"])}


def main():
    if sys.version_info < (3, 8):
        print("请使用 Python 3.8+ 运行，例如：python3 app.py")
        return
    if StateGraph is None:
        print("缺少依赖 langgraph，请先执行：pip3 install -r ../requirements.txt")
        return

    builder = StateGraph(GraphState)
    builder.add_node("plan", plan_node)
    builder.add_node("approval_step", approval_node)
    builder.add_node("revise", revise_node)
    builder.add_node("execute", execute_node)
    builder.add_node("stop", stop_node)

    builder.add_edge(START, "plan")
    builder.add_edge("plan", "approval_step")
    builder.add_conditional_edges(
        "approval_step",
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
            "approval": APPROVAL_REVISE,
            "revision_count": 0,
            "max_revisions": 2,
            "result": "",
        }
    )
    print(final_state["result"])


if __name__ == "__main__":
    main()
