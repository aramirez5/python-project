from todo import app
from bs4 import BeautifulSoup

def test_index():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_add_task():
    client = app.test_client()
    response = client.post('/add', data={'task': 'Task 1'})
    assert response.status_code == 200
    assert b'Task 1' in response.data

def test_add_existing_task():
    client = app.test_client()
    client.post('/add', data={'task': 'Task 1'})
    response = client.post('/add', data={'task': 'Task 1'})
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    error_message = soup.find('div', {'class': 'error'}).text.strip()
    assert error_message == 'La tarea "Task 1" ya existe.'

def test_delete_task():
    client = app.test_client()
    client.post('/add', data={'task': 'Task 1'})
    response = client.post('/delete', data={'task': 'Task 1'})
    assert response.status_code == 200

def test_delete_nonexistent_task():
    client = app.test_client()
    response = client.post('/delete', data={'task': 'Task 1'})
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    error_message = soup.find('div', {'class': 'error'}).text.strip()
    assert error_message == 'La tarea "Task 1" no existe.'
