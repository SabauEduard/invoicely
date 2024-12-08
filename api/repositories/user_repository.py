from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from dtos.user_dtos import UserDTO, UserCreateDTO
from typing import Optional, List


class UserRepository:
    '''
    Repository for Users.
    '''

    @staticmethod
    async def create(user_create_dto: UserCreateDTO, db: AsyncSession) -> UserDTO:
        '''
        Create a user.
        '''
        new_user = user_create_dto.to_user()
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return UserDTO.from_user(new_user)

    @staticmethod
    async def get_all(db: AsyncSession) -> List[UserDTO]:
        '''
        Get all users.
        '''
        result = await db.execute(select(User))
        users = result.scalars().all()
        return [UserDTO.from_user(user) for user in users]

    @staticmethod
    async def get_by_email(email: str, db: AsyncSession) -> Optional[UserDTO]:
        '''
        Get a user by email.
        '''
        result = await db.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        return UserDTO.from_user(user)

    @staticmethod
    async def get_by_id(user_id: int, db: AsyncSession) -> Optional[UserDTO]:
        '''
        Get a user by id.
        '''
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        return UserDTO.from_user(user)

    @staticmethod
    async def delete_by_id(user_id: int, db: AsyncSession) -> None:
        '''
        Delete a user by id.
        '''
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        await db.delete(user)
        await db.commit()

    @staticmethod
    async def update(user_id: int, user_create_dto: UserCreateDTO, db: AsyncSession) -> UserDTO:
        '''
        Update a user.
        '''
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        user.email = user_create_dto.email
        user.password = user_create_dto.password
        user.first_name = user_create_dto.first_name
        user.last_name = user_create_dto.last_name
        user.role_id = user_create_dto.role_id
        await db.commit()
        await db.refresh(user)
        return UserDTO.from_user(user)
