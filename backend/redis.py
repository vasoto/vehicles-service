from aioredis import Redis, create_redis_pool
from .config import get_config

conf = get_config()

async def init_redis() -> Redis:
    redis = await create_redis_pool(
            conf.redis_url,
            encoding="utf-8",
            db=conf.redis_db,
        )
    return redis

