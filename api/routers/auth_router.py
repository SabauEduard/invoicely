from typing import List

from fastapi import APIRouter, Body
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from dtos.token_dtos import TokenDTO
from services.auth_service import AuthService

auth_router = APIRouter()

@auth_router.post(
    "/login",
    response_model=TokenDTO,
    response_model_by_alias=False,
    responses={
        401: {"description": "Invalid credentials"},
        200: {"description": "User logged in successfully"},
    }
)
async def login(form_data: OAuth2PasswordRequestForm = Body(...)):
    response = Response()
    return await AuthService.login(response, form_data)

@auth_router.post(
    "/refresh",
    response_model=TokenDTO,
    response_model_by_alias=False,
    responses={
        401: {"description": "Invalid token"},
        200: {"description": "Token refreshed successfully"},
    }
)
async def refresh_token(response: Response, refresh_token: str = Body(...)):
    return await AuthService.verify_refresh_token(response, refresh_token)

@auth_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "User logged out successfully"},
    }
)
async def logout(response: Response):
    response.delete_cookie("auth_cookie")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
