import pytest
import bcrypt
import json
import jwt
from fastapi import HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service import AuthService
from repositories.user_repository import UserRepository
from dtos.token_dtos import TokenDTO
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_verify_password():
    plain_password = "password123"
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    result = await AuthService.verify_password(plain_password, hashed_password)
    assert result is True

@pytest.mark.asyncio
async def test_get_current_user():
    db = AsyncMock(AsyncSession)
    auth_cookie = json.dumps({"access_token": "valid_token"})
    user = {"email": "test@example.com"}
    
    with patch("jwt.decode", return_value={"sub": "test@example.com"}):
        with patch.object(UserRepository, "get_by_email", return_value=user):
            result = await AuthService.get_current_user(db, auth_cookie)
            assert result == user

@pytest.mark.asyncio
async def test_create_access_token():
    email = "test@example.com"
    token = await AuthService.create_access_token(email)
    payload = jwt.decode(token, AuthService.secret_key, algorithms=["HS256"])
    assert payload["sub"] == email

@pytest.mark.asyncio
async def test_login():
    db = AsyncMock(AsyncSession)
    response = Response()
    form_data = OAuth2PasswordRequestForm(username="test@example.com", password="password123")
    user = {"email": "test@example.com", "is_2fa_enabled": False}
    
    with patch.object(UserRepository, "get_password_by_email", return_value=bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')):
        with patch.object(UserRepository, "get_by_email", return_value=user):
            result = await AuthService.login(db, response, form_data)
            assert isinstance(result, TokenDTO)

@pytest.mark.asyncio
async def test_verify_refresh_token():
    response = Response()
    refresh_token = json.dumps({"refresh_token": "valid_refresh_token"})
    
    with patch("jwt.decode", return_value={"sub": "test@example.com"}):
        token_dto = await AuthService.verify_refresh_token(response, refresh_token)
        assert isinstance(token_dto, TokenDTO)

@pytest.mark.asyncio
async def test_enable_2fa():
    db = AsyncMock(AsyncSession)
    user_id = 1
    user = {"email": "test@example.com", "is_2fa_enabled": False}
    
    with patch.object(UserRepository, "get_by_id", return_value=user):
        with patch.object(UserRepository, "enable_2fa", return_value=None):
            result = await AuthService.enable_2fa(db, user_id)
            assert "otp_secret" in result
            assert "qr_code" in result

@pytest.mark.asyncio
async def test_disable_2fa():
    db = AsyncMock(AsyncSession)
    user_id = 1
    user = {"email": "test@example.com", "is_2fa_enabled": True}
    
    with patch.object(UserRepository, "get_by_id", return_value=user):
        with patch.object(UserRepository, "disable_2fa", return_value=None):
            result = await AuthService.disable_2fa(db, user_id)
            assert result == {"message": "2FA disabled successfully"}

@pytest.mark.asyncio
async def test_verify_2fa():
    db = AsyncMock(AsyncSession)
    user_id = 1
    otp = "123456"
    
    with patch.object(UserRepository, "get_otp_code_by_id", return_value="secret_otp"):
        with patch("services.otp_service.verify_otp", return_value=True):
            result = await AuthService.verify_2fa(db, user_id, otp)
            assert result == {"message": "2FA verified"}