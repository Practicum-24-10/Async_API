import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1 import films, genres, persons
from src.core.config import AppSettings
from src.core.logger import LOGGING
from src.db import elastic, redis_db
from src.db.cache import RedisCache
from src.db.storage import ElasticStorage

config = AppSettings()
app = FastAPI(
    title=config.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis_db.redis = RedisCache(host=config.redis_host, port=config.redis_port)
    elastic.es = ElasticStorage(hosts=[f"{config.es_host}:{config.es_port}"])


@app.on_event("shutdown")
async def shutdown():
    if redis_db.redis:
        await redis_db.redis.close()
    if elastic.es:
        await elastic.es.close()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])

if __name__ == "__main__":
    logging.basicConfig(**LOGGING)
    log = logging.getLogger(__name__)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
