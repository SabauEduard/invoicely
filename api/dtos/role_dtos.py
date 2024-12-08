from pydantic import Field, BaseModel

from models.role import Role


class RoleDTO(BaseModel):
    id: int = Field(..., alias="id")
    name: str = Field(..., alias="name")

    @staticmethod
    def from_role(role: Role):
        return RoleDTO(
            id=role.id,
            name=role.name
        )


class RoleCreateDTO(BaseModel):
    name: str = Field(..., alias="name")

    def to_role(self):
        return Role(
            name=self.name
        )
