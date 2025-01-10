from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    is_2fa_enabled = Column(Boolean, default=False)
    otp_secret = Column(String(100), nullable=True)
    
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    creation_date = Column(DateTime, server_default=func.now(), nullable=False)
    deletion_date = Column(DateTime, nullable=True)

    role = relationship("Role", back_populates="users")
