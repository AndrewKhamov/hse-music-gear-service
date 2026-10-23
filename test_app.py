from datetime import date, timedelta

from fastapi.testclient import TestClient
from app_final import app, write_data

client = TestClient(app)


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


# Тест получения списка дедлайнов 
# Не перезаписывает реальный json файл с дедлайнами
# Использует созданные для теста данные и пишет их во временную папку
def test_deadlines(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    # Подготовка синтетических данных
    data = {
        'next_id': 4,
        'deadlines': [
            {'id': 1, 'subject': 'Дискретные и непрерывные структуры', 'due_date': tomorrow.isoformat(),
             'description': 'Сдать завтра'},
            {'id': 2, 'subject': 'Программирование на Python', 'due_date': yesterday.isoformat(),
             'description': 'Срок прошёл'},
            {'id': 3, 'subject': 'Инфраструктура и администрирование', 'due_date': today.isoformat(),
             'description': 'Сдать сегодня'},
        ],
    }
    write_data(data)

    # Выполнение проверки (получение данных + корректная сортировка)
    response = client.get('/deadlines')
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['id'] == 3
    assert response.json()[1]['id'] == 1


# Тест добавления дедлайна
# Также не работает с реальными данными
def test_create_deadline(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_data({'next_id': 1, 'deadlines': []})
    due_date = (date.today() + timedelta(days=1)).isoformat()

    # Проверяем создание записи
    response = client.post('/deadlines', params={
        'subject': 'Дискретные и непрерывные структуры',
        'due_date': due_date,
        'description': 'Сдать домашнее задание',
    })
    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'subject': 'Дискретные и непрерывные структуры',
        'due_date': due_date,
        'description': 'Сдать домашнее задание',
    }

    # Проверяем наличие созданной записи по Id
    saved = client.get('/deadlines/1')
    assert saved.status_code == 200
    assert saved.json() == response.json()

# Тест обработки некорректной даты
def test_invalid_date():
    response = client.post('/deadlines', params={
        'subject': 'Дискретные и непрерывные структуры',
        'due_date': 'не-дата',
        'description': 'Сдать домашнее задание',
    })
    assert response.status_code == 422