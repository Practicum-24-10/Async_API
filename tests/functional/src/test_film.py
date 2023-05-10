import pytest

from tests.functional.testdata.es_data import film

film = film[0]


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'id': film['id']},
            {'status': 200, 'id': film['id'], 'title': film['title']}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_film_by_id(es_delete_data, make_get_request, es_write_data,
                              query_data, expected_answer):
    await es_write_data()
    id = query_data['id']
    response = await make_get_request(f'films/{id}')
    assert response['status'] == expected_answer['status']
    assert response['body']['uuid'] == expected_answer['id']
    assert response['body']['title'] == expected_answer['title']
    await es_delete_data()
    response = await make_get_request(f'films/{id}')
    assert response['status'] == expected_answer['status']
    assert response['body']['uuid'] == expected_answer['id']
    assert response['body']['title'] == expected_answer['title']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {
                'sort': 'imdb_rating',
                'page': '1',
                'size': '10',
                'genre': film['genres'][1]['id']
            },
            {'status': 200, 'size': 10}
        ),
        (
            {'sort': '-imdb_rating', 'page': '2', 'size': '20'},
            {'status': 200, 'size': 20}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_films_at_home_page(es_delete_data, make_get_request,
                                      es_write_data, query_data, expected_answer):
    await es_write_data()
    response = await make_get_request('films/', params=query_data)
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['size']
    await es_delete_data()
    response = await make_get_request('films/', params=query_data)
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['size']
