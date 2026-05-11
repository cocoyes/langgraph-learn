# 阶段 10：子图路由（Routing Between Subgraphs）

在理解子图概念后，这个阶段学习“怎么在多个子图之间路由”。

## 你会学到

- 先路由，再进入不同子图
- 子图之间如何保持统一状态结构
- 为什么这是多 Agent/多策略系统的基础形态

## 流程

```text
START -> route_node
           ├── fast_flow(子图)
           └── deep_flow(子图)
        -> answer_node -> END
```

## 运行

```bash
cd stage10_subgraph_routing
python app.py
```
