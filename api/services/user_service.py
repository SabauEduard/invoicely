from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dtos.user_dtos import UserDTO, UserCreateDTO
from repositories.user_repository import UserRepository


class UserService:
    '''
    Service class for user
    '''

    @staticmethod
    async def create(user_create_dto: UserCreateDTO, db: AsyncSession) -> UserDTO:
        '''
        Create a user
        '''
        check_email = await UserRepository.get_by_email(user_create_dto.email, db)
        if check_email:
            raise HTTPException(status_code=400, detail="Email already taken")
        return await UserRepository.create(user_create_dto, db)
        

    @staticmethod
    async def get_all(db: AsyncSession) -> List[UserDTO]:
        '''
        Get all users
        '''
        return await UserRepository.get_all(db)

    @staticmethod
    async def get_by_id(user_id: int, db: AsyncSession) -> UserDTO:
        '''
        Get a usser by id
        '''
        user = await UserRepository.get_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User with this id not found")
        return user

    @staticmethod
    async def update_user(user_id: int, user_create_dto: UserCreateDTO, db: AsyncSession) -> UserDTO:
        '''
        Update a user
        '''
        user = await UserRepository.get_by_id(user_id, db)
        check_email = await UserRepository.get_by_email(user_create_dto.email, db)
        if check_email and check_email.id != user_id:
            raise HTTPException(status_code=400, detail="Email already taken")
        if not user:
            raise HTTPException(status_code=404, detail="User with this id not found")
        return await UserRepository.update(user_id, user_create_dto, db)

    @staticmethod
    async def delete_user(user_id: int, db: AsyncSession) -> None:
        '''
        Delete a user
        '''
        user = await UserRepository.get_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User with this id not found")
        await UserRepository.delete_by_id(user_id, db)
