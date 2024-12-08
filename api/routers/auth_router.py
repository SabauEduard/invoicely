from fastapi import APIRouter, Body, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from dtos.token_dtos import TokenDTO
from services.auth_service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


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
):
    return await AuthService.login(response, form_data)


@auth_router.post(
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
    response: Response,
    refresh_token: str = Body(..., embed=True),
):
    return await AuthService.verify_refresh_token(response, refresh_token)


@auth_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={204: {"description": "User logged out successfully"}},
)
async def logout(response: Response):
    response.delete_cookie("auth_cookie", httponly=True, secure=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
