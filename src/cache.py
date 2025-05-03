import redis.asyncio as aioredis

class Cache:
    _redis: aioredis.Redis | None = None

    @classmethod
    async def setup(cls, redis_url: str) -> None:
        cls._redis = aioredis.from_url(redis_url, decode_responses=True)
        await cls._redis.ping()

    @classmethod
    def _check_setup(cls) -> None:
        if not cls._redis:
            raise RuntimeError("Redis is not configured")

    @classmethod
    def is_configured(cls) -> bool:
        return cls._redis is not None

    @classmethod
    async def set(cls, key: str, value: str, exp_seconds: int | None = None) -> None:
        cls._check_setup()
        await cls._redis.set(key, value, ex=exp_seconds)

    @classmethod
    async def get(cls, key: str) -> str | None:
        cls._check_setup()
        return await cls._redis.get(key)
