from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean, Enum, DateTime, Table
from sqlalchemy.types import DECIMAL, TEXT
from sqlalchemy.orm import relationship
from database import Base
from enums.category import InvoiceCategory
from enums.importance import Importance

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

    status = Column(String(32), nullable=False)
    
    content = Column(Text, nullable=True)

    importance = Column(Enum(Importance), nullable=False)

    notes = Column(String(256), nullable=True)

    duplicate = Column(Boolean, nullable=False)

    incomplete = Column(Boolean)

    emission_date = Column(DateTime)

    due_date = Column(DateTime)

    user = relationship("User", back_populates="invoices")

    tags = relationship("Tag", secondary=invoice_tags)
