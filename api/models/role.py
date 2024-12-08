from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable=False)
    
    users = relationship("User", back_populates="role")
