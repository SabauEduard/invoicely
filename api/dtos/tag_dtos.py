from pydantic import BaseModel, Field
from typing import List
from models.tag import Tag


class TagDTO(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_tag(tag: Tag):
        return TagDTO(id=tag.id, name=tag.name)


class TagsCreateDTO(BaseModel):
    tags: List[str] = Field(None, alias="tags")
    
    @staticmethod
    def to_tags(self):
        return [Tag(name=tag) for tag in self.tags]
    
class TagCreateDTO(BaseModel):
    tag: str = Field(None, alias="tag")
    
    @staticmethod
    def to_tag(self):
        return Tag(name=self.tag)
    