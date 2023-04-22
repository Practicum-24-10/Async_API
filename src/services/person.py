from functools import lru_cache
from typing import Optional, Any
import orjson

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis_db import get_redis
from src.models.person import PersonES
from src.services.mixin import MixinModel

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class PersonService(MixinModel):
    index = "persons"

    async def get_by_id(self, person_id: str) -> PersonES | None:
        person = await self._get_from_cache(person_id)
        if person is not None:
            person = PersonES(**orjson.loads(person))
        if not person:
            person_data = await self._get_by_id_from_elastic(self.index, person_id)
            if not person_data:
                return None
            # films_data = await
            # person = PersonES(**row_data)
            await self._put_to_cache(str(person.id), orjson.dumps(person.dict()))

        return person

    async def get_all(self, page, size) -> list[PersonES] | None:
        genres = await self._get_from_cache(f"all_genre{page}{size}")
        if genres is not None:
            genres = [PersonES(**i) for i in orjson.loads(genres)]
        if not genres:
            body = {
                "size": size,
                "from": (page-1)*size
            }
            row_data = await self._search_from_elastic(self.index, body)
            if not row_data:
                return None
            genres = [PersonES(**i["_source"]) for i in row_data]
            await self._put_to_cache(
                F"all_genre{page}{size}", orjson.dumps([i.dict() for i in genres])
            )

        return genres


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)

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
