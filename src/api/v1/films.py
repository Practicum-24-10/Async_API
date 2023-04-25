from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from services.film import FilmService, get_film_service
from src.models.film import Genre, Person
from uuid import UUID
from enum import Enum


router = APIRouter()


class OrderingFilms(str, Enum):
    popular = "-imdb_rating"
    not_popular = "imdb_rating"


class UUIDMixin(BaseModel):
    uuid: UUID = Field(alias='id')


class FilmShort(UUIDMixin, BaseModel):
    title: str
    imdb_rating: float


class FilmDetail(FilmShort):
    description: str
    genres: list[Genre] | None = None
    directors: list[Person]
    actors: list[Person]
    writers: list[Person]
   

@router.get('/',
            response_model=list[FilmShort],
            summary="Главная страница")
async def film_list(
    sort: OrderingFilms,
    page_size: int = 10,
    page_number: int = 1,
    genre: UUID | None = None,
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmShort]:
    films = await film_service.home_page(
        size=page_size, 
        page=page_number, 
        sort=sort,
        genre=genre)
    return films
    
    
        
@router.get("/{film_id}",
            response_model_by_alias=False,
            response_model=FilmDetail)
async def film_details(
    film_id: UUID, film_service: FilmService = Depends(get_film_service)
) -> FilmDetail:
    film = await film_service.get_by_id(str(film_id))
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="film not found"
        )
    return FilmDetail(**film.dict(by_alias=True))



