from typing import Annotated

from fastapi import Query
from src.local.api.v1 import anotation


class PaginatedParams:
    def __init__(
            self,
            page: Annotated[
                int,
                Query(description=anotation.PAGINATION_PAGE, ge=1)
            ] = 1,
            size: Annotated[
                int,
                Query(description=anotation.PAGINATION_SIZE, ge=1)
            ] = 10,
    ):
        self.page = page
        self.size = size
