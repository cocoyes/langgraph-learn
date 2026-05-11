import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from common.deepseek_langchain_client import DeepSeekLangChainClient


class DeepSeekClient(DeepSeekLangChainClient):
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        thinking_type: str,
        connect_timeout_seconds: int,
        read_timeout_seconds: int,
        max_retries: int,
    ):
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            model=model,
            thinking_type=thinking_type,
            logger_name="stage13.deepseek",
            connect_timeout_seconds=connect_timeout_seconds,
            read_timeout_seconds=read_timeout_seconds,
            max_retries=max_retries,
        )
