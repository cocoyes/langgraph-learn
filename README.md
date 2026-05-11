# LangGraph 分阶段学习示例（循序渐进版）

这个项目按“从易到难 + 从教学到真实项目”拆分阶段。  
前 1-8 阶段打基础；从 9 开始，每一阶段只新增一组核心能力，避免把知识点一次性塞进一个 stage。

---

## 学习路线总览

### 基础阶段（1-4）

- `stage1_linear_graph`：最基础的线性工作流
- `stage2_conditional_routing`：条件路由与分支执行
- `stage3_parallel_merge`：并行节点与结果聚合
- `stage4_memory_chatbot`：带持久化记忆的多轮对话

### 进阶阶段（5-8）

- `stage5_loop_reflection`：生成-评审-修订的循环反思流程
- `stage6_tool_calling`：规划选工具并统一回复的工具调用流程
- `stage7_retry_fallback`：失败重试与降级兜底流程
- `stage8_human_approval`：人工审批、修订回路与执行终止流程

### 生产化延伸（9-12）

- `stage9_subgraph_basics`：子图概念与父图挂载方式
- `stage10_subgraph_routing`：多子图路由选择与统一状态
- `stage11_deepseek_subgraph`：LangChain `ChatOpenAI` 接入 DeepSeek（含 mock 降级）
- `stage12_persistence_workflow`：LangChain 生成 + 数据库持久化与历史回放

### 综合实战（可选）

- `stage13_subgraph_deepseek_db`：将子图 + LangChain 模型 + 持久化 + 评审循环合并到完整工程样例

---

## 为什么拆成 9-12 阶段

很多教程只演示“一个文件里写完整张图”，便于入门，但真实项目会遇到：

- 节点逻辑逐步膨胀，难维护
- 模型调用、数据库访问、路由策略耦合在一起
- 缺乏评估闭环（质量门禁、执行历史）
- 缺乏可替换能力（换模型、换 DB、换子流程）

因此从现在开始按“一个阶段一个核心增量”推进，更利于吸收与实战迁移。

---

## 统一安装与运行

在仓库根目录执行一次依赖安装后，再进入各阶段目录运行：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd stage1_linear_graph
python app.py
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd stage1_linear_graph
python app.py
```

---

## 9-12 阶段快速开始

### Stage 9：先学子图概念

```bash
cd stage9_subgraph_basics
python app.py
```

### Stage 10：再学子图路由

```bash
cd stage10_subgraph_routing
python app.py
```

### Stage 11：接入 DeepSeek

在仓库根目录 `.env` 配置：

```bash
DEEPSEEK_API_KEY=你的deepseek_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

然后运行：

```bash
cd stage11_deepseek_subgraph
python app.py
```

### Stage 12：增加数据库持久化

```bash
cd stage12_persistence_workflow
python app.py
```

---

## 推荐学习顺序

建议顺序：`1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10 -> 11 -> 12`，最后可选学习 `13` 综合实战阶段。

每学习完一个阶段，都建议做这 3 件事：

1. 画出状态字段变化（输入 -> 节点更新 -> 输出）
2. 为关键节点补 1 个失败场景（超时、空结果、异常）
3. 将“硬编码逻辑”替换为可配置项（环境变量或常量）

---

## 从 Demo 走向生产的演进建议

- **节点模块化**：把 `node` 拆到 `nodes/`，每个节点保持单一职责
- **公共逻辑沉淀**：路由判断、分数解析、重试策略提炼为 helper
- **模型抽象层**：将 LLM 客户端封装在独立模块，可平滑替换模型厂商
- **持久化层**：将 DB 访问放在 repository，SQL 错误时不阻断主流程
- **子图复用**：把“规划、执行、审批、工具调用”做成可插拔子图
- **可观测性**：记录 run_id、耗时、分数、失败原因，支持回放与评估

---

## 更多 LangGraph 延伸专题（建议逐步实战）

1. **Subgraph 模板化**
   - 把“规划子图、执行子图、审批子图”做成工厂函数
   - 不同业务仅替换 prompt / tools / policy 即可复用

2. **Checkpointer + Thread 会话隔离**
   - 接入 `MemorySaver` 或数据库 checkpointer
   - 按 `thread_id` 区分会话，支持多用户并行

3. **Human-in-the-loop 升级**
   - 使用 `interrupt` 暂停图执行
   - 外部系统（Web 管理台）写回审批结果后继续执行

4. **Agent + Tool + RAG 融合**
   - 将工具调用流程与知识检索子图串联
   - 引入“检索失败兜底”和“重试降级”策略

5. **多 Agent 协作图**
   - 规划 Agent、执行 Agent、审查 Agent 分工
   - 由 Supervisor 节点进行任务分派和汇总

6. **可观测与评估**
   - 每个节点记录输入摘要、输出摘要、耗时、token
   - 建立离线评测集，对不同 prompt/模型版本做 A/B 对比

---

## 常见问题

### 1) 没有 DeepSeek Key 能学吗？

可以。先学习 Stage 9/10/12；Stage 11 未配置 Key 时会自动 Mock。

### 2) 我有自己的数据库怎么办？

先保持 `repository` 接口不变，再替换底层实现（SQLite -> MySQL/PostgreSQL）。

### 3) 为什么要子图？

子图能把复杂流程拆成“可组合单元”，对多人协作、测试、扩展和复用都更友好。
