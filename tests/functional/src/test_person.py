import pytest

from tests.functional.testdata.es_data import person

test_person = person[0]
person_id_2 = person[1]['id']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'size': '60', 'page': '1'},
                {'status': 200, 'length': 3, 'len_films': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_person_get_by_id(es_delete_data, make_get_request,
                                es_write_data,
                                query_data,
                                expected_answer):
    """
    Поиск конкретного человека;
    """

    async def run_assert(person):
        _id = test_person['id']
        response = await make_get_request(f'persons/{_id}', query_data)
        assert response['status'] == expected_answer['status']
        assert len(response['body']) == expected_answer['length']
        assert len(response['body']['films']) == expected_answer['len_films']
        assert response['body']['uuid'] == person['id']
        assert response['body']['full_name'] == person['full_name']

    await es_write_data()
    await run_assert(test_person)
    await es_delete_data()
    await run_assert(test_person)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'size': '60', 'page': '1'},
                {'status': 200, 'length': 1,
                 'uuid': 'cde7b6ff-32de-4807-8cd4-be95682e1ed9',
                 'title': 'The Moon', 'imdb_rating': 7.9}
        )
    ]
)
@pytest.mark.asyncio
async def test_person_film_get_by_id(es_delete_data, make_get_request,
                                     es_write_data,
                                     query_data,
                                     expected_answer):
    """
    поиск всех фильмов с участием человека;
    """

    async def run_assert(person):
        _id = person['id']
        response = await make_get_request(f'persons/{_id}/film', query_data)
        assert response['status'] == expected_answer['status']
        assert len(response['body']) == expected_answer['length']
        assert response['body'][0]['uuid'] == expected_answer['uuid']
        assert response['body'][0]['title'] == expected_answer['title']
        assert response['body'][0]['imdb_rating'] == expected_answer[
            'imdb_rating']

    await es_write_data()
    await run_assert(test_person)
    await es_delete_data()
    await run_assert(test_person)


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
async def test_person_valid(es_delete_data, make_get_request, es_write_data,
                            query_data,
                            expected_answer):
    """
    все граничные случаи по валидации данных;
    """
    async def run_assert(person):
        _id = person['id']
        response = await make_get_request(f'persons/{_id}/film', query_data)
        assert response['status'] == expected_answer['status']
        assert len(response['body']) == expected_answer['length']
        response = await make_get_request(f'persons/{_id}', query_data)
        assert response['status'] == expected_answer['status']
        assert len(response['body']) == expected_answer['length']
    await es_write_data()
    await run_assert(test_person)
    await es_delete_data()
    await run_assert(test_person)
