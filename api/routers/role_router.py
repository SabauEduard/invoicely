from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db
from dtos.role_dtos import RoleDTO, RoleCreateDTO
from services.role_service import RoleService

role_router = APIRouter()


@role_router.get(
    "/",
    response_model=List[RoleDTO],
    response_model_by_alias=False,
    responses={
        200: {"description": "Roles retrieved successfully"},
    }
)
async def get_roles(db: AsyncSession = Depends(get_db)):
    return await RoleService.get_all(db)


@role_router.get(
    "/{role_id}",
    response_model_by_alias=False,
    response_model=RoleDTO,
    responses={
        404: {"description": "Role not found"},
        200: {"description": "Role retrieved successfully"},
    }
)
async def get_role(role_id: int, db: AsyncSession = Depends(get_db)):
    return await RoleService.get_by_id(role_id, db)


@role_router.post(
    "/",
    response_model=RoleDTO,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    responses={
        400: {"description": "Role already exists"},
        201: {"description": "Role created successfully"},
    }
)
async def create_role(role_create_dto: RoleCreateDTO, db: AsyncSession = Depends(get_db)):
    return await RoleService.create(role_create_dto, db)


@role_router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Role not found"},
        204: {"description": "Role deleted successfully"},
    },
)
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db)):
    await RoleService.delete(role_id, db)
