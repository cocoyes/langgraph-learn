import os
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from common.deepseek_timeouts import load_connect_read_timeouts


@dataclass
class AppConfig:
    api_key: str
    base_url: str
    model: str
    thinking_type: str
    connect_timeout_seconds: int
    read_timeout_seconds: int
    max_retries: int
    db_path: str


def load_config() -> AppConfig:
    load_dotenv()
    thinking_type = os.getenv("DEEPSEEK_THINKING_TYPE", "disabled").strip().lower()
    normalized_thinking_type = thinking_type if thinking_type in ("enabled", "disabled") else "disabled"
    connect_s, read_s = load_connect_read_timeouts(default_connect=15, default_read=120)
    max_retries = int(os.getenv("DEEPSEEK_MAX_RETRIES", "1").strip())
    return AppConfig(
        api_key=os.getenv("DEEPSEEK_API_KEY", "").strip(),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").strip(),
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat").strip(),
        thinking_type=normalized_thinking_type,
        connect_timeout_seconds=connect_s,
        read_timeout_seconds=read_s,
        max_retries=max_retries if max_retries >= 0 else 1,
        db_path=os.getenv(
            "STAGE12_DB_PATH", "stage12_persistence_workflow/stage12_runs.db"
        ).strip(),
    )
