from typing import List

from fastapi import HTTPException

from dtos.user_dtos import UserDTO, UserCreateDTO
from repositories.user_repository import UserRepository


class UserService:
    '''
    Service class for user
    '''

    @staticmethod
    async def create(user_create_dto: UserCreateDTO) -> UserDTO:
        '''
        Create a user
        '''
        check_email = await UserRepository.get_by_email(user_create_dto.email)
        if check_email:
            raise HTTPException(status_code=400, detail="Email already taken")
        return await UserRepository.create(user_create_dto)
        

    @staticmethod
    async def get_all() -> List[UserDTO]:
        '''
        Get all users
        '''
        return await UserRepository.get_all()

    @staticmethod
    async def get_by_id(user_id: int) -> UserDTO:
        '''
        Get a usser by id
        '''
        user = await UserRepository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User with this id not found")
        return user

    @staticmethod
    async def update_user(user_id: int, user_create_dto: UserCreateDTO) -> UserDTO:
        '''
        Update a user
        '''
        user = await UserRepository.get_by_id(user_id)
        check_email = await UserRepository.get_by_email(user_create_dto.email)
        if check_email and check_email.id != user_id:
            raise HTTPException(status_code=400, detail="Email already taken")
        if not user:
            raise HTTPException(status_code=404, detail="User with this id not found")
        return await UserRepository.update(user_id, user_create_dto)

    @staticmethod
    async def delete_user(user_id: int) -> None:
        '''
        Delete a user
        '''
        user = await UserRepository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User with this id not found")
        await UserRepository.delete_by_id(user_id)
