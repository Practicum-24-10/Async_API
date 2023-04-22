from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.services.genre import GenreService, get_genre_service
from src.models.genre import Genre

router = APIRouter()


@router.get("/{genre_id}", response_model=Genre)
async def genre_details(
        genre_id: str, film_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await film_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="genre not found")
    return Genre(id=genre.id, name=genre.name, description=genre.description)


@router.get("/", response_model=list[Genre])
async def genre_all(
        genre_service: GenreService = Depends(get_genre_service),
        page: int = 1,
        size: int = 10,
) -> list[Genre]:
    genre = await genre_service.get_all(page, size)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="genres not found")
    return [Genre(id=i.id, name=i.name, description=i.description) for i in
            genre]
