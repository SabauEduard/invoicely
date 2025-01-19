from pydantic import BaseModel, Field
from typing import List
from models.tag import Tag


class TagDTO(BaseModel):
    id: int
    name: str
    user_id: int

    @staticmethod
    def from_tag(tag: Tag):
        return TagDTO(id=tag.id, name=tag.name, user_id=tag.user_id)


class TagsCreateDTO(BaseModel):
    tags: List[str] = Field(None, alias="tags")
    
    @staticmethod
    def to_tags(self):
        return [Tag(name=tag) for tag in self.tags]
    
class TagCreateDTO(BaseModel):
    name: str
    user_id: int

    def to_tag(self) -> Tag:
        return Tag(name=self.name, user_id=self.user_id)
    