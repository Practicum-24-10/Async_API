import logging

import uvicorn
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from core.config import AppSettings
from core.logger import LOGGING
from src.db import elastic, redis_db

config = AppSettings()
app = FastAPI(
    title=config.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis_db.redis = Redis(host=config.redis_host, port=config.redis_port)
    elastic.es = AsyncElasticsearch(
        hosts=[f"{config.elastic_host}:{config.elastic_port}"]
    )


@app.on_event("shutdown")
async def shutdown():
    await redis_db.redis.close()
    await elastic.es.close()


# Подключаем роутер к серверу, указав префикс /v1/films
# Теги указываем для удобства навигации по документации
app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])

if __name__ == "__main__":
    logging.basicConfig(**LOGGING)
    log = logging.getLogger(__name__)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
