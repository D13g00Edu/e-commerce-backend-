from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment, PaymentStatus
from app.repositories.base import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, db: AsyncSession):
        super().__init__(Payment, db)

    async def get_by_order_id(self, order_id: int) -> Optional[Payment]:
        result = await self.db.execute(select(Payment).where(Payment.order_id == order_id))
        return result.scalar_one_or_none()

    async def get_by_stripe_intent(self, intent_id: str) -> Optional[Payment]:
        result = await self.db.execute(
            select(Payment).where(Payment.stripe_payment_intent_id == intent_id)
        )
        return result.scalar_one_or_none()

    async def update_status(self, payment_id: int, status: PaymentStatus) -> Optional[Payment]:
        payment = await self.get_by_id(payment_id)
        if payment:
            payment.status = status
            await self.db.flush()
        return payment
