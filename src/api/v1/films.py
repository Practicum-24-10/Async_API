from enum import Enum
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from src.services.film import FilmService, get_film_service
from src.models.film import Genre, Person

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
                       example="Kirk and Spock team up against the Gorn.")
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



@router.get('/search',
            response_model=list[FilmShort],
            response_model_by_alias=False,
            summary="Поиск по фильмам")
async def film_search(
    query: str,
    page_size: int = 10,
    page_number: int = 1,
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmShort]:
    films = await film_service.search_films(
        query=query,
        size=page_size, 
        page=page_number)
    return films
    
    
        
@router.get("/{film_id}",
            response_model_by_alias=False,
            response_model=FilmDetail,
            summary="Страница фильма")
async def film_details(
    film_id: UUID,
    film_service: FilmService = Depends(get_film_service)
) -> FilmDetail:
    film = await film_service.get_by_id(str(film_id))
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="film not found")
    return FilmDetail(**film.dict(by_alias=True))
