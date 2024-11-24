from database import db_dependency
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, Response
from repositories.user_repository import UserRepository
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from config import settings
import jwt
import json


class AuthService:
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return AuthService.bcrypt_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user, expires_delta=timedelta(minutes=15)):
        encode = {
            "sub": user.email,
            "id": user.id,
            "exp": datetime.now(timezone.utc) + expires_delta,
        }
        return jwt.encode(encode, settings().secret_key, algorithm="HS256")

    @staticmethod
    async def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        """
        Generate access token for user
        """
        user = await UserRepository.get_user_by_email(form_data.email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not AuthService.verify_password(form_data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = await AuthService.create_access_token(user)
        refresh_token = await AuthService.create_access_token(user, timedelta(hours=1))

        secret_data = {"access_token": token, "refresh_token": refresh_token}

        response.set_cookie(
            "auth_cookie",
            json.dumps(secret_data),
            httponly=True,
            expires=timedelta(minutes=15)
        )
        return user
