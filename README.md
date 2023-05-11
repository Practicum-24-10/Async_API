# Проектная работа 4 спринта

Для запуска приложения необходимо подготовить `.env` файл по примеру `.env.example` и выполнить команду `docker compose up`.
API должен быть доступен по адресу `localhost:8000/api/openapi`


Для запуска тестов в контейнере необходимо подготовить `.env` файл по примеру `.env.example` а также `tests/functional/.env` файл по примеру `tests/functional/.env.example` и выполнить команду `docker compose -f tests/functional/docker-compose.yml up`.

Для локального запуска тестов необходимо подготовить `.env` файл по примеру `.env.example`, в виртуальном окружении выполнить `pip install -r tests/functional/requirements.txt` и выполнить команду `docker compose -f tests/functional/docker-compose.dev.yml up`. Когда сервисы будут готовы, можно запустить тесты командой `pytest tests/functional/src/`
