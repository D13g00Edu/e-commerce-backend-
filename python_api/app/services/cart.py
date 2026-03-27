from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestException, NotFoundException
from app.models.cart import Cart
from app.repositories.cart import CartRepository
from app.repositories.product import ProductRepository
from app.schemas.cart import CartItemAdd, CartItemUpdate


class CartService:
    def __init__(self, db: AsyncSession):
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)

    async def get_cart(self, user_id: int) -> Cart:
        return await self.cart_repo.get_or_create(user_id)

    async def add_item(self, user_id: int, data: CartItemAdd) -> Cart:
        product = await self.product_repo.get_by_id(data.product_id)
        if not product or not product.is_active:
            raise NotFoundException("Product not found")
        if product.stock < data.quantity:
            raise BadRequestException(f"Insufficient stock (available: {product.stock})")

        cart = await self.cart_repo.get_or_create(user_id)
        await self.cart_repo.add_item(cart.id, data.product_id, data.quantity)
        return await self.cart_repo.get_by_user_id(user_id)

    async def update_item(self, user_id: int, product_id: int, data: CartItemUpdate) -> Cart:
        cart = await self.cart_repo.get_or_create(user_id)
        item = await self.cart_repo.get_item(cart.id, product_id)
        if not item:
            raise NotFoundException("Item not in cart")

        product = await self.product_repo.get_by_id(product_id)
        if product.stock < data.quantity:
            raise BadRequestException(f"Insufficient stock (available: {product.stock})")

        item.quantity = data.quantity
        return await self.cart_repo.get_by_user_id(user_id)

    async def remove_item(self, user_id: int, product_id: int) -> Cart:
        cart = await self.cart_repo.get_or_create(user_id)
        removed = await self.cart_repo.remove_item(cart.id, product_id)
        if not removed:
            raise NotFoundException("Item not in cart")
        return await self.cart_repo.get_by_user_id(user_id)

    async def clear(self, user_id: int) -> Cart:
        cart = await self.cart_repo.get_or_create(user_id)
        await self.cart_repo.clear(cart.id)
        return await self.cart_repo.get_by_user_id(user_id)
