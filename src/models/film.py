from src.models.mixins import MovieMixin


class Genre(MovieMixin):
    name: str | None = None
    
    
class Person(MovieMixin):
    name: str


class FilmShort(MovieMixin):
    title: str
    imdb_rating: float

    
class Film(FilmShort):
    description: str
    genres: list[Genre] | None = None
    directors: list[Person]
    actors: list[Person]
    writers: list[Person]
