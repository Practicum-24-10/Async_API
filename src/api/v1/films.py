from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from services.film import FilmService, get_film_service
from src.models.genre import Genre
from src.models.person import Person
from uuid import UUID


router = APIRouter()


class Film(BaseModel):
    uuid: UUID
    title: str
    description: str
    imdb_rating: float
    # genre: list[Genre]
    directors: list[Person] | None = []
    actors: list[Person]
    writers: list[Person]
    
        
@router.get("/{film_id}",
            response_model_by_alias=False,
            response_model=Film)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="film not found"
        )

    return Film(
                uuid=film.id,
                title=film.title,
                description=film.description,
                imdb_rating=film.imdb_rating,
                # genre: list[Genre],
                directors=film.directors,
                actors=film.actors,
                writers=film.writers,
                )
