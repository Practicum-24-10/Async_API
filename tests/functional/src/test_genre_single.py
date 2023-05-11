import pytest

from tests.functional.testdata.es_data import genre

genre_id = genre[0]['id']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'id': genre_id},
                {'status': 200, 'id': genre_id}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(make_get_request, es_write_data, query_data,
                      expected_answer, es_delete_data):
    await es_write_data()
    id = query_data['id']
    response = await make_get_request(f'genres/{id}')
    assert response['status'] == expected_answer['status']
    assert response['body']['uuid'] == expected_answer['id']
    await es_delete_data()
    response = await make_get_request(f'genres/{id}')
    assert response['status'] == expected_answer['status']
    assert response['body']['uuid'] == expected_answer['id']
