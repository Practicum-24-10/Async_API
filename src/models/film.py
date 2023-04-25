from src.models.mixins import MovieMixin


class Genre(MovieMixin):
    name: str | None = None
    
    
class Person(MovieMixin):
    name: str
    
    
class Film(MovieMixin):
    title: str
    description: str
    imdb_rating: float
    genres: list[Genre] | None = None
    directors: list[Person]
    actors: list[Person]
    writers: list[Person]
