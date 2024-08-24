# Bsw test task

## Запуск по шагам:
1) Запуск RabbitMQ
- Перейдите в папку rabbitmq: `cd rabbitmq`
- Создайте `.env` файл по примеру файла `.env.example`
- Запустите RabbitMQ: `docker compose up --build`
2) Запуск сервиса line-provider
- Перейдите в папку line-provider: `cd line-provider`
- Создайте `.env` файл по примеру файла `.env.example`
- Соберите docker образ: `docker build -t line-provider .`
- Запустите docker образ: `docker run -p 5000:5000 line-provider`
- SwaggerUI будет доступен по адресу `http://127.0.0.1:5000/docs`
3) Запуск сервиса bet-maker
- Перейдите в папку line-provider: `cd bet-maker`
- Создайте `.env` файл по примеру файла `.env.example`
- Соберите и запустите docker образ: `docker compose up --build`
- SwaggerUI будет доступен по адресу `http://127.0.0.1:8000/docs`

## Использованные технологии:
- Python 3.11
- FastAPI
- Pydantic
- PostgreSQL
- SqlAlchhemy & Alembic
- RabbitMQ & [FastStream](https://faststream.airt.ai/latest/)
- Docker

## TODO:
- Хранить события сервиса line-provider не в памяти, а в базе данных
- Реализовать логгирование
- Покрыть код тестами
- Нормализовать базу данных
