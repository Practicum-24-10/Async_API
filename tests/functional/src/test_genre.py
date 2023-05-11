import pytest

from tests.functional.testdata.es_data import genre

genre_id = genre[0]['id']


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
async def test_genre_all(es_delete_data, make_get_request, es_write_data,
                         query_data,
                         expected_answer):
    """
    вывести все жанры;
    """

    async def run_assert():
        response = await make_get_request('genres', query_data)
        assert response['status'] == expected_answer['status']
        assert len(response['body']) == expected_answer['length']

    await es_write_data()
    await run_assert()
    await es_delete_data()
    await run_assert()


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
async def test_genre_single(make_get_request, es_write_data, query_data,
                            expected_answer, es_delete_data):
    """
    поиск конкретного жанра;
    """

    async def run_assert(genre_id):
        response = await make_get_request(f'genres/{genre_id}')
        assert response['status'] == expected_answer['status']
        assert response['body']['uuid'] == expected_answer['id']

    await es_write_data()
    await run_assert(genre_id)
    await es_delete_data()
    await run_assert(genre_id)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'size': '1', 'page': '-1'},
                {'status': 422, 'length': 1}
        ),

        (
                {'size': '-1', 'page': '1'},
                {'status': 422, 'length': 1}
        ),
        (
                {'size': '0', 'page': '1'},
                {'status': 422, 'length': 1}
        ),
        (
                {'size': '1', 'page': '0'},
                {'status': 422, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(es_delete_data, make_get_request, es_write_data,
                      query_data,
                      expected_answer):
    """
    все граничные случаи по валидации данных;
    """
    async def run_assert():
        response = await make_get_request('genres', query_data)
        assert response['status'] == expected_answer['status']
        assert len(response['body']) == expected_answer['length']
    await es_write_data()
    await run_assert()
    await es_delete_data()
    await run_assert()
