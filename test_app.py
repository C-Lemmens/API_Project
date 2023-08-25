import requests
import pytest

BASE_URL = 'https://api-c-lemmens.cloud.okteto.net'  # Update this to your Flask app's address

def test_get_todos():
    response = requests.get(f"{BASE_URL}/todos")
    assert response.status_code == 200
    assert 'todos' in response.json()

def test_add_todo():
    new_task = {'task': 'Test Task'}
    response = requests.post(f"{BASE_URL}/todos", json=new_task)
    assert response.status_code == 201
    assert 'task' in response.json()['todo']

def test_update_todo():
    todo_id = 1  # Replace with a real todo ID
    updated_data = {'task': 'Updated Test Task'}
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()['todo']['task'] == 'Updated Test Task'

def test_delete_todo():
    todo_id = 1  # Replace with a real todo ID
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    assert response.status_code == 200

def test_register():
    register_data = {'username': 'test', 'password': 'test123'}
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    assert response.status_code == 200
    assert 'message' in response.json()

def test_login():
    login_data = {'username': 'test', 'password': 'test123'}
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 200
    assert 'message' in response.json()

