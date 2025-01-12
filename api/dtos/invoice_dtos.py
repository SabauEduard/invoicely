from fastapi import UploadFile

from enums.category import InvoiceCategory
from pydantic import Field, BaseModel, model_validator, json
from typing import Optional

from models.invoice import Invoice
from datetime import datetime


class InvoiceDTO(BaseModel):
    id: int = Field(..., alias="id")
    name: str = Field(..., alias="name")
    user_id: int = Field(..., alias="user_id")
    category: int = Field(..., alias="category")
    path: str = Field(..., alias="path")
    vendor: str = Field(..., alias="vendor")
    amount: float = Field(..., alias="amount")
    status: str = Field(..., alias="status")
    importance: int = Field(..., alias="importance")
    notes: str = Field(None, alias="notes")
    duplicate: bool = Field(..., alias="duplicate")
    incomplete: bool = Field(None, alias="incomplete")
    emission_date: Optional[datetime] = Field(None, alias="emission_date")
    due_date: Optional[datetime] = Field(None, alias="due_date")

    @staticmethod
    def from_invoice(invoice: Invoice):
        return InvoiceDTO(
            id=invoice.id,
            name=invoice.name,
            user_id=invoice.user_id,
            category=invoice.category,
            path=invoice.path,
            vendor=invoice.vendor,
            amount=invoice.amount,
            status=invoice.status,
            importance=invoice.importance,
            notes=invoice.notes,
            duplicate=invoice.duplicate,
            incomplete=invoice.incomplete,
            emission_date=invoice.emission_date,
            due_date=invoice.due_date
        )


class InvoiceCreateDTO(BaseModel):
    name: str = Field(..., alias="name")
    user_id: Optional[int] = Field(None, alias="user_id")
    category: int = Field(..., alias="category")
    vendor: str = Field(..., alias="vendor")
    amount: float = Field(..., alias="amount")
    status: str = Field(..., alias="status")
    importance: int = Field(..., alias="importance")
    notes: str = Field(None, alias="notes")
    duplicate: bool = Field(..., alias="duplicate")
    incomplete: bool = Field(None, alias="incomplete")
    emission_date: str = Field(None, alias="emission_date")
    due_date: str = Field(None, alias="due_date")
    
    def to_invoice(self):
        return Invoice(
            name=self.name,
            user_id=self.user_id,
            category=InvoiceCategory(self.category),
            path=f"api/uploads/{self.user_id}/{self.category}/{self.vendor}/{self.name}",
            vendor=self.vendor,
            amount=self.amount,
            status=self.status,
            importance=self.importance,
            notes=self.notes,
            duplicate=self.duplicate,
            incomplete=self.incomplete,
            emission_date=datetime.strptime(self.emission_date, "%Y-%m-%d") if self.emission_date else None,
            due_date=datetime.strptime(self.due_date, "%Y-%m-%d") if self.due_date else None
        )
