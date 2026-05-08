# 阶段 6：工具调用（Tool Calling）

这个阶段演示常见 Agent 模式：先规划，再选工具执行，最后整理答案。

```text
START -> planner -> (calculator | weather | kb) -> responder -> END
```

## 学习目标

- 理解工具选择（tool routing）流程
- 学会把不同工具封装为独立节点
- 学会统一汇总工具输出并返回给用户

## 运行

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
python app.py
```

## 核心概念

| 概念 | 作用 |
|---|---|
| Planner Node | 根据问题选择工具 |
| Tool Nodes | 执行具体能力（计算、天气、知识库） |
| Responder Node | 统一包装最终回答 |

## State（状态）

```python
class GraphState(TypedDict):
    question: str
    tool_name: ToolName
    tool_input: str
    tool_result: str
    answer: str
```

## 关键流程

- `planner_node`：解析问题并写入 `tool_name/tool_input`
- `route_tool`：把 `tool_name` 映射到具体节点
- `calculator_node/weather_node/kb_node`：分别执行工具逻辑
- `responder_node`：把工具结果整理成可读回答

## 适用场景

- LLM + 外部工具编排
- 多能力 Agent（检索、计算、执行）
- 函数调用（Function Calling）风格流程

## 本阶段收获

- 你可以把“决策”和“执行”解耦，提升流程可维护性
- 你可以通过条件边快速扩展新工具节点
