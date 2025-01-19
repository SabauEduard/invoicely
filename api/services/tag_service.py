from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dtos.tag_dtos import TagCreateDTO, TagDTO, TagsCreateDTO
from repositories.tag_repository import TagRepository

class TagService:

    @staticmethod
    async def create(tags_create_dto: TagsCreateDTO, db: AsyncSession) -> TagDTO:
        '''
        Create a tag
        '''
        
        user_tags = await TagRepository.get_all(db)
        
        for tag in tags_create_dto.tags:
            if tag not in [user_tag.name for user_tag in user_tags]:
                await TagRepository.create(TagCreateDTO(tag=tag), db)
    
    @staticmethod
    async def get_all(db: AsyncSession) -> List[TagDTO]:
        '''
        Get all tags
        '''
        return await TagRepository.get_all(db)
    
    @staticmethod
    async def get_by_id(tag_id: int, db: AsyncSession) -> TagDTO:
        '''
        Get a tag by id
        '''
        tag = await TagRepository.get_by_id(tag_id, db)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag with this id not found")
        return tag
    
    @staticmethod
    async def delete(tag_id: int, db: AsyncSession) -> None:
        '''
        Delete a tag
        '''
        tag = await TagRepository.get_by_id(tag_id, db)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag with this id not found")
        await TagRepository.delete_by_id(tag_id, db)