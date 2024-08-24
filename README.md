# Bsw test task

## Запуск по шашгам:
0) Склонируйте данный репозиторий: ``
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
2) Запуск сервиса bet-maker
- Перейдите в папку line-provider: `cd bet-maker`
- Создайте `.env` файл по примеру файла `.env.example`
- Соберите и запустите docker образ: `docker compose up --build`
- SwaggerUI будет доступен по адресу `http://127.0.0.1:8000/docs`
