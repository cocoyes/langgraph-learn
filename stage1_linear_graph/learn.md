# LangGraph 入门示例代码说明

---

# 一、代码整体作用

这段代码演示了一个最简单的 LangGraph 工作流：

```text
START
  ↓
process
  ↓
END
```

功能：

- 接收用户输入
- 处理字符串
- 输出结果

---

# 二、核心概念

LangGraph 最核心的三个概念：

| 概念 | 作用 |
|---|---|
| State | 全局状态数据 |
| Node | 一个处理节点 |
| Edge | 节点之间的连接关系 |

---

# 三、State（状态）

## 定义状态结构

```python
class GraphState(TypedDict):
    user_input: str
    result: str
```

这里使用 `TypedDict` 定义整个工作流中的共享状态。

等价于：

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

---

# 四、Node（节点）

## 定义处理节点

```python
def process_input(state: GraphState) -> GraphState:
```

这是一个 LangGraph 节点函数。

特点：

- 输入：当前 state
- 输出：更新后的 state

---

## 节点内部逻辑

```python
text = state["user_input"].strip()
```

读取用户输入并去除首尾空格。

---

```python
output = f"你输入的是：{text}（长度：{len(text)}）"
```

生成输出字符串。

---

```python
return {"result": output}
```

返回新的状态字段。

注意：

这里只返回修改的字段即可。

LangGraph 会自动合并：

```python
原 state:
{
    "user_input": "LangGraph 入门",
    "result": ""
}
```

与：

```python
{
    "result": "处理结果"
}
```

最终得到：

```python
{
    "user_input": "LangGraph 入门",
    "result": "处理结果"
}
```

---

# 五、创建工作流

## 创建图

```python
builder = StateGraph(GraphState)
```

创建一个状态图对象。

参数：

```python
GraphState
```

表示整个图共享的数据结构。

---

# 六、注册节点

```python
builder.add_node("process", process_input)
```

含义：

| 参数 | 说明 |
|---|---|
| "process" | 节点名称 |
| process_input | 实际执行函数 |

这里：

```text
节点名：process
执行函数：process_input
```

可以理解为：

```text
流程图里的一个步骤
```

---

# 七、连接节点（Edge）

## 起点连接到 process

```python
builder.add_edge(START, "process")
```

表示：

```text
流程开始
  ↓
进入 process 节点
```

---

## process 连接到结束

```python
builder.add_edge("process", END)
```

表示：

```text
process 执行完成
  ↓
流程结束
```

---

# 八、编译工作流

```python
graph = builder.compile()
```

将定义好的流程图编译成可运行对象。

---

# 九、执行工作流

```python
final_state = graph.invoke({
    "user_input": "LangGraph 入门",
    "result": ""
})
```

这里传入初始状态。

初始 state：

```python
{
    "user_input": "LangGraph 入门",
    "result": ""
}
```

---

# 十、执行流程详解

执行顺序：

```text
1. START
2. process
3. END
```

---

## process 节点收到的 state

```python
{
    "user_input": "LangGraph 入门",
    "result": ""
}
```

---

## process 返回结果

```python
{
    "result": "你输入的是：LangGraph 入门（长度：12）"
}
```

---

## LangGraph 自动合并 state

最终 state：

```python
{
    "user_input": "LangGraph 入门",
    "result": "你输入的是：LangGraph 入门（长度：12）"
}
```

---

# 十一、最终输出

```python
print("运行结果：", final_state["result"])
```

输出：

```text
运行结果： 你输入的是：LangGraph 入门（长度：12）
```

---

# 十二、整体执行流程图

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

---

# 十三、这个 Demo 学会了什么

通过这个例子，你已经掌握：

## 1. StateGraph 的基本使用

```python
StateGraph(GraphState)
```

---

## 2. 节点注册

```python
add_node()
```

---

## 3. 节点连接

```python
add_edge()
```

---

## 4. 工作流执行

```python
graph.invoke()
```

---

## 5. State 自动流转机制

LangGraph 的核心：

```text
State 在节点之间自动传递
```

每个节点：

- 读取 state
- 修改 state
- 返回更新字段

---

```