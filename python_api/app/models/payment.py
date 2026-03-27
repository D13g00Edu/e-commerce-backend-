import enum

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    stripe_payment_intent_id = Column(String(255), unique=True, nullable=True)
    stripe_client_secret = Column(String(500), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="usd", nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)

    order = relationship("Order", back_populates="payment")
