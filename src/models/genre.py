from pydantic import BaseModel

from src.models.mixins import MovieMixin


class GenreES(MovieMixin):
    name: str
    description: str | None = ""


class ListViewGenresES(BaseModel):
    items: list[GenreES]
