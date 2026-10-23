import json
import os
from datetime import date

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

APP_VERSION = '1.0.0'
DATA_FILE = 'deadlines.json'

app = FastAPI(
    title=os.getenv('APP_NAME', 'Учебные дедлайны'),
    version=APP_VERSION,
)

# Получаем текущую дату
def current_date():
    return date.today()

# Читаем json файл со списком дедлайнов
def read_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

# Перезаписываем json файл
def write_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# Меняем строковый формат дедлайна на дату 
def deadline_date(deadline):
    return date.fromisoformat(deadline['due_date'])


@app.get('/')
def root():
    return {'message': 'Трекер учебных дедлайнов', 'docs': '/docs'}


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/version')
def version():
    return {'version': APP_VERSION}


@app.get('/info')
def info():
    return {
        'app_name': os.getenv('APP_NAME', 'Учебные дедлайны'),
        'author': os.getenv('APP_AUTHOR', 'Не указан'),
    }

# Метод для добавления нового дедлайна с указанием предмета, даты и описания
@app.post('/deadlines', status_code=201)
def create_deadline(subject: str, due_date: date, description: str):
    subject = subject.strip()
    description = description.strip()
    if not subject or not description:
        raise HTTPException(status_code=400, detail='Укажи предмет и описание')
    if due_date < current_date():
        raise HTTPException(status_code=400, detail='Дата уже прошла')

    data = read_data()
    item = {
        'id': data['next_id'],
        'subject': subject,
        'due_date': due_date.isoformat(),
        'description': description,
    }
    data['deadlines'].append(item)
    data['next_id'] += 1
    write_data(data)
    return item

# Метод для получения списка актуальных дедлайнов на текущую дату
@app.get('/deadlines')
def list_deadlines():
    data = read_data()
    today = current_date()
    result = []
    for deadline in data['deadlines']:
        if deadline_date(deadline) >= today:
            result.append(deadline)
    result.sort(key=deadline_date)
    return result

# Метод для получения информации о дедлайне по ID 
@app.get('/deadlines/{deadline_id}')
def get_deadline(deadline_id: int):
    data = read_data()
    for deadline in data['deadlines']:
        if deadline['id'] == deadline_id:
            return deadline
    raise HTTPException(status_code=404, detail='Дедлайн не найден')

# Метод получения списка предметов с актуальными дедлайнами
@app.get('/subjects')
def subjects():
    data = read_data()
    today = current_date()
    result = []
    for deadline in data['deadlines']:
        if deadline_date(deadline) >= today:
            if deadline['subject'] not in result:
                result.append(deadline['subject'])
    return sorted(result)