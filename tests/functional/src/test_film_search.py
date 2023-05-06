import pytest

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
async def test_search(make_get_request, es_write_data, query_data,
                      expected_answer):
    await es_write_data(es_data)
    response = await make_get_request('films/search', query_data)
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
