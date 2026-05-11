# 阶段 12：数据库持久化工作流（Persistence）

这个阶段把“可运行答案”升级到“可追踪执行”。

## 你会学到

- 如何使用 LangChain `ChatOpenAI` 对接 DeepSeek
- 节点内如何调用 Repository 落库
- 如何查询最近历史并回显
- 为什么生产系统必须保留运行轨迹

## 流程

```text
START -> answer_node -> persist_node -> history_node -> END
```

## 运行

可先复制 `stage12_persistence_workflow/.env.example` 到仓库根目录 `.env`，再按需修改：

```bash
DEEPSEEK_API_KEY=你的deepseek_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_THINKING_TYPE=disabled
DEEPSEEK_CONNECT_TIMEOUT_SECONDS=15
DEEPSEEK_READ_TIMEOUT_SECONDS=120
DEEPSEEK_MAX_RETRIES=1
STAGE12_DB_PATH=stage12_persistence_workflow/stage12_runs.db
```

未配置 `DEEPSEEK_API_KEY` 时自动走 Mock 输出，保证流程可跑。

若出现 `httpcore.ReadTimeout`，说明**读超时**：请增大 `DEEPSEEK_READ_TIMEOUT_SECONDS`（LLM 生成常需更久）。未设置 `DEEPSEEK_READ_TIMEOUT_SECONDS` 时，可读 `DEEPSEEK_TIMEOUT_SECONDS` 作为回退。

```bash
cd stage12_persistence_workflow
python app.py
```
