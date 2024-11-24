from typing import List

from fastapi import APIRouter, Body
from starlette import status

from dtos.user_dtos import UserDTO, UserCreateDTO
from services.user_service import UserService

user_router = APIRouter()


@user_router.get(
    "/",
    response_model=List[UserDTO],
    response_model_by_alias=False,
    responses={
        200: {"description": "Users retrieved successfully"},
    }
)
async def get_users():
    return await UserService.get_all()


@user_router.get(
    "/{user_id}",
    response_model_by_alias=False,
    response_model=UserDTO,
    responses={
        404: {"description": "User not found"},
        200: {"description": "User retrieved successfully"},
    }
)
async def get_user(user_id: str):
    return await UserService.get_by_id(user_id)


@user_router.post(
    "/",
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    responses={
        400: {"description": "User already exists"},
        201: {"description": "User created successfully"},
    }
)
async def create_user(user_create_dto: UserCreateDTO):
    return await UserService.create_user(user_create_dto)


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "User not found"},
        204: {"description": "User deleted successfully"},
    },
)
async def delete_user(user_id: str):
    await UserService.delete_by_id(user_id)
    return


@user_router.put(
    "/{user_id}",
    response_model=UserDTO,
    response_model_by_alias=False,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "User not found"},
        201: {"description": "User updated successfully"},
    },
)
async def update_user(user_id: str, user_update_dto: UserCreateDTO):
    await UserService.update_user(user_id, user_update_dto)
    