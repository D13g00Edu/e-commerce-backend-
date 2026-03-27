import enum

from sqlalchemy import Boolean, Column, Enum, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    cart = relationship("Cart", back_populates="user", uselist=False, lazy="selectin")
    orders = relationship("Order", back_populates="user", lazy="selectin")
