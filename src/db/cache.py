from abc import ABC, abstractmethod
from aioredis import Redis


class AbstractCache(ABC):
    @abstractmethod
    async def get(self, _id: bytes):
        pass

    @abstractmethod
    async def set(self, _id: bytes, data: bytes, expire: int):
        pass

    @abstractmethod
    async def close(self):
        pass


class RedisCache(AbstractCache):
    def __init__(self, host: str, port: int):
        self._connect = Redis(host=host, port=port)

    async def get(self, id: bytes):
        return await self._connect.get(name=id)

    async def set(self, id: bytes, data: bytes, expire: int):
        return await self._connect.set(name=id, value=data, ex=expire)

    async def close(self):
        await self._connect.close()
