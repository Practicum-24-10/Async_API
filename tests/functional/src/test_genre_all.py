import pytest


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'size': '1000', 'page': '1'},
                {'status': 200, 'length': 62}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(es_delete_data, make_get_request, es_write_data,
                      query_data,
                      expected_answer):
    await es_write_data()
    response = await make_get_request('genres', query_data)
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
    await es_delete_data()
    response = await make_get_request('genres', query_data)
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
