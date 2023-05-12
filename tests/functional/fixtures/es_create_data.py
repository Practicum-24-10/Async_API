import json
from typing import List

import pytest
from elasticsearch import BadRequestError

from tests.functional.settings import test_settings
from tests.functional.testdata.es_mapping import mapping
from tests.functional.testdata.es_data import test_data


def get_es_bulk_query(data: List[dict], es_index: str,
                      es_id_field: str) -> List:
    bulk_query = []
    for row in data:
        bulk_query.extend([
            json.dumps({'index': {
                '_index': es_index,
                '_id': row[es_id_field]}}),
            json.dumps(row)
        ])
    return bulk_query


async def create_index(es_client):
    try:
        await es_client.indices.create(
            settings=mapping["settings"],
            mappings=mapping["mappings_movies"],
            index="movies",
        )
    except BadRequestError:
        pass
    try:
        await es_client.indices.create(
            settings=mapping["settings"],
            mappings=mapping["mappings_persons"],
            index="persons",
        )
    except BadRequestError:
        pass
    try:
        await es_client.indices.create(
            settings=mapping["settings"],
            mappings=mapping["mappings_genres"],
            index="genres",
        )
    except BadRequestError:
        pass


@pytest.fixture
def es_write_data(es_client):
    async def inner():
        await create_index(es_client)
        for index in test_settings.es_indexes:
            bulk_query = get_es_bulk_query(
                test_data[index],
                index,
                test_settings.es_id_field)
            response = await es_client.bulk(operations=bulk_query,
                                            refresh=True)
            if response['errors']:
                raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


@pytest.fixture
def es_delete_data(es_client):
    async def inner():
        for index in test_settings.es_indexes:
            if await es_client.indices.exists(index=index):
                await es_client.indices.delete(index=index)
    return inner
