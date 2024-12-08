from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user_repository import UserRepository
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from config import settings
import jwt
import json
from starlette import status
from dtos.token_dtos import TokenDTO


class AuthService:
    secret_key = settings().secret_key
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    async def verify_password(plain_password, hashed_password):
        return AuthService.bcrypt_context.verify(plain_password, hashed_password)

    @staticmethod
    async def get_current_user(db: AsyncSession, auth_cookie: str):
        if auth_cookie is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )

        try:
            auth_cookie_dict = json.loads(auth_cookie)
            payload = jwt.decode(
                auth_cookie_dict["access_token"],
                AuthService.secret_key,
                algorithms=["HS256"],
            )

            email = payload.get("sub")

            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
                )

            return UserRepository.get_by_email(email, db)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

    @staticmethod
    async def create_access_token(email, expires_delta=timedelta(minutes=15)):
        encode = {
            "sub": email,
            "exp": datetime.now(timezone.utc) + expires_delta,
        }
        return jwt.encode(encode, AuthService.secret_key, algorithm="HS256")

    @staticmethod
    async def login(
        db: AsyncSession,
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
        password = await UserRepository.get_password_by_email(form_data.username, db)

        if not password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not AuthService.verify_password(form_data.password, password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = await AuthService.create_access_token(form_data.username)
        refresh_token = await AuthService.create_access_token(
            form_data.username, timedelta(hours=1)
        )

        secret_data = {"access_token": token, "refresh_token": refresh_token}

        response.set_cookie(
            "auth_cookie",
            json.dumps(secret_data),
            httponly=True,
            expires=timedelta(minutes=15),
            secure=True
        )

        return TokenDTO(access_token=token, token_type="bearer")

    @staticmethod
    async def verify_refresh_token(db: AsyncSession, response, refresh_token: str = Cookie(None)):
        try:
            auth_cookie_dict = json.loads(refresh_token)
            payload = jwt.decode(
                auth_cookie_dict["refresh_token"],
                AuthService.secret_key,
                algorithms=["HS256"],
            )

            email = payload.get("sub")

            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
                )

            email = payload.get("sub")
            token = await AuthService.create_access_token(email)

            secret_data = {
                "access_token": token,
                "refresh_token": auth_cookie_dict["refresh_token"],
            }

            response.set_cookie(
                "auth_cookie",
                json.dumps(secret_data),
                httponly=True,
                expires=timedelta(minutes=15),
            )

            return TokenDTO(access_token=token, token_type="bearer")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
