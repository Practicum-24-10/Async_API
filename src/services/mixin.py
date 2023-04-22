from typing import Any

from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis

CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class MixinModel:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def _get_from_cache(self, _id: str) -> bytes | None:
        """
        Получения данных по id
        :param _id:
        :return: данные в bytes
        """
        data = await self.redis.get(_id)
        if not data:
            return None
        return data

    async def _put_to_cache(self, _id: str, data: bytes):
        """
        Сохраняет в кеш данные
        :param _id: id для доступа
        :param data: данные в bytes
        """
        await self.redis.set(str(_id), data, CACHE_EXPIRE_IN_SECONDS)

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
            doc = await self.elastic.get(index=index, id=_id)
        except NotFoundError:
            return None
        return doc["_source"]

    async def _search_from_elastic(
            self, index: str, body,
    ) -> list[dict[str, Any]] | None:
        """
        Получение всех данных индекса из elastic
        :param index: индекс elastic
        :return: лист с данными
        """
        try:
            doc = await self.elastic.search(index=index, body=body)
        except NotFoundError:
            return None
        return doc["hits"]["hits"]
