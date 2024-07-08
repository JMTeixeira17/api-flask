import json
import pytest
from .conftest import generate_jwt_token

@pytest.mark.run(order=1)
def test_register(client):
    password = "password"
    new_user = {
        "username": "john_doe",
        "email": "john.doe@example.com",
        "password_hash": password
    }
    response = client.post('/api/register', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == new_user["username"]
    assert data["email"] == new_user["email"]
    assert "id" in data

@pytest.mark.run(order=2)
def test_login(client):
    password = "password"

    user_data = {
        "username": "john_doe",
        "password_hash": password
    }
    response = client.post('/api/login', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

@pytest.mark.run(order=3)
def test_get_user(client, secret_key):
    login_data = {
        "username": "john_doe",
        "password_hash": "password"
    }
    login_response = client.post('/api/login', data=json.dumps(login_data), content_type='application/json')
    assert login_response.status_code == 200
    login_data = login_response.get_json()
    token = login_data['access_token']
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = client.get('/api/user', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'username' in data

@pytest.mark.run(order=4)
def test_update_user(client):
    login_data = {
         "username": "john_doe",
         "password_hash": "password"
    }
    login_response = client.post('/api/login', data=json.dumps(login_data), content_type='application/json')
    assert login_response.status_code == 200
    login_data = login_response.get_json()
    token = login_data['access_token']
    update_data = {
        "username": "john_doe_updated",
        "email": "johndoe_updated@example.com"
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = client.put('/api/user', data=json.dumps(update_data), headers=headers, content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User updated"

@pytest.mark.run(order=5)
def test_delete_user(client):
    login_data = {
        "username": "john_doe_updated",
        "password_hash": "password"
    }
    login_response = client.post('/api/login', data=json.dumps(login_data), content_type='application/json')
    assert login_response.status_code == 200
    login_data = login_response.get_json()
    token = login_data['access_token']
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = client.delete('/api/user', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User deleted"

