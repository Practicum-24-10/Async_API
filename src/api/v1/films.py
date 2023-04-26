from enum import Enum
from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel, Field

from src.local.api.v1 import anotation
from src.local.api.v1 import films as errors
from src.models.film import Genre, Person
from src.services.film import FilmService, get_film_service

router = APIRouter()


class OrderingFilms(str, Enum):
    popular = "imdb_rating"
    not_popular = "-imdb_rating"


class UUIDMixin(BaseModel):
    uuid: UUID = Field(alias='id', title="UUID фильма",
                       example="9b3c278c-665f-4055-a824-891f19cb4993")


class FilmShort(UUIDMixin, BaseModel):
    title: str = Field(title="Название фильма",
                       example="Star Trek Continues")
    imdb_rating: float = Field(title="Рейтинг фильма",
                               example=8.0)


class FilmDetail(FilmShort):
    description: str = Field(..., title="Описание фильма",
                             example="Kirk and Spock team up against the Gorn")
    genres: list[Genre] | None = Field(default=None, title="Жанры фильма")
    directors: list[Person] = Field(title="Режисер")
    actors: list[Person] = Field(title="Актеры")
    writers: list[Person] = Field(title="Сценаристы")


@router.get('/',
            response_model=list[FilmShort],
            response_model_by_alias=False,
            summary="Главная страница")
async def film_list(
        sort: OrderingFilms = OrderingFilms.popular,
        page_size: Annotated[
            int, Query(description=anotation.PAGINATION_SIZE, ge=1)
        ] = 10,
        page_number: Annotated[
            int, Query(description=anotation.PAGINATION_PAGE, ge=1)
        ] = 1,
        genre: Annotated[UUID, Path(
            description=anotation.GENRE_ID
        )] = None,
        film_service: FilmService = Depends(get_film_service),
) -> list[FilmShort]:
    films = await film_service.home_page(
        size=page_size,
        page=page_number,
        sort=sort,
        genre=str(genre))
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=errors.FILM_ALL)
    return films


@router.get('/search',
            response_model=list[FilmShort],
            response_model_by_alias=False,
            summary="Поиск по фильмам")
async def film_search(
        query: Annotated[
            str, Query(description=anotation.FILMS_QUERY,
                       example="Star", min_length=1)
        ],
        page_size: Annotated[
            int, Query(description=anotation.PAGINATION_SIZE, ge=1)
        ] = 10,
        page_number: Annotated[
            int, Query(description=anotation.PAGINATION_PAGE, ge=1)
        ] = 1,
        film_service: FilmService = Depends(get_film_service),
) -> list[FilmShort]:
    films = await film_service.search_films(
        query=query,
        size=page_size,
        page=page_number)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=errors.FILM_SEARCH)
    return films


@router.get("/{film_id}",
            response_model_by_alias=False,
            response_model=FilmDetail,
            summary="Страница фильма")
async def film_details(
        film_id: Annotated[UUID, Path(
            description=anotation.FILM_ID,
            example="77bff1a8-f6e2-4a6c-b555-b5d44c34c0dd"
        )],
        film_service: FilmService = Depends(get_film_service)
) -> FilmDetail:
    film = await film_service.get_by_id(str(film_id))
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=errors.FILM_DETAILS)
    return FilmDetail(**film.dict(by_alias=True))
