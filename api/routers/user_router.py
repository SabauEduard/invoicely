from typing import List

from fastapi import APIRouter, Body
from starlette import status

from models.user import User, UserCreate
from services.user_service import UserService

asset_router = APIRouter()


@asset_router.get(
    "/",
    response_model=List[User],
    response_model_by_alias=False,
    responses={
        200: {"description": "Users retrieved successfully"},
    }
)
async def get_assets():
    return await UserService.get_all()


@asset_router.get(
    "/{asset_id}",
    response_model_by_alias=False,
    response_model=User,
    responses={
        404: {"description": "User not found"},
        200: {"description": "User retrieved successfully"},
    }
)
async def get_asset(user_id: str):
    return await UserService.get_by_id(user_id)


@asset_router.get(
    "/pre-signed-url/{asset_id}",
    response_model_by_alias=False,
    response_model=str,
    responses={
        404: {"description": "Asset not found"},
        200: {"description": "Pre-signed URL retrieved successfully"},
    }
)
async def get_pre_signed_url(asset_id: str):
    return await AssetService.get_pre_signed_url(asset_id)


@asset_router.get(
    "/by-owner/{owner_id}",
    response_model_by_alias=False,
    response_model=List[Asset],
    responses={
        200: {"description": "Assets retrieved successfully"},
    }
)
async def get_assets_of_owner(owner_id: str):
    return await AssetService.get_by_owner_id(owner_id)
