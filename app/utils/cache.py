"""JSON 檔案快取工具。"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

_cache_timestamp: str | None = None


def _ensure_data_dir():
    """確保 data 目錄存在。"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def write_cache(filename: str, data: Any) -> None:
    """將資料寫入 JSON 快取檔案。

    Args:
        filename: 快取檔案名稱。
        data: 要快取的資料。
    """
    global _cache_timestamp
    _ensure_data_dir()
    filepath = DATA_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    _cache_timestamp = datetime.now(timezone.utc).isoformat()
    logger.info("快取寫入: %s", filepath)


def read_cache(filename: str) -> Any | None:
    """讀取 JSON 快取檔案。

    Args:
        filename: 快取檔案名稱。

    Returns:
        快取資料，若檔案不存在則回傳 None。
    """
    filepath = DATA_DIR / filename
    if not filepath.exists():
        logger.debug("快取不存在: %s", filepath)
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_cache_timestamp() -> str | None:
    """取得最近一次快取寫入的時間戳。"""
    return _cache_timestamp
