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
import bcrypt
from starlette import status
from dtos.token_dtos import TokenDTO
from services.otp_service import generate_otp_secret, get_totp_uri, generate_qr_code, verify_otp


class AuthService:
    secret_key = settings().secret_key

    @staticmethod
    async def verify_password(plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

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
            print("Email: " + email)
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
                )
            user = await UserRepository.get_by_email(email, db)
            print(user)
            return user

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
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        otp: str = None,
    ):
        password = await UserRepository.get_password_by_email(form_data.username, db)
        user = await UserRepository.get_by_email(form_data.username, db)

        if not password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not await AuthService.verify_password(form_data.password, password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if user.is_2fa_enabled:
            await AuthService.verify_2fa(db, user.id, otp)

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
    async def verify_refresh_token(response, refresh_token: str = Cookie(None)):
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

    @staticmethod
    async def enable_2fa(db: AsyncSession, user_id: int):
        user = await UserRepository.get_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        if user.is_2fa_enabled:
            return {"message": "2FA already enabled"}
        otp_secret=generate_otp_secret()
        await UserRepository.enable_2fa(user_id, otp_secret, db)
        uri = get_totp_uri(user.email, otp_secret)
        qr_code = generate_qr_code(uri)
        qr_code_url = f"data:image/png;base64,{qr_code}"
        return {"otp_secret": otp_secret, "qr_code_url": qr_code_url}

    @staticmethod
    async def disable_2fa(db: AsyncSession, user_id: int):
        user = await UserRepository.get_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        if not user.is_2fa_enabled:
            return {"message": "2FA already disabled"}
        await UserRepository.disable_2fa(user_id, db)
        return {"message": "2FA disabled successfully"}

    @staticmethod
    async def verify_2fa(db: AsyncSession, user_id: int, otp: str):
        if not otp:
            raise HTTPException(status_code=400, detail="OTP is required")
        secret_otp = await UserRepository.get_otp_code_by_id(user_id, db)
        if verify_otp(secret_otp, otp):
            return {"message": "2FA verified"}
        else:
            raise HTTPException(status_code=400, detail="Invalid OTP")
