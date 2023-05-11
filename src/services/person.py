from functools import lru_cache
from typing import Any

import orjson

from src.db.cache import AbstractCache
from src.db.storage import AbstractStorage
from fastapi import Depends

from src.db.elastic import get_elastic
from src.db.redis_db import get_redis
from src.models.person import (
    FilmPersonES,
    ListPersonFilm,
    PersonES,
    PersonFilmES,
    SearchPersons,
)
from src.services.mixin import MixinModel


class PersonService(MixinModel):
    async def get_by_id(self, person_id: str, page, size) -> PersonES | None:
        """
        Метод получения данных по uuid
        Если запрос есть в кеше Redis выдаются данные из Redis
        иначе идет обращение в Elasticsearch
        :param person_id: uuid персоны
        :param page: страница
        :param size: размер страницы
        :return: данные в моделе PersonES или None
        """
        body = {
            "size": size,
            "from": (page - 1) * size,
            "query": self.get_query_in_films(person_id),
        }
        cache_id = self._get_cache_id(self.get_by_id.__name__, body)
        person = await self._get_from_cache(cache_id)
        if person is not None:
            person = PersonES(**orjson.loads(person))
        if not person:
            person_data = await self._get_by_id_from_elastic(
                self.index, person_id
            )
            if not person_data:
                return None
            row_in_films = await self._search_from_elastic("movies", body)
            in_films = self._get_in_films(row_in_films, person_id)
            person = PersonES(
                id=person_data["id"],
                full_name=person_data["full_name"],
                films=[FilmPersonES(**i) for i in in_films],
            )
            await self._put_to_cache(cache_id, orjson.dumps(person.dict()))

        return person

    @staticmethod
    def _get_in_films(
            row_in_films: list,
            person_id: str
    ) -> list[dict[str, Any]]:
        """
        Метод для получения id фильмов и ролей персоны которая/который
        учавствовали в данных фильмах
        :param row_in_films: Список фильмов полученых из Elasticsearch
        :param person_id: uuid искомой персоны
        :return: список со словарями фильмов и ролями персоны
        """
        in_films = []
        for movies in row_in_films:
            film_data = {"id": movies["_source"]["id"], "roles": []}
            for actors in movies["_source"]["actors"]:
                if person_id in actors.values():
                    film_data["roles"].append("actor")
                    break
            for writers in movies["_source"]["writers"]:
                if person_id in writers.values():
                    film_data["roles"].append("writer")
                    break
            for directors in movies["_source"]["directors"]:
                if person_id in directors.values():
                    film_data["roles"].append("director")
                    break
            in_films.append(film_data)
        return in_films

    async def get_person_films(
        self, person_id: str, page, size
    ) -> ListPersonFilm | None:
        """
        Метод получения подробных данных фильмов с участием персоны по uuid
        Если запрос есть в кеше Redis выдаются данные из Redis
        иначе идет обращение в Elasticsearch
        :param person_id: uuid персоны
        :param page: страница
        :param size: размер страницы
        :return: список данных фильмов в моделе ListPersonFilm или None
        """
        body = {
            "size": size,
            "from": (page - 1) * size,
            "query": self.get_query_in_films(person_id),
        }
        cache_id = self._get_cache_id(self.get_person_films.__name__, body)
        person_films = await self._get_from_cache(cache_id)
        if person_films is not None:
            person_films = ListPersonFilm(**orjson.loads(person_films))
        if not person_films:
            row_in_films = await self._search_from_elastic("movies", body)
            if not row_in_films:
                return None
            in_films = []
            for movies in row_in_films:
                film_data = {
                    "id": movies["_source"]["id"],
                    "title": movies["_source"]["title"],
                    "imdb_rating": movies["_source"]["imdb_rating"],
                }
                in_films.append(film_data)
            person_films = ListPersonFilm(
                films=[PersonFilmES(**i) for i in in_films]
            )
            await self._put_to_cache(
                cache_id,
                orjson.dumps(person_films.dict()),
            )

        return person_films

    async def search_person(
            self, query: str, page, size
    ) -> SearchPersons | None:
        """
        Метод поисках персоны по ее имени подробных
        Если запрос есть в кеше Redis выдаются данные из Redis
        иначе идет обращение в Elasticsearch
        :param query: запрос на поиск
        :param page: страница
        :param size: размер страницы
        :return: список данных найденых персон в моделе SearchPersons или None
        """
        body = {
            "size": size,
            "from": (page - 1) * size,
            "query": self.get_query_search(query),
        }
        cache_id = self._get_cache_id(self.search_person.__name__, body)
        found_persons = await self._get_from_cache(cache_id)
        if found_persons is not None:
            found_persons = SearchPersons(**orjson.loads(found_persons))
        if not found_persons:
            found_persons = await self._search_from_elastic(self.index, body)
            if not found_persons:
                return None
            valid_found_persons = []
            for row in found_persons:
                person_data = row["_source"]
                body = {"query": self.get_query_in_films(person_data["id"])}
                row_in_films = await self._search_from_elastic("movies", body)
                in_films = self._get_in_films(row_in_films, person_data["id"])
                valid_person = PersonES(
                    id=person_data["id"],
                    full_name=person_data["full_name"],
                    films=[FilmPersonES(**i) for i in in_films],
                )
                valid_found_persons.append(valid_person)
            found_persons = SearchPersons(items=valid_found_persons)
            await self._put_to_cache(
                cache_id, orjson.dumps(found_persons.dict())
            )

        return found_persons

    @staticmethod
    def get_query_in_films(_id: str) -> dict[str, Any]:
        """
        Метод для получения данных запроса на поиск данных в Elasticsearch
        :param _id: uuid персоны
        :return: данные запроса в виде словаря
        """
        return {
            "bool": {
                "should": [
                    {
                        "nested": {
                            "path": "actors",
                            "query": {"bool": {
                                "must": [{"term": {"actors.id": _id}}]}
                            },
                        }
                    },
                    {
                        "nested": {
                            "path": "writers",
                            "query": {
                                "bool": {
                                    "must": [{"term": {"writers.id": _id}}]
                                }
                            },
                        }
                    },
                    {
                        "nested": {
                            "path": "directors",
                            "query": {
                                "bool": {
                                    "must": [{"term": {"directors.id": _id}}]
                                }
                            },
                        }
                    },
                ]
            }
        }

    @staticmethod
    def get_query_search(query: str) -> dict[str, Any]:
        """
        Метод для получения данных запроса на поиск данных в Elasticsearch
        :param query: искомые данные
        :return: данные запроса в виде словаря
        """
        return {"bool": {"must": [{"match": {"full_name": query}}]}}


@lru_cache()
def get_person_service(
    redis: AbstractCache = Depends(get_redis),
    elastic: AbstractStorage = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic, "persons")
