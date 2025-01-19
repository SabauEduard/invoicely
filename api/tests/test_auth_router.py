import pytest
from fastapi.testclient import TestClient
from fastapi import status

from main import app  # Assuming your FastAPI app is in main.py

def test_login_success():
    with TestClient(app) as client:
        response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    with TestClient(app) as client:
        response = client.post("/login", data={"username": "wronguser", "password": "wrongpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials"}

def test_enable_2fa_success():
    with TestClient(app) as client:
        response = client.post("/enable-2fa", json={"user_id": 1})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"description": "2FA enabled successfully"}

def test_enable_2fa_user_not_found():
    with TestClient(app) as client:
        response = client.post("/enable-2fa", json={"user_id": 999})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"description": "User not found"}

def test_disable_2fa_success():
    with TestClient(app) as client:
        response = client.post("/disable-2fa", json={"user_id": 1})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"description": "2FA disabled successfully"}

def test_disable_2fa_user_not_found():
    with TestClient(app) as client:
        response = client.post("/disable-2fa", json={"user_id": 999})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"description": "User not found"}

def test_refresh_token_success():
    with TestClient(app) as client:
        response = client.get("/refresh", cookies={"auth_cookie": "valid_token"})
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

def test_refresh_token_invalid():
    with TestClient(app) as client:
        response = client.get("/refresh", cookies={"auth_cookie": "invalid_token"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Invalid token"}

def test_logout_success():
    with TestClient(app) as client:
        response = client.post("/logout")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_get_current_user_success():
    with TestClient(app) as client:
        response = client.get("/current-user", cookies={"auth_cookie": "valid_token"})
    assert response.status_code == status.HTTP_201_CREATED
    assert "username" in response.json()
