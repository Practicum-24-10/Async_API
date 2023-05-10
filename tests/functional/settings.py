from pydantic import BaseSettings
from testdata.es_mapping import mapping


class TestSettings(BaseSettings):
    es_host: str = 'http://localhost'
    es_port: str = '9200'
    es_indexes: list[str] = ['movies']
    es_id_field: str = 'id'
    es_index_mapping: dict = mapping

    service_url: str = 'http://localhost:8000/api/v1/'


test_settings = TestSettings()
