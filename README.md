## manga tracker
Сервис для отслеживания обновлений манги, 
с возможностью добавлять новые сценарии парсинга с помощью расширения хром.

Представляет собой автоматизированный парсер, спроектированный для отслеживания изменений в указанном блоке страницы.
Приложение хром используется для создания сценария парсинга.

## Запуск локально

Помести файл .env в папку проекта, рядом с docker-compose.yml.

Запустить проект используя docker-compose.yml

## Переменные окружения

Все переменные имуют значенмя по-умолчанию. Можно оставить .env пустым.

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

- `POSTGRES_SERVER`
- `POSTGRES_PORT`

- `LOCAL_DEV` - set `1` if runs locally, ignore if not.
- `AMQP_URL`= amqp://guest:guest@localhost:5672/
- `DISCORD_WEBHOOK_URL` - discord server for debug logs

## Структура проекта

Контейнеры:

- `web_app` - FastApi based web app
- `manga_parser` - Контейнер для быстрой обработки запроса на парсинг по запросу через RabbitMQ
- `db` - postgres
- `rabbitmq` - обмен сообщений внутри сервиса
- `selenium-hub` - selenium docker
  - `firefox`
  - `chrome`

## Миграции
Alembic

## Тестирование
```commandline
cd web_app
pytest
```

