from typing import List
from models.tag import Tag
from dtos.invoice_dtos import InvoiceCreateDTO
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dtos.tag_dtos import TagCreateDTO, TagDTO, TagsCreateDTO
from repositories.tag_repository import TagRepository

class TagService:

    @staticmethod
    async def create(tags_create_dto: List[TagCreateDTO], db: AsyncSession) -> List[Tag]:
        '''
        Create tags
        '''
        user_tags = await TagRepository.get_all(db)
        created_tags = []

        for tag_dto in tags_create_dto:
            if tag_dto.name not in [user_tag.name for user_tag in user_tags]:
                created_tag = await TagRepository.create(tag_dto, db)
                created_tags.append(created_tag)

        return created_tags
    
    @staticmethod
    async def create_invoice_tags(tags_create_dto: List[TagDTO], invoice_id: int, db: AsyncSession) -> List[TagDTO]:
        '''
        Create tags for an invoice
        '''
        for tag_dto in tags_create_dto:
            await TagRepository.add_invoice_tag(tag_dto.id, invoice_id, db)
    
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