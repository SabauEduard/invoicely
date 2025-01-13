from pydantic import BaseModel, Field
from typing import List
from models.tag import Tag


class TagDTO(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_tag(tag: Tag):
        return TagDTO(id=tag.id, name=tag.name)


class TagCreateDTO(BaseModel):
    tags: List[str] = Field(None, alias="tags")
