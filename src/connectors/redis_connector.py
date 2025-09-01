from logger import logger
import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        logger.info(f"Подключение к Redis: Host={self.host}, Port={self.port} ")
        self.redis = await redis.Redis(host=self.host, port=self.port)
        logger.info("Подключение к Redis прошло успешно")

    async def set(self, key: str, value: str, expire: int = None):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        await self.redis.aclose()
