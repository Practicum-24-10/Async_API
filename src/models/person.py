from src.models.mixins import MovieMixin


class Person(MovieMixin):
    full_name: str


class FilmPerson(MovieMixin):
    roles: list[str]


class PersonES(MovieMixin):
    full_name: str
    films: list[FilmPerson]
