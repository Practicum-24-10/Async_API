import time

from elasticsearch import Elasticsearch

from tests.functional.utils.settings_wait_for import EsSettings


if __name__ == '__main__':
    config = EsSettings()
    es_client = Elasticsearch(
        hosts=[f"{config.elastic_host}:{config.elastic_port}"]
    )
    while True:
        if es_client.ping():
            break
        time.sleep(1)
