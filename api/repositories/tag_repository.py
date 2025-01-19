from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.tag import Tag
from dtos.tag_dtos import TagCreateDTO, TagDTO
from models.invoice import invoice_tags
from sqlalchemy import insert

class TagRepository:
    '''
    Repository for tags.
    '''

    @staticmethod
    async def create(tag_create_dto: TagCreateDTO, db: AsyncSession) -> TagDTO:
        '''
        Create a tag.
        '''
        new_tag = tag_create_dto.to_tag()
        db.add(new_tag)
        await db.commit()
        await db.refresh(new_tag)

        return TagDTO.from_tag(new_tag)
    
    @staticmethod
    async def add_invoice_tag(tag_id: int, invoice_id: int, db: AsyncSession) -> None:
        '''
        Add a tag to an invoice.
        '''
        stmt = insert(invoice_tags).values(invoice_id=invoice_id, tag_id=tag_id)
        await db.execute(stmt)
        await db.commit()


    @staticmethod
    async def get_all(db: AsyncSession) -> List[TagDTO]:
        '''
        Get all tags.
        '''
        result = await db.execute(select(Tag))
        tags = result.scalars().all()
        return [TagDTO.from_tag(tag) for tag in tags]
    

    @staticmethod
    async def get_by_id(tag_id: int, db: AsyncSession) -> Optional[TagDTO]:
        '''
        Get a tag by id.
        '''
        result = await db.execute(select(Tag).filter(Tag.id == tag_id))
        tag = result.scalars().first()
        return TagDTO.from_tag(tag)
    

    @staticmethod
    async def delete_by_id(tag_id: int, db: AsyncSession) -> None:
        '''
        Delete a tag by id.
        '''
        result = await db.execute(select(Tag).filter(Tag.id == tag_id))
        tag = result.scalars().first()
        await db.delete(tag)
        await db.commit()