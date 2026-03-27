from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestException, NotFoundException
from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.cart import CartRepository
from app.repositories.order import OrderRepository
from app.repositories.product import ProductRepository


class OrderService:
    def __init__(self, db: AsyncSession):
        self.order_repo = OrderRepository(db)
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)

    async def create_from_cart(self, user_id: int) -> Order:
        cart = await self.cart_repo.get_by_user_id(user_id)
        if not cart or not cart.items:
            raise BadRequestException("Cart is empty")

        total = 0.0
        order_items = []

        for item in cart.items:
            product = await self.product_repo.get_by_id(item.product_id)
            if not product or not product.is_active:
                raise BadRequestException(f"Product '{item.product_id}' is unavailable")
            if product.stock < item.quantity:
                raise BadRequestException(f"Insufficient stock for '{product.name}'")

            # Snapshot price at purchase time
            order_items.append(
                OrderItem(
                    product_id=product.id,
                    quantity=item.quantity,
                    unit_price=product.price,
                )
            )
            total += product.price * item.quantity

            # Decrement stock
            await self.product_repo.decrement_stock(product.id, item.quantity)

        order = Order(user_id=user_id, total=round(total, 2), status=OrderStatus.PENDING)
        order = await self.order_repo.create(order)

        for oi in order_items:
            oi.order_id = order.id
            self.order_repo.db.add(oi)

        return order

    async def get_user_orders(self, user_id: int, page: int = 1, page_size: int = 20) -> List[Order]:
        skip = (page - 1) * page_size
        return await self.order_repo.get_user_orders(user_id, skip=skip, limit=page_size)

    async def get_order_or_404(self, order_id: int, user_id: int) -> Order:
        order = await self.order_repo.get_by_id(order_id)
        if not order or order.user_id != user_id:
            raise NotFoundException("Order not found")
        return order

    async def update_status(self, order_id: int, status: OrderStatus) -> Order:
        order = await self.order_repo.update_status(order_id, status)
        if not order:
            raise NotFoundException("Order not found")
        return order
