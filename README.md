## manga tracker
Сервис для отслеживания обновлений манги, 
с возможностью добавлять новые сценарии парсинга с помощью расширения хром.

Представляет собой автоматизированный парсер, спроектированный для отслеживания изменений в указанном блоке страницы.
Приложение хром используется для создания сценария парсинга.

## Запуск локально

1. Помести файл .env в папку проекта, рядом с docker-compose.yml.
2. Запустить проект используя docker-compose.yml
3. При первом запуске, провести миграцию Alembic

Для добавления элемента в список отслеживания использовать [расширение браузера][tool]

[tool]: https://github.com/Evgene-Kopylov/manga-garden-tool

## Переменные окружения

Все переменные имуют значенмя по-умолчанию. Можно оставить .env пустым.

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

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

```commandline
cd web_app
alembic upgrade head
```

## Тестирование

```commandline
cd web_app
pytest
```

