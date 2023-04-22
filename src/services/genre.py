from functools import lru_cache
from typing import Optional, Any
import orjson

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis_db import get_redis
from src.models.genre import GenreES
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

    async def get_all(self, page, size) -> list[GenreES] | None:
        genres = await self._get_from_cache(f"all_genre{page}{size}")
        if genres is not None:
            genres = [GenreES(**i) for i in orjson.loads(genres)]
        if not genres:
            body = {
                "size": size,
                "from": (page-1)*size
            }
            row_data = await self._search_from_elastic(self.index, body)
            if not row_data:
                return None
            genres = [GenreES(**i["_source"]) for i in row_data]
            await self._put_to_cache(
                F"all_genre{page}{size}", orjson.dumps([i.dict() for i in genres])
            )

        return genres


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)

# curl -XGET http://127.0.0.1:9200/movies/_search -H 'Content-Type: application/json' -d '
#
# {
#     "query": {
#         "bool": {
#             "must": [
#                 {"match": {"actors_name": "William Shatner"}}
#             ]
#         }
#     }
# }'
