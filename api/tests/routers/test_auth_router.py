from unittest.mock import AsyncMock, patch, MagicMock
import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient
from main import app
from services.auth_service import AuthService

client = TestClient(app)

@pytest.fixture
def mock_db():
    return AsyncMock()

@pytest.fixture
def mock_form_data():
    return OAuth2PasswordRequestForm(
        username="test@example.com",
        password="password123",
        scope="",
        client_id=None,
        client_secret=None
    )

def test_login_success(mock_db, mock_form_data):
    expected_response = {"access_token": "test_token", "token_type": "bearer"}
    
    with patch.object(AuthService, 'login', return_value=expected_response) as mock_login:
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "password123"}
        )
        
        assert response.status_code == 200
        assert response.json() == expected_response
        mock_login.assert_called_once()

def test_login_invalid_credentials(mock_db, mock_form_data):
    with patch.object(AuthService, 'login', side_effect=HTTPException(status_code=401, detail="Invalid credentials")):
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "wrong_password"}
        )
        
        assert response.status_code == 401

def test_enable_2fa_success(mock_db):
    expected_response = {"otp_secret": "test_secret", "qr_code": "test_qr_code"}
    
    with patch.object(AuthService, 'enable_2fa', return_value=expected_response) as mock_enable:
        response = client.post("/auth/enable-2fa", params={"user_id": 1})
        
        assert response.status_code == 200
        assert response.json() == expected_response

def test_disable_2fa_success(mock_db):
    expected_response = {"message": "2FA disabled successfully"}
    
    with patch.object(AuthService, 'disable_2fa', return_value=expected_response) as mock_disable:
        response = client.post("/auth/disable-2fa", params={"user_id": 1})
        
        assert response.status_code == 200
        assert response.json() == expected_response

def test_refresh_token_success():
    expected_response = {"access_token": "new_token", "token_type": "bearer"}
    
    with patch.object(AuthService, 'verify_refresh_token', return_value=expected_response) as mock_refresh:
        response = client.get(
            "/auth/refresh",
            cookies={"auth_cookie": "test_refresh_token"}
        )
        
        assert response.status_code == 200
        assert response.json() == expected_response
        mock_refresh.assert_called_once()

def test_refresh_token_missing_cookie():
    response = client.get("/auth/refresh")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid token"}

def test_logout_success():
    response = client.post("/auth/logout")
    assert response.status_code == 204

def test_get_current_user_success(mock_db):
    expected_user = {
        'id': 1,
        'email': 'test@example.com',
        'first_name': 'test',
        'last_name': 'test',
        'is_2fa_enabled': False,
        'role_id': 1,
        'creation_date': '2022-01-01T00:00:00',
        'deletion_date': None
    }
    
    with patch.object(AuthService, 'get_current_user', return_value=expected_user) as mock_get_user:
        response = client.get(
            "/auth/current-user",
            cookies={"auth_cookie": "test_token"}
        )
        
        assert response.status_code == 200
        assert response.json() == expected_user
        # mock_get_user.assert_called_once_with(mock_db, "test_token")

def test_get_current_user_no_cookie(mock_db):
    response = client.get("/auth/current-user")
    assert response.status_code == 401
