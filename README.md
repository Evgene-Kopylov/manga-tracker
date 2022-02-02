## manga tracker
Сервис для отслеживания обновлений манги, 
с возможностью добавлять новые сценарии 
парсинга с помощью расширения хром.

Представляет собой автоматизированный парсер, 
спроектированный для отслеживания изменений в указанном 
блоке страницы.
Приложение хром используется для создания сценария парсинга.

## Запуск локально

## Переменные окружения

- `POSTGRES_DB`=manga_tracker_db
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `SECRET_KEY`
- `POSTGRES_SERVER`=localhost
- `POSTGRES_PORT`=5432
- `POSTGRES_TEST_PORT`=5444
- `LOCAL_DEV` - set `1` if runs locally, ignore if not.
- `AMQP_URL`=amqp://guest:guest@localhost:5672/
- `DISCORD_WEBHOOK_URL` - discord server for debug logs

## Структура проекта

Контейнеры:
- `manga_tracker` - FastApi based web app 
- `instant_parser` - Контейнер для быстрой обработки запроса на парсинг
- `manga_parser` - Котейнер для парсинга по расписанию
- `db` - postgres
- `rabbitmq` - обмен сообщений внутри сервиса
- `selenium-hub` - selenium docker
    - `firefox`
    - `chrome`

## Миграции
Alembic

## Тестирование
```commandline
cd fastapi
pytest
```

