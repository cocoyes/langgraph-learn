# LangGraph 分阶段学习示例

这个项目按“从易到难”拆分为 4 个可运行阶段，每个阶段都有独立的 `requirements.txt`，方便你逐步学习和单独安装依赖。

## 目录结构

- `stage1_linear_graph`：最基础的线性工作流
- `stage2_conditional_routing`：条件路由与分支执行
- `stage3_parallel_merge`：并行节点与结果聚合
- `stage4_memory_chatbot`：带持久化记忆的多轮对话

## 运行方式（每个阶段都一样）

进入对应目录后执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

> 建议按阶段顺序学习：1 -> 2 -> 3 -> 4。
