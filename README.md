_Задание выполнено в срок (до 9:30 05.07)_
[openapi.json](https://github.com/sanchoouse1/ad-server/blob/master/openapi.json)

# Выбранный стек технологий
Бэкенд: FastAPI
СУБД Postgres (_версия 15_), SQLAlchemy + Alembic
python 3.12

# Как развернуть проект
### 1. Клонировать репозиторий:
```bash
git clone https://github.com/sanchoouse1/ad-server.git
```
### 2. Перейти в клонированный репо
`cd ad-server`
### 3. Настройка переменных окружения
Нам нужны два файла. 
- Создаём файл `ad-server/.env` в корне проекта (прокидывать переменные окружения в контейнеры):
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=mydatabase

DB_HOST="db"
DB_PORT=5432
DB_USER="postgres"
DB_PASS="password"
DB_NAME="mydatabase"
```
- Создаём файл `ad-server/fastapi/.env` (используется для конфигурации настроек fastapi-приложения):
```
# Генерируем секретный ключ openssl rand -hex 32, тестовый пример:
SECRET_KEY="f760ee781dfee35ffe46e02be494694cf19b3726f3e2ab995d70bb8fd3eeee87"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

DB_HOST="db"
DB_PORT=5432
DB_USER="postgres"
DB_PASS="password"
DB_NAME="mydatabase"
```
4. Запустить контейнеры (БД + FastAPI)
```bash
docker-compose up -d
```
5. Выполнить миграции Alembic внутри контейнера backend
```bash
docker exec -it adserver_backend bash
```
```bash
alembic upgrade head
```
6. Проверить работу сервиса
Swagger UI: `http://localhost:8000/api/docs`

# Реализованный функционал
- Реализован весь основной функционал
- Частично реализован дополнительный функционал:
  -  Фильтрация объявлений
  -  Авторизация с помощью JWT-токена
  -  Отзыв на размещенное объявление
  -  Сборка проекта в докер-образ

<details><summary><h3><code>Содержимое файла `requirements.txt`</code></h3></summary>
_Запрошено в ТЗ_

fastapi[all]==0.115.14
  
uvicorn==0.34.3

sqlalchemy==2.0.41

asyncpg==0.30.0

alembic==1.16.2

shortuuid==1.0.13

PyJWT==2.9.0
</details>

<details><summary><h3><code>Файловая структура проекта</code></h3></summary>
`enpoints/` # API-эндпоинты
`services/` # Сервисы
</details>
