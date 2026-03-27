from typing import List, Optional, Tuple

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: AsyncSession):
        super().__init__(Product, db)

    async def search(
        self,
        *,
        query: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        only_active: bool = True,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[Product], int]:
        stmt = select(Product)

        if only_active:
            stmt = stmt.where(Product.is_active == True)
        if query:
            stmt = stmt.where(
                or_(
                    Product.name.ilike(f"%{query}%"),
                    Product.description.ilike(f"%{query}%"),
                )
            )
        if category:
            stmt = stmt.where(Product.category == category)
        if min_price is not None:
            stmt = stmt.where(Product.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Product.price <= max_price)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.execute(count_stmt)).scalar_one()

        result = await self.db.execute(stmt.offset(skip).limit(limit))
        return list(result.scalars().all()), total

    async def decrement_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        product = await self.get_by_id(product_id)
        if product and product.stock >= quantity:
            product.stock -= quantity
            await self.db.flush()
            return product
        return None
