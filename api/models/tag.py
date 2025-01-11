from sqlalchemy import Column, String, Integer
from database import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable=False)