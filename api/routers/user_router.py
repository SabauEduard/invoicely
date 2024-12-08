from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db
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
async def get_users(db: AsyncSession = Depends(get_db)):
    return await UserService.get_all(db)


@user_router.get(
    "/{user_id}",
    response_model_by_alias=False,
    response_model=UserDTO,
    responses={
        404: {"description": "User not found"},
        200: {"description": "User retrieved successfully"},
    }
)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserService.get_by_id(user_id, db)


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
async def create_user(user_create_dto: UserCreateDTO, db: AsyncSession = Depends(get_db)):
    return await UserService.create(user_create_dto, db)


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "User not found"},
        204: {"description": "User deleted successfully"},
    },
)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    await UserService.delete_user(user_id, db)
    return


@user_router.put(
    "/{user_id}",
    response_model=UserDTO,
    response_model_by_alias=False,
    responses={
        404: {"description": "User not found"},
        201: {"description": "User updated successfully"},
    },
)
async def update_user(user_id: int, user_update_dto: UserCreateDTO, db: AsyncSession = Depends(get_db)):
    await UserService.update_user(user_id, user_update_dto, db)
