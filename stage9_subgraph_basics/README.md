# 阶段 9：子图基础（Subgraph Basics）

这个阶段只做一件事：先真正理解“什么是子图”。

## 你会学到

- 子图本质：一段可复用的小流程
- 父图如何把子图当成一个普通节点使用
- 为什么生产项目会大量使用子图（解耦、复用、可测试）

## 流程

```text
父图：
START -> planning_node -> drafting_flow(子图) -> review_node -> finalize_node -> END

子图 drafting_flow：
START -> collect_context_node -> write_draft_node -> END
```

## 运行

```bash
cd stage9_subgraph_basics
python app.py
```
