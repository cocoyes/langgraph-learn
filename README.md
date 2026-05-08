# LangGraph 分阶段学习示例

这个项目按“从易到难”拆分为 8 个可运行阶段，统一使用仓库根目录的 `requirements.txt`。

## 目录结构

- `stage1_linear_graph`：最基础的线性工作流
- `stage2_conditional_routing`：条件路由与分支执行
- `stage3_parallel_merge`：并行节点与结果聚合
- `stage4_memory_chatbot`：带持久化记忆的多轮对话
- `stage5_loop_reflection`：生成-评审-修订的循环反思流程
- `stage6_tool_calling`：规划选工具并统一回复的工具调用流程
- `stage7_retry_fallback`：失败重试与降级兜底流程
- `stage8_human_approval`：人工审批、修订回路与执行终止流程

## 运行方式（每个阶段都一样）

在仓库根目录执行一次依赖安装后，再进入对应阶段目录运行：

```bash
python3 -m venv .venv
source .venv/bin/activate 或 windows下  .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd stage1_linear_graph
python app.py
```

> 建议按阶段顺序学习：1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8。
