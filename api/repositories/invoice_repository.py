from typing import List, Optional

from enums.category import InvoiceCategory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.invoice import Invoice
from dtos.invoice_dtos import InvoiceCreateDTO, InvoiceDTO

class InvoiceRepository:

    @staticmethod
    async def create(invoice_create_dto: InvoiceCreateDTO, db: AsyncSession) -> InvoiceDTO:
        '''
        Create an invoice
        '''
        new_invoice = invoice_create_dto.to_invoice()

        db.add(new_invoice)
        await db.commit()
        await db.refresh(new_invoice)

        return InvoiceDTO.from_invoice(new_invoice)

    @staticmethod
    async def get_all(db: AsyncSession) -> List[InvoiceDTO]:
        '''
        Get all invoices
        '''
        result = await db.execute(select(Invoice))
        invoices = result.scalars().all()
        return [InvoiceDTO.from_invoice(invoice) for invoice in invoices]
    
    @staticmethod
    async def get_by_id(invoice_id: int, db: AsyncSession) -> Optional[InvoiceDTO]:
        '''
        Get an invoice by id
        '''
        result = await db.execute(select(Invoice).filter(Invoice.id == invoice_id))
        invoice = result.scalars().first()
        if not invoice:
            return None
        return InvoiceDTO.from_invoice(invoice)
    
    @staticmethod
    async def update(invoice_id: int, invoice_create_dto: InvoiceCreateDTO, db: AsyncSession) -> Optional[InvoiceDTO]:
        '''
        Update an invoice
        '''
        result = await db.execute(select(Invoice).filter(Invoice.id == invoice_id))
        invoice = result.scalars().first()

        invoice.category = InvoiceCategory(invoice_create_dto.category)
        invoice.path = invoice_create_dto.path
        invoice.vendor = invoice_create_dto.vendor
        invoice.amount = invoice_create_dto.amount
        invoice.status = invoice_create_dto.status
        invoice.importance = invoice_create_dto.importance
        invoice.notes = invoice_create_dto.notes
        invoice.duplicate = invoice_create_dto.duplicate
        invoice.incomplete = invoice_create_dto.incomplete
        invoice.emitted_date = invoice_create_dto.emitted_date
        invoice.expiry_date = invoice_create_dto.expiry_date

        await db.commit()
        await db.refresh(invoice)
        return InvoiceDTO.from_invoice(invoice)
    
    @staticmethod
    async def delete_by_id(invoice_id: int, db: AsyncSession) -> None:
        '''
        Delete an invoice by id
        '''
        result = await db.execute(select(Invoice).filter(Invoice.id == invoice_id))
        invoice = result.scalars().first()
        await db.delete(invoice)
        await db.commit()