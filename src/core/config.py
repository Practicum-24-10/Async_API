import os
from logging import config as logging_config

import dotenv
from pydantic import BaseSettings, Field

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)
dotenv.load_dotenv()


class AppSettings(BaseSettings):
    project_name: str = Field('Some project name', env='PROJECT_NAME')
    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')
    elastic_host: str = Field(..., env='ES_HOST')
    elastic_port: int = Field(9200, env='ES_PORT')


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
