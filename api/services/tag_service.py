from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dtos.tag_dtos import TagCreateDTO, TagDTO
from repositories.tag_repository import TagRepository

class TagService:

    @staticmethod
    async def create(tag_create_dto: TagCreateDTO, db: AsyncSession) -> TagDTO:
        '''
        Create a tag
        '''
        return await TagRepository.create(tag_create_dto, db)
    
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