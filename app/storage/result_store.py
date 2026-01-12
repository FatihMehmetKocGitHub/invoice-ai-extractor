import json
import redis
from typing import Any, Dict, Optional

class ResultStore:
    def __init__(self, redis_url: str):
        self.r = redis.Redis.from_url(redis_url, decode_responses=True)

    def set(self, key: str, value: Dict[str, Any], ttl: int = 3600) -> None:
        self.r.setex(key, ttl, json.dumps(value))

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        v = self.r.get(key)
        return json.loads(v) if v else None
