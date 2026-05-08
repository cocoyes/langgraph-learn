# 阶段 1：线性流程（Linear Graph）

这个阶段演示一个最简单的 LangGraph 工作流：

```text
START
  ↓
process
  ↓
END
```

## 学习目标

- 理解 `StateGraph` 的基本构建方式
- 理解 `START -> 节点 -> END` 的最简单流程
- 学会通过 `graph.invoke()` 触发执行

## 运行

```bash
python app.py
```

## 核心概念

LangGraph 最核心的三个概念：

| 概念 | 作用 |
|---|---|
| State | 全局状态数据 |
| Node | 一个处理节点 |
| Edge | 节点之间的连接关系 |

## State（状态）

状态结构：

```python
class GraphState(TypedDict):
    user_input: str
    result: str
```

等价于一个共享字典：

```python
{
    "user_input": "",
    "result": ""
}
```

字段说明：

| 字段 | 作用 |
|---|---|
| user_input | 用户输入内容 |
| result | 节点处理后的结果 |

## Node（节点）

节点函数定义：

```python
def process_input(state: GraphState) -> GraphState:
```

特点：

- 输入：当前 `state`
- 输出：更新后的 `state`

节点核心逻辑：

```python
text = state["user_input"].strip()
output = f"你输入的是：{text}（长度：{len(text)}）"
return {"result": output}
```

说明：

- 节点只需要返回修改过的字段
- LangGraph 会自动把返回字段与原始 `state` 合并

## 创建并连接工作流

```python
builder = StateGraph(GraphState)
builder.add_node("process", process_input)
builder.add_edge(START, "process")
builder.add_edge("process", END)
graph = builder.compile()
```

含义：

- `add_node("process", process_input)`：注册节点
- `add_edge(START, "process")`：定义起点到节点
- `add_edge("process", END)`：定义节点到终点
- `compile()`：将流程图编译为可执行对象

## 执行示例

执行：

```python
final_state = graph.invoke({
    "user_input": "LangGraph 入门",
    "result": ""
})
print("运行结果：", final_state["result"])
```

执行顺序：

```text
1. START
2. process
3. END
```

输出示例：

```text
运行结果： 你输入的是：LangGraph 入门（长度：12）
```

## 状态流转过程

`process` 节点收到的状态：

```python
{
    "user_input": "LangGraph 入门",
    "result": ""
}
```

`process` 节点返回：

```python
{
    "result": "你输入的是：LangGraph 入门（长度：12）"
}
```

自动合并后的最终状态：

```python
{
    "user_input": "LangGraph 入门",
    "result": "你输入的是：LangGraph 入门（长度：12）"
}
```

## 整体流程图

```text
初始 State
{
    "user_input": "LangGraph 入门",
    "result": ""
}

        │
        ▼

START
        │
        ▼

process 节点
(process_input 函数)

        │
        ▼

更新 result

        │
        ▼

END

        │
        ▼

最终输出
```

## 本阶段收获

通过这个示例，你已经掌握：

- `StateGraph(GraphState)`：创建状态图
- `add_node()`：注册节点
- `add_edge()`：连接节点
- `graph.invoke()`：执行工作流
- `state` 在节点间自动流转与合并的机制
