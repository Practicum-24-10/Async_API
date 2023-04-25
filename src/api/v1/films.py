from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from services.film import FilmService, get_film_service
from src.models.film import Genre, Person
from uuid import UUID


router = APIRouter()


class UUIDMixin(BaseModel):
    id: UUID


class FilmShort(UUIDMixin, BaseModel):
    title: str
    imdb_rating: float
    genre: list[Genre]


class FilmDetail(UUIDMixin,BaseModel):
    uuid: UUID = Field(alias='id')
    title: str
    description: str
    imdb_rating: float
    genres: list[Genre] | None = None
    directors: list[Person]
    actors: list[Person]
    writers: list[Person]
   


    
        
@router.get("/{film_id}",
            response_model_by_alias=False,
            response_model=FilmDetail)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmDetail:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="film not found"
        )
    return FilmDetail(**film.dict(by_alias=True))



