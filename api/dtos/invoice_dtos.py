from fastapi import UploadFile, Form, File

from enums.category import InvoiceCategory
from enums.importance import Importance
from enums.status import InvoiceStatus
from pydantic import Field, BaseModel, model_validator, json
from typing import Optional

from models.invoice import Invoice, InvoiceBuilder
from datetime import datetime


class InvoiceDTO(BaseModel):
    id: int = Field(..., alias="id")
    name: str = Field(..., alias="name")
    user_id: int = Field(..., alias="user_id")
    category: InvoiceCategory = Field(..., alias="category")
    path: str = Field(..., alias="path")
    vendor: str = Field(..., alias="vendor")
    amount: float = Field(..., alias="amount")
    status: InvoiceStatus = Field(..., alias="status")
    importance: Importance = Field(..., alias="importance")
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
    category: InvoiceCategory = Field(None, alias="category")
    vendor: str = Field(..., alias="vendor")
    amount: float = Field(..., alias="amount")
    status: InvoiceStatus = Field(..., alias="status")
    importance: Importance = Field(..., alias="importance")
    notes: str = Field(None, alias="notes")
    duplicate: bool = Field(None, alias="duplicate")
    incomplete: bool = Field(None, alias="incomplete")
    emission_date: str = Field(None, alias="emission_date")
    due_date: str = Field(None, alias="due_date")
    file: UploadFile = File(..., alias="file")
    path: str = Field(None, alias="path")
    content: str = Field(None, alias="content")

    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            file: UploadFile = File(...),
            vendor: str = Form(...),
            amount: float = Form(...),
            status: str = Form(...),
            importance: str = Form(...),
            notes: str = Form(None),
            emission_date: str = Form(...),
            due_date: str = Form(...),
    ):
        return cls(
            name=name,
            file=file,
            vendor=vendor,
            amount=amount,
            status=status,
            importance=importance,
            notes=notes,
            emission_date=emission_date,
            due_date=due_date,
        )

    def to_invoice(self):
        invoice = (
            InvoiceBuilder()
            .with_name(self.name)
            .with_user_id(self.user_id)
            .with_category(InvoiceCategory(self.category))
            .with_path(self.path)
            .with_content(self.content)
            .with_vendor(self.vendor)
            .with_amount(self.amount)
            .with_status(self.status)
            .with_importance(Importance(self.importance))
            .with_notes(self.notes)
            .with_duplicate(self.duplicate)
            .with_incomplete(self.incomplete)
            .with_emission_date(datetime.strptime(self.emission_date, "%Y-%m-%d") if self.emission_date else None)
            .with_due_date(datetime.strptime(self.due_date, "%Y-%m-%d") if self.due_date else None)
            .build()
        )
        return invoice
