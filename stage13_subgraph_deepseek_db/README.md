# 阶段 13：子图 + DeepSeek + 数据库存档（更贴近生产）

这个阶段把前 8 个教学示例升级为一个更像真实项目的结构，重点演示：

- 父图编排 + 子图组合（subgraph composition）
- 真实大模型调用（LangChain `ChatOpenAI` + DeepSeek OpenAI 兼容接口）
- 数据库存档（SQLite，可替换到 MySQL/PostgreSQL）
- 节点拆分到 `nodes/`，降低耦合，便于复用
- 质量评审 + 重写循环（质量门禁）

---

## 目录结构

```text
stage13_subgraph_deepseek_db/
├── app.py                    # 入口
├── config.py                 # 环境变量配置
├── enums.py                  # 枚举与默认值
├── graph.py                  # 父图 + 子图装配
├── state.py                  # 图状态定义
├── llm/
│   └── deepseek_client.py    # LangChain DeepSeek 客户端封装
├── db/
│   └── repository.py         # 数据存取（Repository）
└── nodes/
    ├── execution.py          # research / writer 节点
    ├── helpers.py            # 公共逻辑（打分解析、路由）
    ├── intake.py             # 意图识别入口节点
    ├── persist.py            # 落库节点
    ├── planning.py           # 规划节点
    ├── prompts.py            # Prompt 常量
    └── review.py             # 评审节点与循环控制
```

---

## 流程图（父图）

```text
START
  -> intake
  -> planning_flow (子图)
  -> 条件路由
      ├─ research_and_write_flow (子图)
      └─ direct_write_flow (子图)
  -> review
      ├─ pass    -> finalize -> persist -> END
      └─ rewrite -> rewrite_round -> planning_flow (循环)
```

---

## 子图拆分示例

1. `planning_flow` 子图：只做方案规划
2. `research_and_write_flow` 子图：调研 + 生成
3. `direct_write_flow` 子图：无需调研时直接生成

把复杂流程拆成子图后，后续可以单独替换任一子图实现，而不必重写整张大图。

---

## 环境变量

可先复制 `stage13_subgraph_deepseek_db/.env.example` 到仓库根目录 `.env`，再按需修改：

```bash
DEEPSEEK_API_KEY=你的deepseek_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_THINKING_TYPE=disabled
DEEPSEEK_CONNECT_TIMEOUT_SECONDS=15
DEEPSEEK_READ_TIMEOUT_SECONDS=120
DEEPSEEK_MAX_RETRIES=1
DEMO_DB_PATH=stage13_subgraph_deepseek_db/learning_runs.db
MAX_REWRITE_ROUNDS=2
```

说明：

- 未配置 `DEEPSEEK_API_KEY` 时会自动走 Mock 输出，保证你能先跑通流程
- `DEMO_DB_PATH` 默认 SQLite 文件路径，便于本地学习
- 若出现 `httpcore.ReadTimeout`，请增大 `DEEPSEEK_READ_TIMEOUT_SECONDS`；未设置时可用 `DEEPSEEK_TIMEOUT_SECONDS` 作为读超时回退

---

## 运行方式

```bash
cd stage13_subgraph_deepseek_db
python app.py
```

运行后会输出：

- intent（意图分类）
- route（执行路由）
- quality_score（评审分）
- persisted_id（数据库记录 ID）
- final_answer（最终产物）
- recent runs（最近历史记录）

---

## 你可以继续扩展什么

1. 把 `db/repository.py` 改成 SQLAlchemy + MySQL 版本
2. 增加 `tool` 子图：RAG 检索、Web 搜索、代码执行
3. 增加人工审批节点（结合 stage8）
4. 增加可观测性：节点耗时、token 消耗、失败率
5. 增加 API 化封装：FastAPI + `/invoke` + `/history`

---

## 生产化实践建议

- **低耦合**：节点只做单一职责，通过 `state` 传递数据
- **可替换性**：LLM、DB、Prompt、路由策略都通过模块独立
- **容错优先**：数据库失败不抛异常，返回 `None` 或 `[]` 保持主流程可用
- **可追踪**：每次执行都落库，便于回放与评估
- **可演进**：先本地 SQLite 跑通，再切换真实外部服务
