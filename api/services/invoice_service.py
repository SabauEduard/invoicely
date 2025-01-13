import os
from typing import List, Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from dtos.user_dtos import UserDTO
from models.invoice import Invoice
from dtos.invoice_dtos import InvoiceDTO, InvoiceCreateDTO
from repositories.invoice_repository import InvoiceRepository
from routers.auth_router import get_current_user
from ml_utils.category_detection import detect_category
from pathlib import Path
import time 
from PIL import Image

class InvoiceService:

    @staticmethod
    async def create(invoice_create_dto: InvoiceCreateDTO, db: AsyncSession, user: UserDTO) -> InvoiceDTO:
        '''
        Create an invoice
        '''
        invoice_create_dto.user_id = user.id

        original_file_path = Path() / (f"uploads/{user.id}/categorie/{invoice_create_dto.vendor}/{invoice_create_dto.file.filename}")
        # File used for processing and it will be altered during the process and deleted after
        copy_file_path = Path() / (f"uploads/{user.id}/categorie/{invoice_create_dto.vendor}/copy_{invoice_create_dto.file.filename}")
        
        file_type = invoice_create_dto.file.content_type
        content = await invoice_create_dto.file.read()
        
        # os.makedirs(os.path.dirname(original_file_path), exist_ok=True)
        # os.makedirs(os.path.dirname(copy_file_path), exist_ok=True)
        
        with open(original_file_path, "wb") as file_object:
            file_object.write(content)
        with open(copy_file_path, "wb") as file_object:
            file_object.write(content)
            
        time.sleep(5)
            
        # extract the content of the file and determine the category
        category_id, content = detect_category(str(original_file_path), str(copy_file_path), file_type)
        
        print(category_id, content)
            
        # delete the copy file
        # os.remove(copy_file_path)

        invoice_create_dto.category = category_id
        invoice_create_dto.path = original_file_path
        invoice_create_dto.duplicate = False
        invoice_create_dto.incomplete = False

        return await InvoiceRepository.create(invoice_create_dto, db)

    @staticmethod
    async def get_all(db: AsyncSession, user: UserDTO) -> List[InvoiceDTO]:
        '''
        Get all invoices
        '''
        invoices = await InvoiceRepository.get_all(db)
        filtered_invoices = [invoice for invoice in invoices if invoice.user_id == user.id]
        return filtered_invoices
    
    @staticmethod
    async def get_by_id(invoice_id: int, db: AsyncSession, user: UserDTO) -> InvoiceDTO:
        '''
        Get an invoice by id
        '''
        invoice = await InvoiceRepository.get_by_id(invoice_id, db)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice with this id not found")
        if invoice.user_id != user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to access this invoice")
        return invoice
    
    @staticmethod
    async def update_invoice(invoice_id: int, invoice_create_dto: InvoiceCreateDTO, db: AsyncSession, user: UserDTO) -> InvoiceDTO:
        '''
        Update an invoice
        '''
        invoice = await InvoiceRepository.get_by_id(invoice_id, db)
        
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice with this id not found")
        
        if invoice.user_id != user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to update this invoice")
        
        return await InvoiceRepository.update(invoice_id, invoice_create_dto, db)
    
    @staticmethod
    async def delete_invoice(invoice_id: int, db: AsyncSession, user: UserDTO) -> None:
        '''
        Delete an invoice
        '''
        invoice = await InvoiceRepository.get_by_id(invoice_id, db)
        
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice with this id not found")
        
        if invoice.user_id != user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to delete this invoice")
        
        return await InvoiceRepository.delete_by_id(invoice_id, db)
