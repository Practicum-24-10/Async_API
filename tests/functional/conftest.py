import asyncio
import aiohttp
import json
from typing import Any, Generator, List

import pytest
from elasticsearch import AsyncElasticsearch, BadRequestError

from tests.functional.settings import test_settings
from tests.functional.testdata.es_mapping import mapping


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


@pytest.fixture(scope="session", name="event_loop")
def fixture_event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(
            hosts=f"{test_settings.es_host}:{test_settings.es_port}")
    yield client
    await client.close()


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
    async def inner(data: List[dict]):
        await create_index(es_client)
        bulk_query = get_es_bulk_query(
            data,
            test_settings.es_index,
            test_settings.es_id_field)
        response = await es_client.bulk(operations=bulk_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
async def make_get_request():
    async with aiohttp.ClientSession() as session:
        async def _make_get_request(endpoint: str, params: dict | None = None):
            url = test_settings.service_url + endpoint
            params = params if params else {}
            async with session.get(url, params=params) as response:
                body = await response.json()
                status = response.status
            return {'status': status, 'body': body}
        yield _make_get_request
