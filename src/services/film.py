from functools import lru_cache
from typing import Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.db.elastic import get_elastic
from src.db.redis_db import get_redis
from src.models.film import Film, FilmShort
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
            await self._put_to_cache(
                f"{self.get_by_id.__name__}{self.index}{film_id}",
                orjson.dumps(film.dict()))
        return film

    async def home_page(self, size: int, page: int, sort: str, genre: str
                        ) -> Optional[list]:
        cache_id = f"{self.home_page.__name__}{self.index}{size}{page}{sort}"
        if genre:
            cache_id = f"""
            {self.home_page.__name__}{self.index}{size}{page}{sort}{genre}"""
        films = await self._get_from_cache(cache_id)
        if films:
            films = orjson.loads(films)
        if not films:
            body = {
                "size": size,
                "from": size * (page - 1),
                "query": {
                    "bool": {
                        "filter": []
                    }
                },
                "sort": [{
                    "imdb_rating": {
                        "order": "desc" if sort == 'imdb_rating' else "asc"
                    }
                }],
                "_source": ["id", "title", "imdb_rating"]
            }
            if genre:
                body["query"]["bool"]["filter"].append(
                    {"term": {"genres.id": genre}})
            docs = await self._search_from_elastic(self.index, body)
            films = [FilmShort(**i['_source']) for i in docs]
            if not films:
                return []
            await self._put_to_cache(cache_id, orjson.dumps(
                [film.dict() for film in films]))
        return films

    async def search_films(self, size: int, page: int, query: str
                           ) -> Optional[list]:
        cache_id = f"""
                {self.search_films.__name__}{self.index}{size}{page}{query}"""
        films = await self._get_from_cache(cache_id)
        if films:
            films = orjson.loads(films)
        if not films:
            body = {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"title": query}},
                        ]
                    }
                }
            }
            docs = await self._search_from_elastic(self.index, body)
            films = [FilmShort(**i['_source']) for i in docs]
            if not films:
                return []
            await self._put_to_cache(cache_id, orjson.dumps(
                [film.dict() for film in films]))
        return films


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
