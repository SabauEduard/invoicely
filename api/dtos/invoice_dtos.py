from enums.category import InvoiceCategory
from pydantic import Field, BaseModel
from typing import Optional

from models.invoice import Invoice
from datetime import datetime


class InvoiceDTO(BaseModel):
    id: int = Field(..., alias="id")
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
    emitted_date: Optional[datetime] = Field(None, alias="emitted_date")
    expiry_date: Optional[datetime] = Field(None, alias="expiry_date")

    @staticmethod
    def from_invoice(invoice: Invoice):
        return InvoiceDTO(
            id=invoice.id,
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
            emitted_date=invoice.emitted_date,
            expiry_date=invoice.expiry_date
        )


class InvoiceCreateDTO(BaseModel):
    user_id: Optional[int] = Field(None, alias="user_id")
    category: int = Field(..., alias="category")
    path: str = Field(..., alias="path")
    vendor: str = Field(..., alias="vendor")
    amount: float = Field(..., alias="amount")
    status: str = Field(..., alias="status")
    importance: int = Field(..., alias="importance")
    notes: str = Field(None, alias="notes")
    duplicate: bool = Field(..., alias="duplicate")
    incomplete: bool = Field(None, alias="incomplete")
    emitted_date: str = Field(None, alias="emitted_date")
    expiry_date: str = Field(None, alias="expiry_date")

    def to_invoice(self):
        return Invoice(
            user_id=self.user_id,
            category=InvoiceCategory(self.category),
            path=self.path,
            vendor=self.vendor,
            amount=self.amount,
            status=self.status,
            importance=self.importance,
            notes=self.notes,
            duplicate=self.duplicate,
            incomplete=self.incomplete,
            emitted_date=datetime.strptime(self.emitted_date, "%Y-%m-%d") if self.emitted_date else None,
            expiry_date=datetime.strptime(self.expiry_date, "%Y-%m-%d") if self.expiry_date else None
        )
