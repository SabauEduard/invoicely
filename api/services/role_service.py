from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dtos.role_dtos import RoleDTO, RoleCreateDTO
from repositories.role_repository import RoleRepository


class RoleService:
    '''
    Service class for role
    '''

    @staticmethod
    async def create(role_create_dto: RoleCreateDTO, db: AsyncSession) -> RoleDTO:
        '''
        Create a role
        '''
        return await RoleRepository.create(role_create_dto, db)

    @staticmethod
    async def get_all(db: AsyncSession) -> List[RoleDTO]:
        '''
        Get all roles
        '''
        return await RoleRepository.get_all(db)

    @staticmethod
    async def get_by_id(role_id: int, db: AsyncSession) -> RoleDTO:
        '''
        Get a role by id
        '''
        role = await RoleRepository.get_by_id(role_id, db)
        if not role:
            raise HTTPException(status_code=404, detail="Role with this id not found")
        return role

    @staticmethod
    async def delete(role_id: int, db: AsyncSession) -> None:
        '''
        Delete a role
        '''
        role = await RoleRepository.get_by_id(role_id, db)
        if not role:
            raise HTTPException(status_code=404, detail="Role with this id not found")
        await RoleRepository.delete_by_id(role_id, db)
