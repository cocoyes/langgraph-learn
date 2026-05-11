import logging
import time
from typing import Optional
import os

try:
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI
except Exception:
    HumanMessage = None
    SystemMessage = None
    ChatOpenAI = None


class DeepSeekLangChainClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str = "deepseek-v4-pro",
        thinking_type: Optional[str] = None,
        logger_name: str = "deepseek_client",
        connect_timeout_seconds: int = 30,
        read_timeout_seconds: int = 300,
        max_retries: int = 2,
    ):
        self._client: Optional[ChatOpenAI] = None
        self._logger = logging.getLogger(logger_name)

        self._connect_timeout_seconds = max(1, int(connect_timeout_seconds))
        self._read_timeout_seconds = max(1, int(read_timeout_seconds))
        self._max_retries = max(0, int(max_retries))

        if ChatOpenAI is None:
            self._logger.warning(
                "langchain_openai 未安装，当前使用 Mock 模式。"
            )
            return

        if not api_key:
            self._logger.warning(
                "未配置 API KEY，当前使用 Mock 模式。"
            )
            return

        normalized_base_url = self._normalize_base_url(base_url)

        self._logger.info(
            "初始化 DeepSeek Client: model=%s, base_url=%s",
            model,
            normalized_base_url,
        )

        extra_body = {}

        print(f"thinking_type: {thinking_type}")
        print(f"extra_body: {extra_body}")
        print(f"model: {model}")
        print(f"api_key: {api_key}")
        print(f"normalized_base_url: {normalized_base_url}")
        print(f"self._read_timeout_seconds: {self._read_timeout_seconds}")
        print(f"self._max_retries: {self._max_retries}")   
        
  

        # 只有传了 thinking_type 才加
        # 很多兼容层不支持 thinking 参数
        if thinking_type:
            self._logger.info("Thinking type: %s", thinking_type)
            extra_body["thinking"] = {
                "type": thinking_type
            }

        try:
            self._client = ChatOpenAI(
                model=model,

                # 新版推荐参数
                api_key=api_key,
                base_url=normalized_base_url,

                temperature=0.3,

                # 不要传 httpx.Timeout
                # LangChain/OpenAI SDK 很多版本兼容不好
                timeout=self._read_timeout_seconds,

                max_retries=self._max_retries,

                # 有些平台不支持 thinking
                extra_body=extra_body if extra_body else None,
            )

            self._logger.info("DeepSeek Client 初始化成功。")

        except Exception:
            self._logger.exception("DeepSeek Client 初始化失败。")

    def invoke(self, system_prompt: str, user_prompt: str) -> str:
        if (
            self._client is None
            or HumanMessage is None
            or SystemMessage is None
        ):
            return (
                "【Mock】未配置 DeepSeek。\n\n"
                f"用户问题：{user_prompt}"
            )

        try:
            started = time.monotonic()

            response = self._client.invoke(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt),
                ]
            )

            elapsed_ms = int((time.monotonic() - started) * 1000)

            self._logger.info(
                "DeepSeek 调用成功，耗时 %sms。",
                elapsed_ms,
            )

            return self._to_text(response.content)

        except Exception as exc:
            self._log_exception(exc)

            return (
                "【Mock】DeepSeek 调用失败，已降级。\n\n"
                f"用户问题：{user_prompt}"
            )

    def _log_exception(self, exc: Exception) -> None:
        exc_type = type(exc).__name__

        self._logger.error(
            "DeepSeek 调用异常类型: %s",
            exc_type,
        )

        self._logger.error(
            "DeepSeek 异常详情: %s",
            repr(exc),
        )

        if self._is_read_timeout(exc):
            self._logger.error(
                (
                    "DeepSeek 读超时（ReadTimeout）。\n"
                    "说明 TCP 已连接成功，但模型长时间未返回数据。\n"
                    "可能原因：\n"
                    "1. deepseek-reasoner 推理耗时太长\n"
                    "2. thinking 参数导致思考时间过久\n"
                    "3. 代理/Nginx/Cloudflare 提前断开\n"
                    "4. 网络质量不稳定\n"
                    "5. timeout 设置过小\n"
                )
            )

        self._logger.exception("完整异常堆栈：")

    @staticmethod
    def _is_read_timeout(exc: Exception) -> bool:
        current: Optional[BaseException] = exc

        while current is not None:
            name = type(current).__name__

            if (
                "ReadTimeout" in name
                or "TimeoutError" in name
                or "APITimeoutError" in name
            ):
                return True

            current = current.__cause__

        return False

    @staticmethod
    def _normalize_base_url(base_url: str) -> str:
        """
        不再强制拼接 /v1
        因为不同 SDK / 平台行为不一致。

        推荐直接传：
        https://api.deepseek.com
        """

        return base_url.strip().rstrip("/")

    @staticmethod
    def _to_text(content: object) -> str:
        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            parts = []

            for item in content:
                text = getattr(item, "text", None)

                if text:
                    parts.append(str(text))
                    continue

                if isinstance(item, dict):
                    if "text" in item:
                        parts.append(str(item["text"]))

            return "\n".join(parts).strip()

        return str(content).strip()