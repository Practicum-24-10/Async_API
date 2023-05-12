from functools import lru_cache
from typing import Any, Optional
from uuid import UUID

import orjson
from fastapi import Depends

from src.db.cache import AbstractCache
from src.db.elastic import get_elastic
from src.db.redis_db import get_redis
from src.db.storage import AbstractStorage
from src.models.film import Film, FilmShort, ListFilmShort
from src.services.mixin import MixinModel


class FilmService(MixinModel):
    async def _get_films(
            self, method_name: str, query: dict[str, Any]) -> ListFilmShort | None:
        cache_id = self._get_cache_id(method_name, query)
        films = await self._get_from_cache(cache_id)
        if films:
            films = ListFilmShort(**orjson.loads(films))
        if not films:
            docs = await self._search_from_elastic(self.index, query)
            if not docs:
                return None
            films = ListFilmShort(
                films=[FilmShort(**i["_source"]) for i in docs]
            )
            await self._put_to_cache(cache_id, orjson.dumps(films.dict()))
        return films

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        cache_id = self._get_cache_id(self.get_by_id.__name__, film_id)
        film = await self._get_from_cache(cache_id)
        if film:
            film = Film(**orjson.loads(film))
        if not film:
            doc = await self._get_by_id_from_elastic(self.index, film_id)
            if not doc:
                return None
            film = Film(**doc)
            await self._put_to_cache(cache_id, orjson.dumps(film.dict()))
        return film

    async def home_page(
        self, size: int, page: int, sort: str, genre: UUID | None
    ) -> ListFilmShort | None:
        body = {
            "size": size,
            "from": size * (page - 1),
            "query": {"nested": {
                "path": "genres", "query": {"bool": {"filter": []}}}
            },
            "sort": [
                {"imdb_rating": {
                    "order": "desc" if sort == "imdb_rating" else "asc"
                }}
            ],
            "_source": ["id", "title", "imdb_rating"],
        }
        if genre:
            body["query"]["nested"]["query"]["bool"]["filter"].append(
                {"term": {"genres.id": genre}}
            )
        films = await self._get_films(self.home_page.__name__, body)
        return films

    async def search_films(
        self, size: int, page: int, query: str
    ) -> ListFilmShort | None:
        body = {
            "size": size,
            "from": size * (page - 1),
            "query": {
                "bool": {
                    "must": [
                        {"match": {"title": query}},
                    ]
                }
            },
        }
        films = await self._get_films(self.search_films.__name__, body)
        return films


@lru_cache()
def get_film_service(
    redis: AbstractCache = Depends(get_redis),
    elastic: AbstractStorage = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic, "movies")
