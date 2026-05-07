# 阶段 4：会话记忆（Memory Chatbot）

## 学习目标

- 理解 `MessagesState` 的消息状态结构
- 理解 `MemorySaver` + `thread_id` 的会话持久化方式
- 学会在多轮调用中读取历史上下文

## 运行

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
