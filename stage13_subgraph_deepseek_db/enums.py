from enum import Enum


class IntentType(str, Enum):
    LEARNING = "learning"
    CODING = "coding"
    ANALYSIS = "analysis"


class RouteType(str, Enum):
    RESEARCH_AND_WRITE = "research_and_write"
    DIRECT_WRITE = "direct_write"


class QualityDecision(str, Enum):
    PASS = "pass"
    REWRITE = "rewrite"


class ConfigKey(str, Enum):
    DEEPSEEK_API_KEY = "DEEPSEEK_API_KEY"
    DEEPSEEK_BASE_URL = "DEEPSEEK_BASE_URL"
    DEEPSEEK_MODEL = "DEEPSEEK_MODEL"
    DEEPSEEK_THINKING_TYPE = "DEEPSEEK_THINKING_TYPE"
    DEEPSEEK_CONNECT_TIMEOUT_SECONDS = "DEEPSEEK_CONNECT_TIMEOUT_SECONDS"
    DEEPSEEK_READ_TIMEOUT_SECONDS = "DEEPSEEK_READ_TIMEOUT_SECONDS"
    DEEPSEEK_TIMEOUT_SECONDS = "DEEPSEEK_TIMEOUT_SECONDS"
    DEEPSEEK_MAX_RETRIES = "DEEPSEEK_MAX_RETRIES"
    DEMO_DB_PATH = "DEMO_DB_PATH"
    MAX_REWRITE_ROUNDS = "MAX_REWRITE_ROUNDS"


class DefaultValue(str, Enum):
    DEEPSEEK_BASE_URL = "https://api.deepseek.com"
    DEEPSEEK_MODEL = "deepseek-chat"
    DEEPSEEK_THINKING_TYPE = "disabled"
    DEEPSEEK_CONNECT_TIMEOUT_SECONDS = "15"
    DEEPSEEK_READ_TIMEOUT_SECONDS = "120"
    DEEPSEEK_MAX_RETRIES = "1"
    DEMO_DB_PATH = "stage13_subgraph_deepseek_db/learning_runs.db"
    MAX_REWRITE_ROUNDS = "2"
