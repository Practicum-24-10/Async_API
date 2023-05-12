import asyncio
import aiohttp
from typing import Any, Generator

import pytest
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings


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
