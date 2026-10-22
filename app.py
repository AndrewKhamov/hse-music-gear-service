"""Учебная заготовка: этот файл заполняем вместе на занятии."""
import os
from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI(title="Наш первый сервис")
load_dotenv()

# Шаг 1. Добавьте обработчик адреса /
# Подсказка:
@app.get("/")
def root():
     return {"message": "Сервис работает"}


# Шаг 2. Добавьте техническую проверку /health
# Она должна возвращать: {"status": "ok"}
@app.get("/health")
def health():
    return {"status": "ok"}


# Шаг 3. Добавьте /hello с параметром name
# Пример запроса: /hello?name=Anna
# Пример ответа: {"message": "Привет, Anna!"}
@app.get("/hello")
def hello(name: str = "Андрей"):
    return {"message": f"Привет, {name}!"}


# Шаг 4. Прочитайте APP_NAME и APP_AUTHOR из переменных окружения
# и верните их по адресу /info.
@app.get("/info")
def info():
    app_name = os.getenv("APP_NAME", "Учебный сервис")
    app_author = os.getenv("APP_AUTHOR", "Не указан")

    return {
        "app_name": app_name,
        "author": app_author,
    }
