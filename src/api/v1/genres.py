from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from src.services.genre import GenreService, get_genre_service

router = APIRouter()


class Genre(BaseModel):
    uuid: UUID = Field(..., alias="id", title="UUID жанра",
                       example="f39d7b6d-aef2-40b1-aaf0-cf05e7048011")
    name: str = Field(..., title="Название жанра жанра",
                      example="Horror")
    description: str | None = Field(..., title="Описание жанра",
                                    example="Очень стращный жанр")


@router.get(
    "/{genre_id}",
    response_model=Genre,
    response_model_by_alias=False,
    summary="Данные по конкретному жанру",
    description="Метод выдает все данные жанра по его uuid",
)
async def genre_details(
        genre_id: UUID,
        genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    """
    Метод API
    Получение всех данных жанра
    :param genre_id: uuid жанра
    :param genre_service:
    :return: данные Жанра в моделе Genre
    """
    genre = await genre_service.get_by_id(str(genre_id))
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="genre not found"
        )
    return Genre(id=genre.id, name=genre.name, description=genre.description)


@router.get(
    "/",
    response_model=list[Genre],
    response_model_by_alias=False,
    summary="Получения спика жанров кино",
    description="Метод выдает список жанров",
)
async def genre_all(
        genre_service: GenreService = Depends(get_genre_service),
        page: int = 1,
        size: int = 10,
) -> list[Genre]:
    """
    Метод API
    Получения спика жанров кино
    :param genre_service:
    :param page: страница
    :param size: размер страницы
    :return: список жанров кино в моделях Genre
    """
    genres = await genre_service.get_all(page, size)
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="genres not found"
        )
    return [Genre(**i.dict()) for i in genres.items]
