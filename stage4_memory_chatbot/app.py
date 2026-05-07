from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph


def assistant_node(state: MessagesState) -> MessagesState:
    last_human_text = ""
    for message in reversed(state["messages"]):
        if isinstance(message, HumanMessage):
            last_human_text = message.content
            break

    history_count = len(state["messages"])
    reply = (
        f"我记住了你刚才说的：{last_human_text}。"
        f"当前会话消息总数（含历史）是：{history_count}。"
    )
    return {"messages": [AIMessage(content=reply)]}


def main() -> None:
    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant_node)
    builder.add_edge(START, "assistant")
    builder.add_edge("assistant", END)

    checkpointer = MemorySaver()
    graph = builder.compile(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "demo-user"}}

    print("===== 第一次提问 =====")
    first = graph.invoke({"messages": [HumanMessage(content="你好，我是 LangGraph 新手")]}, config=config)
    for msg in first["messages"]:
        print(type(msg).__name__, ":", msg.content)

    print("\n===== 第二次提问（同一 thread_id，会带上历史） =====")
    second = graph.invoke({"messages": [HumanMessage(content="你还记得我是谁吗？")]}, config=config)
    for msg in second["messages"]:
        print(type(msg).__name__, ":", msg.content)


if __name__ == "__main__":
    main()
