from functools import lru_cache

import orjson
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from aioredis import Redis

from src.db.elastic import get_elastic
from src.db.redis_db import get_redis
from src.models.genre import GenreES, ListViewGenresES
from src.services.mixin import MixinModel

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class GenreService(MixinModel):
    index = "genres"

    async def get_by_id(self, genre_id: str) -> GenreES | None:
        genre = await self._get_from_cache(genre_id)
        if genre is not None:
            genre = GenreES(**orjson.loads(genre))
        if not genre:
            row_data = await self._get_by_id_from_elastic(self.index, genre_id)
            if not row_data:
                return None
            genre = GenreES(**row_data)
            await self._put_to_cache(str(genre.id), orjson.dumps(genre.dict()))

        return genre

    async def get_all(self, page, size) -> ListViewGenresES | None:
        genres = await self._get_from_cache(
            f"genre{self.get_all.__name__}{page}{size}"
        )
        if genres is not None:
            genres = ListViewGenresES(**orjson.loads(genres))
        if not genres:
            body = {"size": size, "from": (page - 1) * size}
            row_data = await self._search_from_elastic(self.index, body)
            if not row_data:
                return None
            genres = ListViewGenresES(
                items=[GenreES(**i["_source"]) for i in row_data]
            )
            await self._put_to_cache(
                f"genre{self.get_all.__name__}{page}{size}",
                orjson.dumps(genres.dict())
            )

        return genres


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
