import io
from typing import List

from fastapi import HTTPException, UploadFile, BackgroundTasks

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
        # TODO: Implement logic to verify if email is already taken and password respects constraints
        return await UserRepository.create(user_create_dto)
        

    @staticmethod
    async def get_all() -> List[UserDTO]:
        '''
        Get all assets
        '''
        return await UserRepository.get_all()

    @staticmethod
    async def get_by_id(user_id: str) -> UserDTO:
        '''
        Get an asset by id
        '''
        user = await UserRepository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User with this id not found")
        return user