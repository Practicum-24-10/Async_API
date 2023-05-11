from abc import ABC, abstractmethod
from typing import Any

import orjson
from elasticsearch import NotFoundError

from src.db.cache import AbstractCache
from src.db.storage import AbstractStorage

CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class AbstractMixin(ABC):
    @abstractmethod
    def _get_cache_id(self, method: str, data: str | dict):
        pass

    @abstractmethod
    async def _get_from_cache(self, _id: bytes) -> bytes | None:
        pass

    @abstractmethod
    async def _put_to_cache(self, _id: bytes, data: bytes):
        pass

    @abstractmethod
    async def _search_from_elastic(
            self,
            index: str,
            body: dict[str, Any],
    ) -> list[dict[str, Any]] | None:
        pass


class MixinModel(AbstractMixin):
    def __init__(self, cache: AbstractCache, storage: AbstractStorage,
                 index: str):
        self.cache = cache
        self.storage = storage
        self.index = index

    def _get_cache_id(self, method: str, data: str | dict):
        return orjson.dumps({self.index: {method: data}})

    async def _get_from_cache(self, _id: bytes) -> bytes | None:
        """
        Получения данных по id
        :param _id:
        :return: данные в bytes
        """
        data = await self.cache.get(_id)
        if not data:
            return None
        return data

    async def _put_to_cache(self, _id: bytes, data: bytes):
        """
        Сохраняет в кеш данные
        :param _id: id для доступа
        :param data: данные в bytes
        """
        await self.cache.set(_id, data, CACHE_EXPIRE_IN_SECONDS)

    async def _get_by_id_from_elastic(
            self, index: str, _id: str
    ) -> dict[str, Any] | None:
        """
        Получение данных индекса по id из elastic
        :param index: индекс elastic
        :param _id: запрашиваемый id
        :return: данные в виде словаря
        """
        try:
            doc = await self.storage.get(index=index, id=_id)
        except NotFoundError:
            return None
        return doc["_source"]

    async def _search_from_elastic(
            self,
            index: str,
            body: dict[str, Any],
    ) -> list[dict[str, Any]] | None:
        """
        Получение всех данных индекса из elastic
        :param index: индекс elastic
        :param body: параметры поиска
        :return: лист с данными
        """
        try:
            doc = await self.storage.search(index=index, body=body)
        except NotFoundError:
            return None
        return doc["hits"]["hits"]
