# 阶段 7：重试与降级（Retry + Fallback）

这个阶段演示生产里非常常见的稳定性策略：主路径失败时先重试，超过上限再降级。

```text
START -> fetch_primary
          ├── retry -> fetch_primary
          ├── fallback -> fallback_cache
          └── format -> format_response -> END
fallback_cache -> format_response
```

## 学习目标

- 理解失败重试与退出条件控制
- 学会在 LangGraph 中实现 fallback 降级路径
- 学会统一格式化响应，隔离上游抖动

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
| Retry Loop | 主链路失败后自动重试 |
| Fallback Path | 达到重试上限后走降级方案 |
| Response Formatter | 对上层暴露稳定结构 |

## State（状态）

```python
class GraphState(TypedDict):
    user_id: str
    attempts: int
    max_attempts: int
    profile: str
    error: str
    source: str
    response: str
```

## 关键流程

- `fetch_primary`：模拟主服务调用，记录失败或成功
- `decide_after_primary`：判断 `retry/fallback/format`
- `fallback_cache`：返回缓存结果作为降级数据
- `format_response`：统一拼接输出，便于上游消费

## 适用场景

- 外部 API 不稳定
- 数据库/向量库偶发超时
- 多数据源容灾编排

## 本阶段收获

- 你可以把稳定性策略显式建模到图里
- 你可以让失败路径与成功路径同样可观测、可测试
