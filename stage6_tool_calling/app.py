import ast
from datetime import date
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


ToolName = Literal["calculator", "weather", "kb"]
RouteName = Literal["calculator_node", "weather_node", "kb_node"]


class GraphState(TypedDict):
    question: str
    tool_name: ToolName
    tool_input: str
    tool_result: str
    answer: str


def planner_node(state: GraphState) -> GraphState:
    question = state["question"].strip()
    lower = question.lower()

    if any(ch in question for ch in ["+", "-", "*", "/"]):
        return {"tool_name": "calculator", "tool_input": question}
    if "天气" in question or "weather" in lower:
        return {"tool_name": "weather", "tool_input": question}
    return {"tool_name": "kb", "tool_input": question}


def route_tool(state: GraphState) -> RouteName:
    mapping: dict[ToolName, RouteName] = {
        "calculator": "calculator_node",
        "weather": "weather_node",
        "kb": "kb_node",
    }
    return mapping[state["tool_name"]]


def calculator_node(state: GraphState) -> GraphState:
    expression = state["tool_input"].replace("=", "").strip()
    try:
        node = ast.parse(expression, mode="eval")
        result = eval(compile(node, "<calc>", "eval"), {"__builtins__": {}}, {})
        return {"tool_result": f"计算结果：{result}"}
    except Exception:
        return {"tool_result": "计算失败：请提供简单算术表达式，例如 12 * (3 + 1)。"}


def weather_node(state: GraphState) -> GraphState:
    today = date.today().isoformat()
    return {"tool_result": f"天气工具（模拟）：{today} 晴，24-30C，适合外出学习。"}


def kb_node(state: GraphState) -> GraphState:
    question = state["tool_input"]
    return {
        "tool_result": (
            "知识库工具（模拟）：LangGraph 适合构建可控、可追踪、支持分支和记忆的 Agent 工作流。"
            f" 你的问题是：{question}"
        )
    }


def responder_node(state: GraphState) -> GraphState:
    answer = (
        f"已调用工具：{state['tool_name']}。\n"
        f"工具输出：{state['tool_result']}\n"
        "建议：若结果不满足预期，可改写问题后再次调用。"
    )
    return {"answer": answer}


def main() -> None:
    builder = StateGraph(GraphState)
    builder.add_node("planner", planner_node)
    builder.add_node("calculator_node", calculator_node)
    builder.add_node("weather_node", weather_node)
    builder.add_node("kb_node", kb_node)
    builder.add_node("responder", responder_node)

    builder.add_edge(START, "planner")
    builder.add_conditional_edges(
        "planner",
        route_tool,
        {
            "calculator_node": "calculator_node",
            "weather_node": "weather_node",
            "kb_node": "kb_node",
        },
    )
    builder.add_edge("calculator_node", "responder")
    builder.add_edge("weather_node", "responder")
    builder.add_edge("kb_node", "responder")
    builder.add_edge("responder", END)

    graph = builder.compile()

    demo_questions = [
        "12 * (3 + 1)",
        "上海明天天气怎么样？",
        "LangGraph 适合解决哪些问题？",
    ]

    for question in demo_questions:
        print("\n===== 新问题 =====")
        print("用户输入：", question)
        result = graph.invoke(
            {
                "question": question,
                "tool_name": "kb",
                "tool_input": "",
                "tool_result": "",
                "answer": "",
            }
        )
        print(result["answer"])


if __name__ == "__main__":
    main()
