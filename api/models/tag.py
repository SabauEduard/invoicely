from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database import Base
from .invoice import invoice_tags

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable=False)

    invoices = relationship("Invoice", secondary=invoice_tags, back_populates="tags")