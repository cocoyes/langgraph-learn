import os
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from enums import ConfigKey, DefaultValue

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from common.deepseek_timeouts import load_connect_read_timeouts


@dataclass
class AppConfig:
    deepseek_api_key: str
    deepseek_base_url: str
    deepseek_model: str
    deepseek_thinking_type: str
    deepseek_connect_timeout_seconds: int
    deepseek_read_timeout_seconds: int
    deepseek_max_retries: int
    db_path: str
    max_rewrite_rounds: int


def load_config() -> AppConfig:
    load_dotenv()
    max_rewrite = int(
        os.getenv(ConfigKey.MAX_REWRITE_ROUNDS.value, DefaultValue.MAX_REWRITE_ROUNDS.value)
    )
    raw_thinking_type = os.getenv(
        ConfigKey.DEEPSEEK_THINKING_TYPE.value, DefaultValue.DEEPSEEK_THINKING_TYPE.value
    ).strip().lower()
    normalized_thinking_type = (
        raw_thinking_type if raw_thinking_type in ("enabled", "disabled") else "disabled"
    )
    default_connect = int(DefaultValue.DEEPSEEK_CONNECT_TIMEOUT_SECONDS.value)
    default_read = int(DefaultValue.DEEPSEEK_READ_TIMEOUT_SECONDS.value)
    connect_s, read_s = load_connect_read_timeouts(
        default_connect=default_connect,
        default_read=default_read,
    )
    max_retries = int(
        os.getenv(
            ConfigKey.DEEPSEEK_MAX_RETRIES.value,
            DefaultValue.DEEPSEEK_MAX_RETRIES.value,
        ).strip()
    )

    return AppConfig(
        deepseek_api_key=os.getenv(ConfigKey.DEEPSEEK_API_KEY.value, "").strip(),
        deepseek_base_url=os.getenv(
            ConfigKey.DEEPSEEK_BASE_URL.value, DefaultValue.DEEPSEEK_BASE_URL.value
        ).strip(),
        deepseek_model=os.getenv(ConfigKey.DEEPSEEK_MODEL.value, DefaultValue.DEEPSEEK_MODEL.value).strip(),
        deepseek_thinking_type=normalized_thinking_type,
        deepseek_connect_timeout_seconds=connect_s,
        deepseek_read_timeout_seconds=read_s,
        deepseek_max_retries=max_retries if max_retries >= 0 else 1,
        db_path=os.getenv(ConfigKey.DEMO_DB_PATH.value, DefaultValue.DEMO_DB_PATH.value).strip(),
        max_rewrite_rounds=max_rewrite if max_rewrite >= 0 else int(DefaultValue.MAX_REWRITE_ROUNDS.value),
    )
