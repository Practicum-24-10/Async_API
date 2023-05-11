import pytest

from tests.functional.testdata.es_data import film

film = film[0]
id_not_existing_film = '6c162475-c7ed-4461-9184-001ef3d9f26e'


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'id': film['id']},
            {'status': 200}
        ),
        (
            {'id': 'notValidId'},
            {'status': 422}
        ),
        (
            {'id': id_not_existing_film},
            {'status': 404}
        ),
    ]
)
@pytest.mark.asyncio
async def test_films_film_id(
        es_delete_data, make_get_request, es_write_data, query_data, expected_answer):
    id = query_data['id']

    async def run_assert():
        response = await make_get_request(f'films/{id}')
        assert response['status'] == expected_answer['status']
    await es_write_data()
    await run_assert()
    await es_delete_data()
    await run_assert()


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'id': film['id']},
            {'film': film}
        ),
    ]
)
@pytest.mark.asyncio
async def test_films_film_id_check_content(
        es_delete_data, make_get_request, es_write_data, query_data, expected_answer):
    id = query_data['id']

    async def run_assert():
        response = await make_get_request(f'films/{id}')
        response['body']['id'] = response['body'].pop('uuid')
        assert response['body'] == expected_answer['film']
    await es_write_data()
    await run_assert()
    await es_delete_data()
    await run_assert()
