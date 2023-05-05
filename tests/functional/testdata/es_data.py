import datetime
import uuid

es_data = [{
    'id': str(uuid.uuid4()),
    'imdb_rating': 8.5,
    'genre': ['Action', 'Sci-Fi'],
    'title': 'The Star',
    'description': 'New World',
    'director': ['Stan'],
    'actors_names': ['Ann', 'Bob'],
    'writers_names': ['Ben', 'Howard'],
    'actors': [
        {'id': '111', 'name': 'Ann'},
        {'id': '222', 'name': 'Bob'}
    ],
    'writers': [
        {'id': '333', 'name': 'Ben'},
        {'id': '444', 'name': 'Howard'}
    ],
    'created_at': datetime.datetime.now().isoformat(),
    'updated_at': datetime.datetime.now().isoformat(),
    'film_work_type': 'movie'
} for _ in range(60)]
