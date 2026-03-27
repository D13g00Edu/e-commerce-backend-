from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, db: AsyncSession):
        super().__init__(Order, db)

    async def get_user_orders(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Order]:
        result = await self.db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update_status(self, order_id: int, status: OrderStatus) -> Optional[Order]:
        order = await self.get_by_id(order_id)
        if order:
            order.status = status
            await self.db.flush()
        return order
