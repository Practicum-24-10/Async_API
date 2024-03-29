from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel, Field
from src.api.v1.models import PaginatedParams
from src.local.api.v1 import anotation
from src.local.api.v1 import persons as errors
from src.services.person import PersonService, get_person_service

router = APIRouter()


class PersonFilm(BaseModel):
    uuid: UUID = Field(..., alias="id", title="UUID фильма",
                       example="9b3c278c-665f-4055-a824-891f19cb4993")
    roles: list[str] = Field(..., title="Список ролей",
                             example=['actor', 'writer'])


class FilmDetail(BaseModel):
    uuid: UUID = Field(..., alias="id", title="UUID фильма",
                       example="9b3c278c-665f-4055-a824-891f19cb4993")
    title: str = Field(..., title="Название фильма",
                       example="Star Trek Continues")
    imdb_rating: float = Field(..., title="Рейтинг фильма",
                               example=8.0)


class PersonDetail(BaseModel):
    uuid: UUID = Field(..., alias="id", title="UUID персоны",
                       example="9758b894-57d7-465d-b657-c5803dd5b7f7")
    full_name: str = Field(..., title="Полное имя персоны",
                           example="William Shatner")
    films: list[PersonFilm] = Field(..., title="Список фильмов")


@router.get(
    "/{person_id}",
    response_model=PersonDetail,
    response_model_by_alias=False,
    summary="Данные по персоне",
    description="Метод выдает все данные персоны "
                "по uuid и фильмы с его/ее участием",
)
async def person_details(
        person_id: Annotated[UUID, Path(
            description=anotation.PERSON_ID,
            example="9758b894-57d7-465d-b657-c5803dd5b7f7"
        )],
        person_service: PersonService = Depends(get_person_service),
        pagination: PaginatedParams = Depends(),
) -> PersonDetail:
    """
    Метод API
    Получение всех данных персоны
    :param person_id: uuid персоны
    :param person_service:
    :param pagination: страница и размер страницы
    :return: данные персону в моделе Person
    """
    person = await person_service.get_by_id(
        str(person_id), pagination.page, pagination.size
    )
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=errors.PERSON_DETAILS
        )
    return PersonDetail(**person.dict())


@router.get(
    "/{person_id}/film",
    response_model=list[FilmDetail],
    response_model_by_alias=False,
    summary="Фильмы по персоне",
    description="Метод выдает подробные данные "
                "фильмов по uuid персоны с его/ее участием",
)
async def person_details_film(
        person_id: Annotated[UUID, Path(
            description=anotation.PERSON_ID,
            example="9758b894-57d7-465d-b657-c5803dd5b7f7"
        )],
        person_service: PersonService = Depends(get_person_service),
        pagination: PaginatedParams = Depends(),
) -> list[FilmDetail]:
    """
    Метод API
    Получение всех фильмов персоны
    :param person_id: uuid персоны
    :param person_service:
    :param pagination: страница и размер страницы
    :return: список данных фильмов в моделе PersonFilm
    """
    films_person = await person_service.get_person_films(
        str(person_id), pagination.page, pagination.size
    )
    if not films_person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=errors.PERSON_DETAILS
        )
    return [FilmDetail(**i.dict()) for i in films_person.films]


@router.get("/search/", response_model=list[PersonDetail],
            response_model_by_alias=False,
            summary="Поиск по персонам",
            description="Метод выдает данные поиска по имени персоны "
                        "из query запроса")
async def person_search(
        query: Annotated[
            str, Query(description=anotation.PERSON_QUERY,
                       example="William Shatner", min_length=1)
        ],
        person_service: PersonService = Depends(get_person_service),
        pagination: PaginatedParams = Depends(),
) -> list[PersonDetail]:
    """
    Метод API
    Поиск по имени персоны
    :param query: запрос на поиск
    :param person_service:
    :param pagination: страница и размер страницы
    :return: список найденых персон в моделях Person
    """
    search_person = await person_service.search_person(
        query, pagination.page, pagination.size
    )
    if not search_person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=errors.PERSON_SEARCH
        )
    return [PersonDetail(**i.dict()) for i in search_person.items]
