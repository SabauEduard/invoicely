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
    async def enable_2fa(user_id: int, otp_secret: str, db: AsyncSession) -> bool:
        '''
        Enable 2FA for a user.
        '''
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        user.is_2fa_enabled = True
        user.otp_secret = otp_secret
        await db.commit()
        return UserDTO.from_user(user)

    @staticmethod
    async def disable_2fa(user_id: int, db: AsyncSession) -> bool:
        '''
        Disable 2FA for a user.
        '''
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        user.is_2fa_enabled = False
        user.otp_secret = None
        await db.commit()
        return UserDTO.from_user(user)

    @staticmethod
    async def get_otp_code_by_id(user_id: int, db: AsyncSession) -> Optional[str]:
        '''
        Get a user's OTP code by id.
        '''
        result = await db.execute(select(User.otp_secret).filter(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    async def get_password_by_email(email: str, db: AsyncSession) -> Optional[str]:
        '''
        Get a user's password by email.
        '''
        result = await db.execute(select(User.password).filter(User.email == email))
        return result.scalars().first()

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
        print("Test")
        print(email)
        result = await db.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        print(user.email)
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
