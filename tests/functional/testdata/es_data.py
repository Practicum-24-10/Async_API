import uuid

film = [{
  "id": 'cde7b6ff-32de-4807-8cd4-be95682e1ed9',
  "title": "The Moon",
  "imdb_rating": 7.9,
  "description": "When a seemingly unstoppable new enemy threatens the very ",
  "genres": [
    {
      "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
      "name": "Action"
    },
    {
      "id": "6c162475-c7ed-4461-9184-001ef3d9f26e",
      "name": "Sci-Fi"
    }
  ],
  "directors": [
    {
      "id": "b14dece3-a90b-4e66-bd49-7ab6282b3b46",
      "name": "Lebed Nikolaev"
    }
  ],
  "actors": [
    {
      "id": "a6165ca2-6f23-4753-8e49-04e26e9eb633",
      "name": "Adrienne Wilkinson"
    },
    {
      "id": "d9162823-9df0-4b03-bbab-272601eba66c",
      "name": "Walter Koenig"
    }
  ],
  "writers": [
    {
      "id": "9b8804c3-1403-41bb-84c3-d31bffa65501",
      "name": "Ethan H. Calk"
    },
    {
      "id": "d49684b8-9dba-4e1a-bdd6-3f64852c0883",
      "name": "Jack Treviño"
    },
  ]
}]

films_data = film + [{
  "id": str(uuid.uuid4()),
  "title": "The Star",
  "imdb_rating": 4.9,
  "description": "When a seemingly unstoppable new enemy threatens the very ",
  "genres": [
    {
      "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
      "name": "Action"
    },
    {
      "id": "6c162475-c7ed-4461-9184-001ef3d9f26e",
      "name": "Sci-Fi"
    }
  ],
  "directors": [
    {
      "id": "b14dece3-a90b-4e66-bd49-7ab6282b3b46",
      "name": "Nikolay Lebedev"
    }
  ],
  "actors": [
    {
      "id": "a6165ca2-6f23-4753-8e49-04e26e9eb633",
      "name": "Adrienne Wilkinson"
    },
    {
      "id": "d9162823-9df0-4b03-bbab-272601eba66c",
      "name": "Walter Koenig"
    }
  ],
  "writers": [
    {
      "id": "9b8804c3-1403-41bb-84c3-d31bffa65501",
      "name": "Ethan H. Calk"
    },
    {
      "id": "d49684b8-9dba-4e1a-bdd6-3f64852c0883",
      "name": "Jack Treviño"
    },
  ]
} for _ in range(60)]
