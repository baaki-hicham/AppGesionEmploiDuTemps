import pytest
from app import create_app


def test_app_creates():
    app = create_app()
    assert app is not None


def test_login_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Connexion' in response.data
