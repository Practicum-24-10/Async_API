from abc import ABC, abstractmethod
from typing import Any

from elasticsearch import AsyncElasticsearch


class AbstractStorage(ABC):
    @abstractmethod
    async def get(self, index: str, id: str):
        pass

    @abstractmethod
    async def search(self, index: str,
                     body: dict[str, Any]):
        pass

    @abstractmethod
    async def close(self):
        pass


class ElasticStorage(AbstractStorage):
    def __init__(self, hosts: list[str]):
        self._connect = AsyncElasticsearch(hosts=hosts)

    async def get(self, index: str, id: str):
        return await self._connect.get(index=index, id=id)

    async def search(self, index: str,
                     body: dict[str, Any]):
        return await self._connect.search(index=index, body=body)

    async def close(self):
        await self._connect.close()
