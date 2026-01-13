import json
import os
from typing import Any, Optional

import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/2")
KEY_PREFIX = "invoice_result:"


def _client() -> redis.Redis:
    return redis.Redis.from_url(REDIS_URL, decode_responses=True)


def save_result(task_id: str, result: Any) -> None:
    r = _client()
    r.set(f"{KEY_PREFIX}{task_id}", json.dumps(result, ensure_ascii=False))


def get_result(task_id: str) -> Optional[Any]:
    r = _client()
    raw = r.get(f"{KEY_PREFIX}{task_id}")
    if raw is None:
        return None
    return json.loads(raw)
