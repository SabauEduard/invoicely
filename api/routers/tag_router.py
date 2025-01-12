from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db
from dtos.tag_dtos import TagDTO, TagCreateDTO
from services.tag_service import TagService

tag_router = APIRouter(tags=["Tags"])

@tag_router.get(
    "/",
    response_model=List[TagDTO],
    response_model_by_alias=False,
    responses={
        200: {"description": "Tags retrieved successfully"},
    }
)
async def get_tags(db: AsyncSession = Depends(get_db)):
    return await TagService.get_all(db)


@tag_router.get(
    "/{tag_id}",
    response_model_by_alias=False,
    response_model=TagDTO,
    responses={
        404: {"description": "Tag not found"},
        200: {"description": "Tag retrieved successfully"},
    }
)
async def get_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    return await TagService.get_by_id(tag_id, db)


@tag_router.post(
    "/",
    response_model=TagDTO,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    responses={
        400: {"description": "Tag already exists"},
        201: {"description": "Tag created successfully"},
    }
)
async def create_tag(tag_create_dto: TagCreateDTO, db: AsyncSession = Depends(get_db)):
    return await TagService.create(tag_create_dto, db)


@tag_router.delete(
    "/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Tag not found"},
        204: {"description": "Tag deleted successfully"},
    },
)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    await TagService.delete(tag_id, db)