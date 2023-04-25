from functools import lru_cache
from typing import Optional

from fastapi import Depends
from aioredis import Redis
import orjson
from elasticsearch import AsyncElasticsearch

from src.db.elastic import get_elastic
from src.db.redis_db import get_redis
from src.models.film import Film
from src.services.mixin import MixinModel


class FilmService(MixinModel):
    index = 'movies'

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._get_from_cache(film_id)
        if not film:
            doc = await self._get_by_id_from_elastic(self.index, film_id)
            if not doc:
                return None
            film = Film(**doc)
            await self. _put_to_cache(
                f"{self.get_by_id.__name__}{self.index}{film_id}",
                orjson.dumps(film.dict()))
        return film
        
        



@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
