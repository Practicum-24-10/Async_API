from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.services.person import PersonService, get_genre_service
from src.models.person import Person

router = APIRouter()


@router.get("/{person_id}", response_model=Person)
async def person_details(
        person_id: str, film_service: PersonService = Depends(get_genre_service)
) -> Person:
    genre = await film_service.get_by_id(person_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="person not found")
    return Person(id=genre.id)


# @router.get("/", response_model=list[Genre])
# async def film_details(
#         genre_service: PersonService = Depends(get_genre_service),
#         page: int = 1,
#         size: int = 10,
# ) -> list[Genre]:
#     genre = await genre_service.get_all(page, size)
#     if not genre:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
#                             detail="genres not found")
#     return [Genre(id=i.id, name=i.name, description=i.description) for i in
#             genre]
