import requests
import pytest

BASE_URL = 'https://api-c-lemmens.cloud.okteto.net'  # Update this to your Flask app's address

def test_get_all_todos():
    r = requests.get(f'{BASE_URL}/todos')
    assert r.status_code == 200
    assert isinstance(r.json()['todos'], list)

def test_get_single_todo():
    # Assume that there is a Todo with id 1
    r = requests.get(f'{BASE_URL}/todos/1')
    assert r.status_code == 200
    assert 'id' in r.json()['todo']
    assert 'task' in r.json()['todo']

def test_get_completed_todos():
    r = requests.get(f'{BASE_URL}/todos/completed')
    assert r.status_code == 200
    assert isinstance(r.json()['todos'], list)

def test_create_todo():
    new_todo = {'task': 'Test todo'}
    r = requests.post(f'{BASE_URL}/todos', json=new_todo)
    assert r.status_code == 201
    assert 'id' in r.json()['todo']
    assert r.json()['todo']['task'] == 'Test todo'

def test_update_todo():
    updated_data = {'task': 'Updated task', 'completed': True}
    # Assume that there is a Todo with id 1
    r = requests.put(f'{BASE_URL}/todos/1', json=updated_data)
    assert r.status_code == 200
    assert r.json()['todo']['task'] == 'Updated task'
    assert r.json()['todo']['completed'] is True

def test_delete_todo():
    # Assume that there is a Todo with id 1 to be deleted
    r = requests.delete(f'{BASE_URL}/todos/1')
    assert r.status_code == 200
    assert r.json()['result'] == 'Successfully deleted'

def test_register_user():
    new_user = {'username': 'test_user', 'password': 'test_password'}
    r = requests.post(f'{BASE_URL}/register', json=new_user)
    assert r.status_code == 200
    assert r.json()['message'] == 'User registered'

def test_login():
    user_credentials = {'username': 'test_user', 'password': 'test_password'}
    r = requests.post(f'{BASE_URL}/login', json=user_credentials)
    assert r.status_code == 200
    assert r.json()['message'] == 'Logged in'

@pytest.mark.parametrize("user_credentials, expected_status_code", [
    ({"username": "wrong_user", "password": "test_password"}, 401),
    ({"username": "test_user", "password": "wrong_password"}, 401),
])
def test_login_failures(user_credentials, expected_status_code):
    r = requests.post(f'{BASE_URL}/login', json=user_credentials)
    assert r.status_code == expected_status_code
    assert r.json()['error'] == 'Invalid username or password'
