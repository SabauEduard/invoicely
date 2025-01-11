from pydantic import BaseModel, Field

from models.tag import Tag

class TagDTO(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_tag(tag: Tag):
        return TagDTO(
            id=tag.id,
            name=tag.name
        )


class TagCreateDTO(BaseModel):
    name: str = Field(..., alias="name")

    def to_tag(self):
        return Tag(
            name=self.name
        )