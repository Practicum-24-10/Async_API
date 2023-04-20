from .mixins import MovieMixin


class Genre(MovieMixin):
    name: str
    description: str | None = ''
