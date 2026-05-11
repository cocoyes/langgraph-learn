# 阶段 11：真实 DeepSeek 接入（不含数据库）

这个阶段只关注一件事：把子图和 LangChain 模型调用结合起来。

## 你会学到

- 如何使用 LangChain `ChatOpenAI` 对接 DeepSeek（OpenAI 兼容接口）
- 未配置 Key 时如何平滑降级到 Mock
- 先 plan 再 answer 的子图执行方式

## 环境变量

可先复制 `stage11_deepseek_subgraph/.env.example` 到仓库根目录 `.env`：

```bash
DEEPSEEK_API_KEY=你的key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_THINKING_TYPE=disabled
DEEPSEEK_CONNECT_TIMEOUT_SECONDS=15
DEEPSEEK_READ_TIMEOUT_SECONDS=120
DEEPSEEK_MAX_RETRIES=1
```

说明：`httpcore.ReadTimeout` 表示**读超时**（连接已建立，但模型在限定时间内未返回完整响应）。LLM 生成常需数十秒，请把 `DEEPSEEK_READ_TIMEOUT_SECONDS` 调大。旧环境变量 `DEEPSEEK_TIMEOUT_SECONDS` 仍可作为读超时回退（当未设置 `DEEPSEEK_READ_TIMEOUT_SECONDS` 时）。

## 运行

```bash
cd stage11_deepseek_subgraph
python app.py
```
