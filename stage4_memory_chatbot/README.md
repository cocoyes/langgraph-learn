# 阶段 4：会话记忆（Memory Chatbot）

这个阶段演示如何让 LangGraph 在多轮对话中“记住历史消息”：

```text
同一 thread_id：
第 1 次 invoke -> 写入历史
第 2 次 invoke -> 自动带上历史 -> 再生成回复
```

## 学习目标

- 理解 `MessagesState` 的消息状态结构
- 理解 `MemorySaver` + `thread_id` 的会话持久化方式
- 学会在多轮调用中读取历史上下文

## 运行

```bash
python app.py
```

## 核心概念

本阶段重点是“多轮记忆”：

| 概念 | 作用 |
|---|---|
| MessagesState | 标准消息状态，包含 `messages` 列表 |
| Checkpointer | 保存与恢复会话状态 |
| thread_id | 会话隔离键；同一 `thread_id` 共享历史 |

## State（状态）

本示例直接使用内置的 `MessagesState`，其核心字段是：

```python
{
    "messages": [HumanMessage(...), AIMessage(...), ...]
}
```

说明：

- 每次节点返回新的消息增量
- LangGraph 会把新消息追加到历史消息中

## 会话节点（assistant_node）

节点实现：

```python
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
```

逻辑说明：

- 倒序扫描 `messages`，找到最近一条用户消息
- 统计当前会话消息总数（包含历史轮次）
- 返回一条新的 `AIMessage` 作为回复

## 创建并连接工作流

```python
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant_node)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)
```

这是一个单节点聊天图，但状态由消息序列驱动。

## 持久化记忆配置

```python
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
config = {"configurable": {"thread_id": "demo-user"}}
```

关键点：

- `MemorySaver()`：提供内存级会话存储
- `compile(checkpointer=...)`：启用状态持久化能力
- `thread_id`：指定会话身份
  - 同一个 `thread_id`：读取并续写同一段历史
  - 不同 `thread_id`：历史相互隔离

## 多轮调用示例

第一次提问：

```python
first = graph.invoke(
    {"messages": [HumanMessage(content="你好，我是 LangGraph 新手")]},
    config=config
)
```

第二次提问（使用同一个 `thread_id`）：

```python
second = graph.invoke(
    {"messages": [HumanMessage(content="你还记得我是谁吗？")]},
    config=config
)
```

重点：

- 第二次调用只传入“本轮新消息”
- 历史消息由 checkpointer 自动补齐

## 预期输出（示意）

```text
===== 第一次提问 =====
HumanMessage : 你好，我是 LangGraph 新手
AIMessage : 我记住了你刚才说的：你好，我是 LangGraph 新手。当前会话消息总数（含历史）是：1。

===== 第二次提问（同一 thread_id，会带上历史） =====
HumanMessage : 你好，我是 LangGraph 新手
AIMessage : 我记住了你刚才说的：你好，我是 LangGraph 新手。当前会话消息总数（含历史）是：1。
HumanMessage : 你还记得我是谁吗？
AIMessage : 我记住了你刚才说的：你还记得我是谁吗？当前会话消息总数（含历史）是：3。
```

> 实际输出顺序与消息数量会随实现细节略有差异，但核心现象是：第二次调用可读取第一次历史。

## 状态流转过程

第一次调用初始输入：

```python
{
    "messages": [HumanMessage("你好，我是 LangGraph 新手")]
}
```

节点返回增量：

```python
{
    "messages": [AIMessage("我记住了你刚才说的：你好，我是 LangGraph 新手。当前会话消息总数（含历史）是：1。")]
}
```

第二次调用时，框架会自动还原历史后再追加新输入，形成更长的 `messages` 序列，节点由此实现“记忆感”回复。

## 本阶段收获

通过这个示例，你已经掌握：

- 如何使用 `MessagesState` 构建对话状态
- 如何接入 `MemorySaver` 实现多轮会话记忆
- 如何通过 `thread_id` 控制会话隔离与续写
- 如何在节点中读取历史消息并生成上下文感知回复
