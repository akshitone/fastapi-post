import pytest
from jose import jwt
from app.models import schemas
from app.utils.config import settings
from tests.database import client, session


def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.parametrize('email, password', [
    ('user@example.com', 'string'),
    ('user1@example.com', 'string1'), ('user2@example.com', 'string2')
])
def test_create_user(client, email, password):
    response = client.post(
        '/api/v1/users/', json={"email": email, "password": password})

    new_user = schemas.UserResponse(**response.json())

    assert new_user.email == email
    assert response.status_code == 201


@pytest.fixture
def test_user(client):
    response = client.post('/api/v1/users/',
                           json={"email": "user@example.com", "password": "string"})

    new_user = schemas.UserResponse(**response.json())
    return new_user


def test_login_user(client, test_user):
    response = client.post(
        '/api/v1/auth/login', json={"email": "user@example.com", "password": "string"})

    login_response = schemas.Token(**response.json())

    user_data = jwt.decode(login_response.access_token,
                           settings.secret_key, algorithms=[settings.algorithm])
    id = str(user_data.get('user_id'))

    assert id == test_user.id
    assert login_response.token_type == 'bearer'
    assert response.status_code == 200


@pytest.mark.parametrize('email, password, status_code', [
    ('user@example.com', '', 422),
    ('', 'password', 422),
    ('user@example.com', 'wrong', 403),
    ('invalid@example.com', 'password', 403),
])
def test_incorrect_login_user(client, test_user, email, password, status_code):
    response = client.post(
        '/api/v1/auth/login', json={"email": email, "password": password})

    assert response.status_code == status_code


def test_get_users(client):
    response = client.get('/api/v1/users')

    print(response.json())
