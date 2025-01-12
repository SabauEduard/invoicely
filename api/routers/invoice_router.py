from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db
from dtos.invoice_dtos import InvoiceDTO, InvoiceCreateDTO
from services.invoice_service import InvoiceService

invoice_router = APIRouter(tags=["Invoices"])


@invoice_router.get(
    "/",
    response_model=List[InvoiceDTO],
    response_model_by_alias=False,
    responses={
        200: {"description": "Invoices retrieved successfully"},
    }
)
async def get_invoices(db: AsyncSession = Depends(get_db)):
    return await InvoiceService.get_all(db)


@invoice_router.get(
    "/{invoice_id}",
    response_model_by_alias=False,
    response_model=InvoiceDTO,
    responses={
        404: {"description": "Invoice not found"},
        200: {"description": "Invoice retrieved successfully"},
    }
)
async def get_invoice(invoice_id: int, db: AsyncSession = Depends(get_db)):
    return await InvoiceService.get_by_id(invoice_id, db)


@invoice_router.post(
    "/",
    response_model=InvoiceDTO,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    responses={
        400: {"description": "Invoice already exists"},
        201: {"description": "Invoice created successfully"},
    }
)
async def create_invoice(invoice_create_dto: InvoiceCreateDTO, db: AsyncSession = Depends(get_db)):
    return await InvoiceService.create(invoice_create_dto, db)

@invoice_router.put(
    "/{invoice_id}",
    response_model=InvoiceDTO,
    response_model_by_alias=False,
    responses={
        404: {"description": "Invoice not found"},
        200: {"description": "Invoice updated successfully"},
    }
)
async def update_invoice(invoice_id: int, invoice_create_dto: InvoiceCreateDTO, db: AsyncSession = Depends(get_db)):
    return await InvoiceService.update_invoice(invoice_id, invoice_create_dto, db)

@invoice_router.delete(
    "/{invoice_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Invoice not found"},
        204: {"description": "Invoice deleted successfully"},
    },
)
async def delete_invoice(invoice_id: int, db: AsyncSession = Depends(get_db)):
    await InvoiceService.delete_invoice(invoice_id, db)
    return