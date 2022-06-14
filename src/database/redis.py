from typing import Optional

from aioredis import Redis

from src.configurator import config

# Warning: This part of the code has not been tested and may contain bugs.

__all__ = ("redis",)

redis: Optional[Redis]

if config.database.redis.url is None:
    redis = None
else:
    redis = Redis.from_url(config.database.redis.url)
