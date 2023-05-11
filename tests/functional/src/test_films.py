import pytest

from tests.functional.testdata.es_data import film

film = film[0]
id_not_existing_genre = "b04d45e4-e7bd-417e-a700-0049e8cae9e6"


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {
                'sort': 'imdb_rating',
                'page': '1',
                'size': '1',
                'genre': film['genres'][1]['id']
            },
            {'status': 200, 'size': 1}
        ),
        (
            {
                'sort': 'imdb_rating',
                'page': '1',
                'size': '1',
                'genre': id_not_existing_genre
            },
            {'status': 404, 'size': 1}
        ),
        (
            {'sort': '-imdb_rating', 'page': '2', 'size': '20'},
            {'status': 200, 'size': 20}
        ),
        (
            {'sort': '-imdb_rating', 'size': '1', 'page': '-1'},
            {'status': 422, 'size': 1}
        ),
        (
            {'sort': '-imdb_rating', 'size': '-1', 'page': '1'},
            {'status': 422, 'size': 1}
        ),
        (
            {'sort': '-imdb_rating', 'size': '0', 'page': '1'},
            {'status': 422, 'size': 1}
        ),
        (
            {'sort': '-imdb_rating', 'size': '1', 'page': '0'},
            {'status': 422, 'size': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_films(es_delete_data, make_get_request,
                     es_write_data, query_data, expected_answer):
    async def run_asseert():
        response = await make_get_request('films/', params=query_data)
        assert response['status'] == expected_answer['status']
        assert len(response['body']) == expected_answer['size']
    await es_write_data()
    await run_asseert()
    await es_delete_data()
    await run_asseert()


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {
                'sort': 'imdb_rating',
                'page': '1',
                'size': '1',
                'genre': film['genres'][1]['id']
            },
            {'id': film['id'], 'title': film['title'], 'imdb_rating': film['imdb_rating']}
        ),
        (
            {
                'sort': 'imdb_rating',
                'page': '1',
                'size': '1'
            },
            {'id': film['id'], 'title': film['title'], 'imdb_rating': film['imdb_rating']}
        )
    ]
)
@pytest.mark.asyncio
async def test_films_check_content(
        es_delete_data, make_get_request, es_write_data, query_data, expected_answer):
    async def run_assert():
        response = await make_get_request('films/', query_data)
        assert response['body'][0]['uuid'] == expected_answer['id']
        assert response['body'][0]['title'] == expected_answer['title']
        assert response['body'][0]['imdb_rating'] == expected_answer['imdb_rating']
    await es_write_data()
    await run_assert()
    await es_delete_data()
    await run_assert()
