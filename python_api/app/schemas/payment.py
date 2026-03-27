from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.payment import PaymentStatus


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    stripe_payment_intent_id: Optional[str]
    client_secret: Optional[str]
    amount: float
    currency: str
    status: PaymentStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class CheckoutResponse(BaseModel):
    order_id: int
    payment_id: int
    client_secret: str
    amount: float
    currency: str
