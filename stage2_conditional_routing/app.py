from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


RouteType = Literal["short", "long"]


class GraphState(TypedDict):
    question: str
    route: RouteType
    answer: str


def route_question(state: GraphState) -> GraphState:
    question = state["question"].strip()
    route: RouteType = "short" if len(question) <= 12 else "long"
    return {"route": route}


def short_answer(state: GraphState) -> GraphState:
    return {"answer": f"短问题快速回答：{state['question']}"}


def long_answer(state: GraphState) -> GraphState:
    return {"answer": f"长问题详细回答：{state['question']}。建议拆分子问题再逐步求解。"}


def choose_route(state: GraphState) -> RouteType:
    return state["route"]


def main() -> None:
    builder = StateGraph(GraphState)
    builder.add_node("router", route_question)
    builder.add_node("short_answer", short_answer)
    builder.add_node("long_answer", long_answer)

    builder.add_edge(START, "router")
    builder.add_conditional_edges(
        "router",
        choose_route,
        {"short": "short_answer", "long": "long_answer"},
    )
    builder.add_edge("short_answer", END)
    builder.add_edge("long_answer", END)

    graph = builder.compile()

    question = "LangGraph 和普通函数调用有什么区别？"
    final_state = graph.invoke({"question": question, "route": "short", "answer": ""})
    print("路由结果：", final_state["route"])
    print("回答结果：", final_state["answer"])


if __name__ == "__main__":
    main()
