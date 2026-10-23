import os
from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI(title="Наш первый сервис")
load_dotenv()

# Шаг 1. Обработчик адреса 
@app.get("/")
def root():
     return {"message": "Сервис работает"}


# Шаг 2. Техническая проверка
@app.get("/health")
def health():
    return {"status": "ok"}


# Шаг 3. /hello с параметром name
# Пример запроса: /hello?name=Anna
@app.get("/hello")
def hello(name: str = "Андрей"):
    return {"message": f"Привет, {name}!"}


# Шаг 4. Информация о проекте
@app.get("/info")
def info():
    app_name = os.getenv("APP_NAME", "Учебный сервис")
    app_author = os.getenv("APP_AUTHOR", "Не указан")

    return {
        "app_name": app_name,
        "author": app_author,
    }

# Шаг 5. Версия проекта
@app.get('/version')
def version():
    return {'version': '0.1.0'}