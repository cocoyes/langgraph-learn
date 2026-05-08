# 阶段 2：条件路由（Conditional Routing）

这个阶段演示如何在 LangGraph 中根据输入内容进行动态分支：

```text
START
  ↓
router
  ├── short -> short_answer -> END
  └── long  -> long_answer  -> END
```

## 学习目标

- 理解如何定义路由节点
- 理解 `add_conditional_edges()` 的用法
- 学会让同一状态走不同分支节点

## 运行

```bash
python app.py
```

## 核心概念

相较阶段 1，本阶段重点是“路由”：

| 概念 | 作用 |
|---|---|
| Router Node | 根据状态计算分支标记 |
| Conditional Edges | 根据分支标记跳转到不同节点 |
| Branch Node | 处理各自分支逻辑并返回结果 |

## State（状态）

状态结构：

```python
RouteType = Literal["short", "long"]

class GraphState(TypedDict):
    question: str
    route: RouteType
    answer: str
```

字段说明：

| 字段 | 作用 |
|---|---|
| question | 用户问题文本 |
| route | 路由结果（`short` 或 `long`） |
| answer | 最终回答内容 |

## 路由节点（Router Node）

路由函数：

```python
def route_question(state: GraphState) -> GraphState:
    question = state["question"].strip()
    route: RouteType = "short" if len(question) <= 12 else "long"
    return {"route": route}
```

逻辑说明：

- 读取 `question`
- 根据长度计算 `route`
- 返回 `{"route": ...}` 供后续分支使用

## 分支节点（Branch Nodes）

短问题分支：

```python
def short_answer(state: GraphState) -> GraphState:
    return {"answer": f"短问题快速回答：{state['question']}"}
```

长问题分支：

```python
def long_answer(state: GraphState) -> GraphState:
    return {"answer": f"长问题详细回答：{state['question']}。建议拆分子问题再逐步求解。"}
```

这两个节点都只更新 `answer` 字段，LangGraph 会自动和已有状态合并。

## 条件路由函数

```python
def choose_route(state: GraphState) -> RouteType:
    return state["route"]
```

这个函数用于告诉 `add_conditional_edges()` 当前应该走哪个分支。

## 创建并连接工作流

```python
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
```

关键点：

- `add_conditional_edges()` 第 3 个参数是“路由值 -> 节点名”的映射
- `router` 执行后，不再固定走某个节点，而是由 `choose_route` 决定

## 执行示例

示例输入：

```python
question = "LangGraph 和普通函数调用有什么区别？"
final_state = graph.invoke({"question": question, "route": "short", "answer": ""})
```

> 这里初始 `route` 只是占位值，真正结果会被 `route_question()` 覆盖。

输出：

```python
print("路由结果：", final_state["route"])
print("回答结果：", final_state["answer"])
```

示例结果：

```text
路由结果： long
回答结果： 长问题详细回答：LangGraph 和普通函数调用有什么区别？。建议拆分子问题再逐步求解。
```

## 状态流转过程

初始状态：

```python
{
    "question": "LangGraph 和普通函数调用有什么区别？",
    "route": "short",
    "answer": ""
}
```

`router` 执行后：

```python
{
    "route": "long"
}
```

进入 `long_answer` 后返回：

```python
{
    "answer": "长问题详细回答：LangGraph 和普通函数调用有什么区别？。建议拆分子问题再逐步求解。"
}
```

最终合并状态（核心字段）：

```python
{
    "question": "LangGraph 和普通函数调用有什么区别？",
    "route": "long",
    "answer": "长问题详细回答：LangGraph 和普通函数调用有什么区别？。建议拆分子问题再逐步求解。"
}
```

## 本阶段收获

通过这个示例，你已经掌握：

- 如何设计路由节点并写入路由结果
- 如何使用 `add_conditional_edges()` 做动态分支
- 如何让同一份 `state` 在不同路径中流转
- 如何在分支节点中分别产出结果并汇总为最终状态
