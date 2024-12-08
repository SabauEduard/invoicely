from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dtos.role_dtos import RoleDTO, RoleCreateDTO
from models.role import Role
from typing import Optional, List


class RoleRepository:
    '''
    Repository for Roles.
    '''

    @staticmethod
    async def create(role_create_dto: RoleCreateDTO, db: AsyncSession) -> RoleDTO:
        '''
        Create a role.
        '''
        new_role = role_create_dto.to_role()
        db.add(new_role)
        await db.commit()
        await db.refresh(new_role)

        return RoleDTO.from_role(new_role)

    @staticmethod
    async def get_all(db: AsyncSession) -> List[RoleDTO]:
        '''
        Get all roles.
        '''
        result = await db.execute(select(Role))
        roles = result.scalars().all()
        return [RoleDTO.from_role(role) for role in roles]

    @staticmethod
    async def get_by_id(role_id: int, db: AsyncSession) -> Optional[RoleDTO]:
        '''
        Get a role by id.
        '''
        result = await db.execute(select(Role).filter(Role.id == role_id))
        role = result.scalars().first()
        return RoleDTO.from_role(role)

    @staticmethod
    async def delete_by_id(role_id: int, db: AsyncSession) -> None:
        '''
        Delete a role by id.
        '''
        result = await db.execute(select(Role).filter(Role.id == role_id))
        role = result.scalars().first()
        await db.delete(role)
        await db.commit()
