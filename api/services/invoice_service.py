from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.invoice import Invoice
from dtos.invoice_dtos import InvoiceDTO, InvoiceCreateDTO
from repositories.invoice_repository import InvoiceRepository
from routers.auth_router import get_current_user

class InvoiceService:

    @staticmethod
    async def create(invoice_create_dto: InvoiceCreateDTO, db: AsyncSession) -> InvoiceDTO:
        '''
        Create an invoice
        '''
        current_user = await get_current_user(db)
        invoice_create_dto.user_id = current_user.id
        return await InvoiceRepository.create(invoice_create_dto, db)
    
    @staticmethod
    async def get_all(db: AsyncSession) -> List[InvoiceDTO]:
        '''
        Get all invoices
        '''
        current_user = await get_current_user(db)
        invoices = await InvoiceRepository.get_all(db)
        filtered_invoices = [invoice for invoice in invoices if invoice.user_id == current_user.id]
        return filtered_invoices
    
    @staticmethod
    async def get_by_id(invoice_id: int, db: AsyncSession) -> InvoiceDTO:
        '''
        Get an invoice by id
        '''
        current_user = await get_current_user(db)
        invoice = await InvoiceRepository.get_by_id(invoice_id, db)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice with this id not found")
        if invoice.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to access this invoice")
        return invoice
    
    @staticmethod
    async def update_invoice(invoice_id: int, invoice_create_dto: InvoiceCreateDTO, db: AsyncSession) -> InvoiceDTO:
        '''
        Update an invoice
        '''
        current_user = await get_current_user(db)
        invoice = await InvoiceRepository.get_by_id(invoice_id, db)
        
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice with this id not found")
        
        if invoice.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to update this invoice")
        
        return await InvoiceRepository.update(invoice_id, invoice_create_dto, db)
    
    @staticmethod
    async def delete_invoice(invoice_id: int, db: AsyncSession) -> None:
        '''
        Delete an invoice
        '''
        current_user = await get_current_user(db)
        invoice = await InvoiceRepository.get_by_id(invoice_id, db)
        
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice with this id not found")
        
        if invoice.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to delete this invoice")
        
        return await InvoiceRepository.delete_by_id(invoice_id, db)