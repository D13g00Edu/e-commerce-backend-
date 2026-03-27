from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cart import Cart, CartItem
from app.repositories.base import BaseRepository


class CartRepository(BaseRepository[Cart]):
    def __init__(self, db: AsyncSession):
        super().__init__(Cart, db)

    async def get_by_user_id(self, user_id: int) -> Optional[Cart]:
        result = await self.db.execute(
            select(Cart)
            .where(Cart.user_id == user_id)
            .options(selectinload(Cart.items).selectinload(CartItem.product))
        )
        return result.scalar_one_or_none()

    async def get_or_create(self, user_id: int) -> Cart:
        cart = await self.get_by_user_id(user_id)
        if not cart:
            cart = Cart(user_id=user_id)
            cart = await self.create(cart)
        return cart

    async def get_item(self, cart_id: int, product_id: int) -> Optional[CartItem]:
        result = await self.db.execute(
            select(CartItem).where(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id,
            )
        )
        return result.scalar_one_or_none()

    async def add_item(self, cart_id: int, product_id: int, quantity: int) -> CartItem:
        existing = await self.get_item(cart_id, product_id)
        if existing:
            existing.quantity += quantity
            await self.db.flush()
            return existing
        item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        self.db.add(item)
        await self.db.flush()
        return item

    async def remove_item(self, cart_id: int, product_id: int) -> bool:
        item = await self.get_item(cart_id, product_id)
        if item:
            await self.db.delete(item)
            await self.db.flush()
            return True
        return False

    async def clear(self, cart_id: int) -> None:
        cart = await self.get_by_id(cart_id)
        if cart:
            for item in list(cart.items):
                await self.db.delete(item)
            await self.db.flush()
