import os


def load_connect_read_timeouts(
    default_connect: int = 15,
    default_read: int = 120,
) -> tuple[int, int]:
    """解析 DeepSeek HTTP 超时：连接与读取分开，避免 LLM 生成触发 ReadTimeout。

    优先级：DEEPSEEK_READ_TIMEOUT_SECONDS > DEEPSEEK_TIMEOUT_SECONDS（兼容旧名）> default_read
    """
    raw_connect = os.getenv("DEEPSEEK_CONNECT_TIMEOUT_SECONDS", str(default_connect)).strip()
    connect = int(raw_connect) if raw_connect else default_connect

    read_raw = os.getenv("DEEPSEEK_READ_TIMEOUT_SECONDS")
    legacy = os.getenv("DEEPSEEK_TIMEOUT_SECONDS")
    if read_raw is not None and str(read_raw).strip() != "":
        read = int(str(read_raw).strip())
    elif legacy is not None and str(legacy).strip() != "":
        read = int(str(legacy).strip())
    else:
        read = default_read

    return max(1, connect), max(1, read)
