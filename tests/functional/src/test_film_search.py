import aiohttp
import pytest

from tests.functional.settings import test_settings
from tests.functional.testdata.es_data import es_data


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': 'The Star', 'page_size': '60', 'page_number': '1'},
            {'status': 200, 'length': 60}
        ),
        (
            {'query': 'Mashed potato', 'page_size': '60', 'page_number': '1'},
            {'status': 404, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(es_write_data, query_data, expected_answer):
    await es_write_data(es_data)
    session = aiohttp.ClientSession()
    url = test_settings.service_url + 'films/search'
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        status = response.status
    await session.close()
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']
