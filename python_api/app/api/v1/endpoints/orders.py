from typing import List

from fastapi import APIRouter, Query

from app.core.dependencies import CurrentAdmin, CurrentUser, DBSession
from app.schemas.order import OrderResponse, OrderStatusUpdate
from app.services.order import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(current_user: CurrentUser, db: DBSession):
    """Create an order from the current cart."""
    service = OrderService(db)
    return await service.create_from_cart(current_user.id)


@router.get("", response_model=List[OrderResponse])
async def list_orders(
    current_user: CurrentUser,
    db: DBSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List current user's orders."""
    service = OrderService(db)
    return await service.get_user_orders(current_user.id, page=page, page_size=page_size)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, current_user: CurrentUser, db: DBSession):
    """Get order detail."""
    service = OrderService(db)
    return await service.get_order_or_404(order_id, current_user.id)


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: DBSession,
    _: CurrentAdmin,
):
    """Update order status (admin only)."""
    service = OrderService(db)
    return await service.update_status(order_id, data.status)
