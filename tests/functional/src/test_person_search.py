from http import HTTPStatus

import pytest
from tests.functional.testdata.es_data import film

film = film[0]


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': 'Walter Koenig', 'size': '60', 'page': '1'},
            {'status': HTTPStatus.OK, 'length': 1}
        ),
        (
            {'query': 'Walter Koenig', 'size': '60', 'page': '2'},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        ),
        (
            {'query': 'Boby Fisher', 'size': '60', 'page': '1'},
            {'status': HTTPStatus.OK, 'length': 60}
        ),
        (
            {'query': 'Mashed potato', 'size': '60', 'page': '1'},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        ),
        (
            {'query': 'Walter Koenig', 'size': '1', 'page': '-1'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        ),
        (
            {'query': 'Walter Koenig', 'size': '-1', 'page': '1'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        ),
        (
            {'query': 'Walter Koenig', 'size': '0', 'page': '1'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        ),
        (
            {'query': 'Walter Koenig', 'size': '1', 'page': '0'},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_person_search(es_delete_data, make_get_request, es_write_data,
                             query_data, expected_answer):
    async def run_assert():
        response = await make_get_request('persons/search/', query_data)
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
            {'query': 'Walter Koenig', 'size': '60', 'page': '1'},
            {'films_id': film['id'], 'roles': 'actor'}
        )
    ]
)
@pytest.mark.asyncio
async def test_person_search_check_content(
        es_delete_data, make_get_request, es_write_data, query_data, expected_answer):
    async def run_assert():
        response = await make_get_request('persons/search/', query_data)
        assert response['body'][0]['films'][0]['uuid'] == expected_answer['films_id']
        assert response['body'][0]['films'][0]['roles'][0] == expected_answer['roles']
    await es_write_data()
    await run_assert()
    await es_delete_data()
    await run_assert()
