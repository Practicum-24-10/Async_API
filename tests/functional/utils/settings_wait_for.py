import dotenv
from pydantic import BaseSettings, Field

dotenv.load_dotenv()


class RedisSettings(BaseSettings):
    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')


class EsSettings(BaseSettings):
    elastic_host: str = Field(..., env='ES_HOST')
    elastic_port: int = Field(9200, env='ES_PORT')
