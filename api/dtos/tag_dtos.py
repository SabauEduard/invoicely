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
    names: List[str] = Field(default_factory=list, alias="names")

    def to_tags(self):
        return [Tag(name=name) for name in self.names]
