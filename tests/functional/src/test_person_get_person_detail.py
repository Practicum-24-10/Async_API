import pytest
import uuid

from tests.functional.testdata.es_data import person

person_id_1 = person[0]['id']
person_id_2 = person[1]['id']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'id': person_id_1},
                {'status': 200, 'length': 1}
        ),
        (
                {'id': person_id_2},
                {'status': 200, 'length': 1}
        ),
        (
                {'id': str(uuid.uuid4())},
                {'status': 404, 'length': 0}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search(es_delete_data, make_get_request, es_write_data,
                      query_data,
                      expected_answer):
    await es_write_data()
    id = query_data['id']
    response = await make_get_request(f'persons/{id}', query_data)
    assert response['status'] == expected_answer['status']
    try:
        films_len = len(response['body']['films'])
    except KeyError:
        films_len = 0
    assert films_len == expected_answer['length']
    await es_delete_data()
    response = await make_get_request(f'persons/{id}', query_data)
    assert response['status'] == expected_answer['status']
    try:
        films_len = len(response['body']['films'])
    except KeyError:
        films_len = 0
    assert films_len == expected_answer['length']
