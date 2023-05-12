import time

from elasticsearch import Elasticsearch

from tests.functional.utils.settings_wait_for import EsSettings
from tests.functional.utils.backoff import check_connection

if __name__ == '__main__':
    config = EsSettings()  # type: ignore
    es_client = Elasticsearch(
        hosts=[f"{config.elastic_host}:{config.elastic_port}"]
    )
    check_connection(es_client)
