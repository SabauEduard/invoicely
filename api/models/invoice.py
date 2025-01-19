from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean, Enum, DateTime, Table
from sqlalchemy.types import DECIMAL, TEXT
from sqlalchemy.orm import relationship
from database import Base
from enums.category import InvoiceCategory
from enums.importance import Importance
from enums.status import InvoiceStatus

invoice_tags = Table(
    'invoice_tags',
    Base.metadata,
    Column('invoice_id', Integer, ForeignKey('invoices.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(128), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    category = Column(Enum(InvoiceCategory), nullable=False)

    path = Column(String(256), nullable=False)

    vendor = Column(String(128), nullable=False)

    amount = Column(DECIMAL(10, 2), nullable=False)

    status = Column(Enum(InvoiceStatus), nullable=False)
    
    content = Column(Text, nullable=True)

    importance = Column(Enum(Importance), nullable=False)

    notes = Column(String(256), nullable=True)

    duplicate = Column(Boolean, nullable=False)

    incomplete = Column(Boolean)

    emission_date = Column(DateTime)

    due_date = Column(DateTime)

    user = relationship("User", back_populates="invoices")

    tags = relationship("Tag", secondary=invoice_tags, back_populates="invoices")


class InvoiceBuilder:
    def __init__(self):
        self.invoice = Invoice()

    def with_name(self, name):
        self.invoice.name = name
        return self

    def with_user_id(self, user_id):
        self.invoice.user_id = user_id
        return self

    def with_category(self, category):
        self.invoice.category = category
        return self

    def with_path(self, path):
        self.invoice.path = path
        return self

    def with_vendor(self, vendor):
        self.invoice.vendor = vendor
        return self

    def with_amount(self, amount):
        self.invoice.amount = amount
        return self

    def with_status(self, status):
        self.invoice.status = status
        return self

    def with_importance(self, importance):
        self.invoice.importance = importance
        return self

    def with_notes(self, notes):
        self.invoice.notes = notes
        return self

    def with_duplicate(self, duplicate):
        self.invoice.duplicate = duplicate
        return self

    def with_incomplete(self, incomplete):
        self.invoice.incomplete = incomplete
        return self

    def with_emission_date(self, emission_date):
        self.invoice.emission_date = emission_date
        return self

    def with_due_date(self, due_date):
        self.invoice.due_date = due_date
        return self

    def with_content(self, content):
        self.invoice.content = content
        return self
    
    def with_tags(self, tags):
        self.invoice.tags = tags
        return self

    def build(self):
        return self.invoice