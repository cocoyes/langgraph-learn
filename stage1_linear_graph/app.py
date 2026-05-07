from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class GraphState(TypedDict):
    user_input: str
    result: str


def process_input(state: GraphState) -> GraphState:
    text = state["user_input"].strip()
    output = f"你输入的是：{text}（长度：{len(text)}）"
    return {"result": output}


def main() -> None:
    builder = StateGraph(GraphState)
    builder.add_node("process", process_input)
    builder.add_edge(START, "process")
    builder.add_edge("process", END)

    graph = builder.compile()
    final_state = graph.invoke({"user_input": "LangGraph 入门", "result": ""})
    print("运行结果：", final_state["result"])


if __name__ == "__main__":
    main()
