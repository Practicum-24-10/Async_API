from functools import lru_cache

import orjson

from src.db.cache import AbstractCache
from src.db.storage import AbstractStorage
from fastapi import Depends

from src.db.elastic import get_elastic
from src.db.redis_db import get_redis
from src.models.genre import GenreES, ListViewGenresES
from src.services.mixin import MixinModel


class GenreService(MixinModel):
    async def get_by_id(self, genre_id: str) -> GenreES | None:
        cache_id = self._get_cache_id(self.get_by_id.__name__, genre_id)
        genre = await self._get_from_cache(cache_id)
        if genre is not None:
            genre = GenreES(**orjson.loads(genre))
        if not genre:
            row_data = await self._get_by_id_from_elastic(self.index, genre_id)
            if not row_data:
                return None
            genre = GenreES(**row_data)
            await self._put_to_cache(cache_id, orjson.dumps(genre.dict()))

        return genre

    async def get_all(self, page, size) -> ListViewGenresES | None:
        body = {"size": size, "from": (page - 1) * size}
        cache_id = self._get_cache_id(self.get_all.__name__, body)
        genres = await self._get_from_cache(cache_id)
        if genres is not None:
            genres = ListViewGenresES(**orjson.loads(genres))
        if not genres:
            row_data = await self._search_from_elastic(self.index, body)
            if not row_data:
                return None
            genres = ListViewGenresES(
                items=[GenreES(**i["_source"]) for i in row_data]
            )
            await self._put_to_cache(cache_id, orjson.dumps(genres.dict()))

        return genres


@lru_cache()
def get_genre_service(
    redis: AbstractCache = Depends(get_redis),
    elastic: AbstractStorage = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic, "genres")
