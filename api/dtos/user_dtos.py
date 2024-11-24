from pydantic import constr, conint
from datetime import datetime
from models.user import User

class UserCreateDTO(BaseModel):
    email: constr(regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    first_name: constr(min_length=2, max_length=50)
    last_name: constr(min_length=2, max_length=50)
    password: constr(min_length=8)
    role_id: conint(ge=1)

    def to_user(self):
        return User(
            last_name=self.last_name,
            first_name=self.first_name,
            email=self.email,
            password=self.password,
            role_id=self.role_id
        )


class UserDTO(BaseModel):
    id: conint(ge=1)
    email: constr(regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    first_name: constr(min_length=2, max_length=50)
    last_name: constr(min_length=2, max_length=50)
    role_id: conint(ge=1)
    creation_date: datetime
    deletion_date: Optional[datetime]

    class Config:
        orm_mode = True

    @staticmethod
    def from_user(user: User):
        if user is None:
            return None
        return UserDTO(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role_id=user.role_id,
            creation_date=user.creation_date,
            deletion_date=user.deletion_date
        )
