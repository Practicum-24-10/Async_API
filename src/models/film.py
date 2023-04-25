from src.models.genre import Genre
from src.models.mixins import MovieMixin
from src.models.person import Person


class Film(MovieMixin):
    title: str
    description: str
    imdb_rating: float
    genres: list[Genre] | None = None
    directors: list[Person]
    actors: list[Person]
    writers: list[Person]
