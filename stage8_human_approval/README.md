# 阶段 8：人工审批流（Human Approval Workflow）

这个阶段演示业务系统常见模式：先生成执行方案，经过审批，再决定执行、修改或终止。

```text
START -> plan -> approval
                 ├── execute -> END
                 ├── revise -> plan (循环)
                 └── stop -> END
```

## 学习目标

- 理解 Human-in-the-loop 的图建模方式
- 学会把审批结论映射为流程分支
- 学会在审批场景下控制修订次数

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
| Plan Node | 生成待审批方案 |
| Approval Node | 产出审批结论（approve/revise/reject） |
| Revision Loop | 驳回后修订并再次提交 |

## State（状态）

```python
class GraphState(TypedDict):
    requirement: str
    draft_plan: str
    revision_notes: str
    approval: Approval
    revision_count: int
    max_revisions: int
    result: str
```

## 关键流程

- `plan_node`：生成或修订方案
- `approval_node`：返回审批结果（示例里是模拟）
- `decide_after_approval`：决定执行、继续修订或终止
- `revise_node`：修订计数 +1，回到计划节点
- `execute_node/stop_node`：输出流程最终结果

## 适用场景

- 上线审批、发布审批
- 财务/合同审核
- 高风险操作前置确认

## 本阶段收获

- 你可以把人工决策点嵌入自动化图流程
- 你可以将“可审计流程”做成稳定可复现的状态机
