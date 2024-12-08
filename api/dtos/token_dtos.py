from pydantic import Field, BaseModel


class TokenDTO(BaseModel):
    access_token: str = Field(..., alias="access_token")
    token_type: str = Field(..., alias="token_type")
