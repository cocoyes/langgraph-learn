# 阶段 3：并行与聚合（Parallel + Merge）

这个阶段演示如何让同一份状态并行流向多个节点，再将结果聚合成最终摘要：

```text
           ┌──────────────> core_concept ─┐
START ─────┼──────────────> use_case     ─┼─> summarize_node -> END
           └──────────────> use_case2    ─┘
```

## 学习目标

- 理解一个状态如何从 `START` 并行触发多个节点
- 理解 `Annotated` + 自定义 reducer 的合并机制
- 学会把并行结果汇总成最终输出

## 运行

```bash
python app.py
```

## 核心概念

本阶段重点是“并行执行 + 状态聚合”：

| 概念 | 作用 |
|---|---|
| Parallel Branches | 同一份状态同时进入多个节点 |
| Reducer | 定义并行分支返回值如何合并 |
| Merge Node | 消费聚合后的状态生成最终结果 |

## State（状态）

状态结构：

```python
class GraphState(TypedDict):
    topic: str
    notes: Annotated[list[str], smart_merge]
    summary: str
```

字段说明：

| 字段 | 作用 |
|---|---|
| topic | 当前主题（如 `LangGraph`） |
| notes | 并行节点收集到的要点列表 |
| summary | 基于 `notes` 生成的最终摘要 |

关键点：

- `notes` 使用 `Annotated[list[str], smart_merge]`
- 这表示当多个节点同时返回 `notes` 时，LangGraph 会调用 `smart_merge` 进行合并

## 自定义 reducer（smart_merge）

```python
def smart_merge(old: list[str], new: list[str]) -> list[str]:
    merged = old + new
    merged = list(dict.fromkeys(merged))
    merged = [x for x in merged if x.strip()]
    return merged
```

合并策略：

- 先拼接旧值和新值
- 再去重（保持出现顺序）
- 过滤空字符串和全空白值

这样可以避免并行分支产生重复或空内容。

## 并行采集节点

三个分支节点都基于 `topic` 生成不同 `notes`：

```python
def collect_core_concept(state: GraphState) -> GraphState:
    topic = state["topic"]
    return {"notes": [f"{topic} 核心：基于有向图编排节点与状态流转。"]}

def collect_use_case(state: GraphState) -> GraphState:
    topic = state["topic"]
    return {"notes": [f"{topic} 场景：适合多步骤 Agent、分支逻辑、可恢复执行流程。"]}

def collect_use_case2(state: GraphState) -> GraphState:
    topic = state["topic"]
    return {"notes": [f"{topic} 场景2：适合多步骤 Agent、分支逻辑、可恢复执行流程。2"]}
```

共同特征：

- 输入同一份 `state`
- 各自返回 `notes` 的增量内容
- 不直接处理 `summary`

## 汇总节点（Merge Node）

```python
def build_summary(state: GraphState) -> GraphState:
    summary = "；".join(state["notes"])
    return {"summary": summary}
```

说明：

- 该节点接收已经聚合完成的 `notes`
- 使用分号连接后写入 `summary`

## 创建并连接工作流

```python
builder = StateGraph(GraphState)
builder.add_node("core_concept", collect_core_concept)
builder.add_node("use_case", collect_use_case)
builder.add_node("use_case2", collect_use_case2)
builder.add_node("summarize_node", build_summary)

builder.add_edge(START, "core_concept")
builder.add_edge(START, "use_case")
builder.add_edge(START, "use_case2")
builder.add_edge("core_concept", "summarize_node")
builder.add_edge("use_case", "summarize_node")
builder.add_edge("use_case2", "summarize_node")
builder.add_edge("summarize_node", END)
```

关键点：

- 从 `START` 到多个节点的边，表示并行分发
- 多个分支都汇入 `summarize_node`
- 汇入过程会触发 `notes` 的 reducer 合并

## 执行示例

执行：

```python
final_state = graph.invoke({"topic": "LangGraph", "notes": [], "summary": ""})
```

打印：

```python
print("并行收集结果：")
for item in final_state["notes"]:
    print("-", item)
print("最终摘要：", final_state["summary"])
```

示例输出（结构）：

```text
并行收集结果：
- LangGraph 核心：基于有向图编排节点与状态流转。
- LangGraph 场景：适合多步骤 Agent、分支逻辑、可恢复执行流程。
- LangGraph 场景2：适合多步骤 Agent、分支逻辑、可恢复执行流程。2
最终摘要： LangGraph 核心：基于有向图编排节点与状态流转。；LangGraph 场景：适合多步骤 Agent、分支逻辑、可恢复执行流程。；LangGraph 场景2：适合多步骤 Agent、分支逻辑、可恢复执行流程。2
```

## 状态流转过程

初始状态：

```python
{
    "topic": "LangGraph",
    "notes": [],
    "summary": ""
}
```

三个并行分支各自返回（示意）：

```python
{"notes": ["LangGraph 核心：..."]}
{"notes": ["LangGraph 场景：..."]}
{"notes": ["LangGraph 场景2：..."]}
```

`smart_merge` 聚合后：

```python
{
    "notes": [
        "LangGraph 核心：基于有向图编排节点与状态流转。",
        "LangGraph 场景：适合多步骤 Agent、分支逻辑、可恢复执行流程。",
        "LangGraph 场景2：适合多步骤 Agent、分支逻辑、可恢复执行流程。2"
    ]
}
```

`summarize_node` 写入 `summary` 后得到最终状态（核心字段）：

```python
{
    "topic": "LangGraph",
    "notes": [...],
    "summary": "LangGraph 核心：...；LangGraph 场景：...；LangGraph 场景2：..."
}
```

## 本阶段收获

通过这个示例，你已经掌握：

- 如何配置并行分支（一个起点连接多个节点）
- 如何用 `Annotated` 为字段声明合并策略
- 如何通过自定义 reducer 控制并行结果聚合质量
- 如何在汇总节点中消费聚合后的状态生成最终输出
