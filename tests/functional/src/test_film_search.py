import pytest

from tests.functional.testdata.es_data import films_data


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': 'The Star', 'size': '60', 'page': '1'},
            {'status': 200, 'length': 60}
        ),
        (
            {'query': 'Mashed potato', 'size': '60', 'page': '1'},
            {'status': 404, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(es_delete_data, make_get_request, es_write_data, query_data,
                      expected_answer):
    await es_write_data(films_data)
    response = await make_get_request('films/search', query_data)
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
    await es_delete_data()
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
