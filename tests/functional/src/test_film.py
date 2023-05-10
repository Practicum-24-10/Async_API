import pytest

from tests.functional.testdata.es_data import film

film_id = film[0]['id']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'id': film_id},
            {'status': 200, 'id': film_id}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search(es_delete_data, make_get_request, es_write_data,
                      query_data,
                      expected_answer):
    await es_write_data()
    id = query_data['id']
    response = await make_get_request(f'films/{id}')
    assert response['status'] == expected_answer['status']
    assert response['body']['uuid'] == expected_answer['id']
    await es_delete_data()
    response = await make_get_request(f'films/{id}')
    assert response['status'] == expected_answer['status']
    assert response['body']['uuid'] == expected_answer['id']
