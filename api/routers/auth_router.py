from fastapi import APIRouter, Body, Depends, Response, Cookie, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db
from dtos.token_dtos import TokenDTO
from dtos.user_dtos import UserDTO
from services.auth_service import AuthService

auth_router = APIRouter(tags=["Authentication"])


@auth_router.post(
    "/login",
    response_model=TokenDTO,
    response_model_by_alias=False,
    responses={
        401: {
            "description": "Invalid credentials",
            "content": {"application/json": {"example": {"detail": "Invalid credentials"}}},
        },
        200: {
            "description": "User logged in successfully",
            "content": {"application/json": {"example": {"access_token": "token", "token_type": "bearer"}}},
        },
    },
)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    otp: str = Body(None),
    db: AsyncSession = Depends(get_db)
):
    return await AuthService.login(db, response, form_data, otp)


@auth_router.post(
    "/enable-2fa",
    response_model=dict,
    responses={
        200: {"description": "2FA enabled successfully"},
        400: {"description": "User not found"},
    },
)
async def enable_2fa(user_id: int, db: AsyncSession = Depends(get_db)):
    return await AuthService.enable_2fa(db, user_id)

@auth_router.post(
    "/disable-2fa",
    response_model=dict,
    responses={
        200: {"description": "2FA disabled successfully"},
        400: {"description": "User not found"},
    },
)
async def disable_2fa(user_id: int, db: AsyncSession = Depends(get_db)):
    return await AuthService.disable_2fa(db, user_id)


@auth_router.get(
    "/refresh",
    response_model=TokenDTO,
    response_model_by_alias=False,
    responses={
        401: {
            "description": "Invalid token",
            "content": {"application/json": {"example": {"detail": "Invalid token"}}},
        },
        200: {
            "description": "Token refreshed successfully",
            "content": {"application/json": {"example": {"access_token": "new_token", "token_type": "bearer"}}},
        },
    },
)
async def refresh_token(
    request: Request,
    response: Response
):
    auth_cookie = request.cookies.get("auth_cookie")
    
    if not auth_cookie:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    return await AuthService.verify_refresh_token(response, auth_cookie)


@auth_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={204: {"description": "User logged out successfully"}},
)
async def logout(response: Response):
    response.delete_cookie("auth_cookie", httponly=True, secure=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@auth_router.get(
    "/current-user",
    response_model=UserDTO,
    response_model_by_alias=False,
    responses={
        201: {"description": "User retrieved successfully"},
    }
)
async def get_current_user(db: AsyncSession = Depends(get_db), auth_cookie: str = Cookie(None)):
    return await AuthService.get_current_user(db, auth_cookie)
