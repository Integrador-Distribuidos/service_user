# tests/test_openapi.py
from dotenv import load_dotenv
import httpx
import pytest
import json
from termcolor import colored
from tests.generate_jwt import create_test_token
import os
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users_service.users.models import User  # ajuste conforme seu app
load_dotenv()

AUTH_TOKEN = create_test_token()
HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}

BASE_URL = os.getenv("BASE_URL", "http://localhost:8001")

@pytest.fixture
def api_client():
    """Retorna uma instância do DRF APIClient para fazer requisições."""
    return APIClient()

@pytest.fixture
def user(db):
    """Cria e retorna um usuário para testes."""
    return User.objects.create_user(
        email="testuser@example.com",
        password="testpass123"
    )

@pytest.fixture
def auth_client(api_client, user):
    """Retorna um APIClient autenticado com o usuário criado."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture(scope="session")
def openapi():
    r = httpx.get(f"{BASE_URL}/openapi.json")
    r.raise_for_status()
    return r.json()

def pretty_print_result(method, url, status_code, response_text):
    color = "green" if status_code < 400 else "yellow" if status_code < 500 else "red"
    print(colored(f"\n[{method}] {url} -> {status_code}", color))
    print(colored(f"Response:", "cyan"))
    print(response_text[:500] + ("..." if len(response_text) > 500 else ""))

def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

def test_user_list(auth_client):
    url = reverse('user-list')  # deve ser o nome exato da url
    response = auth_client.get(url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_user_detail(auth_client, user):
    url = reverse('user-detail', kwargs={'pk': user.pk})
    response = auth_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == user.pk
    assert data['email'] == user.email

def test_user_me(auth_client, user):
    url = reverse('user-me')
    response = auth_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == user.pk

def test_make_admin(auth_client, user):
    url = reverse('user-make-admin', kwargs={'pk': user.pk})
    response = auth_client.post(url)
    assert response.status_code == 200 or response.status_code == 204
    user.refresh_from_db()
    assert user.is_staff is True  # ou outro campo que seu sistema use para admin

def test_update_cpf(auth_client, user):
    url = reverse('user-update-cpf', kwargs={'pk': user.pk})
    new_cpf = "123.456.789-00"
    response = auth_client.post(url, data={"cpf": new_cpf})
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.cpf == new_cpf

def test_unauthenticated_access(api_client):
    url = reverse('user-list')
    response = api_client.get(url)
    assert response.status_code == 401  # Unauthorized, pois não autenticado

def test_auth_token(api_client, user):
    url = reverse('obtain_auth_token')
    response = api_client.post(url, data={"username": user.username, "password": "testpass123"})
    assert response.status_code == 200
    assert "token" in response.json()