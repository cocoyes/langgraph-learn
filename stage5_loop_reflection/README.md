# 阶段 5：循环反思（Loop + Reflection）

这个阶段演示一种常见 Agent 流程：先生成，再评审，不达标就继续迭代。

```text
START -> draft -> review
                 ├── revise -> draft (循环)
                 └── finish -> END
```

## 学习目标

- 理解 LangGraph 中如何构建循环工作流
- 学会使用评审节点驱动迭代优化
- 学会通过质量门槛和最大轮次避免死循环

## 运行

```bash
python app.py
```

## 核心概念

| 概念 | 作用 |
|---|---|
| Draft Node | 生成当前版本内容 |
| Review Node | 评分并给出反馈 |
| Loop Control | 根据评分决定继续迭代还是结束 |

## State（状态）

```python
class GraphState(TypedDict):
    topic: str
    draft: str
    feedback: str
    score: int
    iteration: int
    max_iterations: int
```

字段说明：

| 字段 | 作用 |
|---|---|
| topic | 写作主题 |
| draft | 当前草稿 |
| feedback | 评审意见 |
| score | 当前评分 |
| iteration | 当前迭代次数 |
| max_iterations | 最大允许迭代次数 |

## 节点逻辑

- `draft_content`：按轮次生成或补充草稿
- `review_content`：根据关键内容给分并输出反馈
- `revise_content`：迭代次数 +1，为下一轮草稿做准备
- `decide_next_step`：评分达标或达到上限则结束，否则继续循环

## 适用场景

- 提示词自动优化
- 代码草稿与自动评审
- 文案生成与质量控制

## 本阶段收获

- 你可以用 LangGraph 实现“生成 -> 评估 -> 改进”的闭环
- 你可以显式控制循环退出条件，保证流程可控
