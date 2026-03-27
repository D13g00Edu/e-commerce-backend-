from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.cart import CartItemAdd, CartItemUpdate, CartResponse
from app.services.cart import CartService

router = APIRouter(prefix="/cart", tags=["cart"])


def _build_response(cart) -> CartResponse:
    from app.schemas.cart import CartItemResponse
    return CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        items=[CartItemResponse.from_orm_item(i) for i in cart.items],
        subtotal=cart.subtotal,
    )


@router.get("", response_model=CartResponse)
async def get_cart(current_user: CurrentUser, db: DBSession):
    """Get current user's cart."""
    service = CartService(db)
    cart = await service.get_cart(current_user.id)
    return _build_response(cart)


@router.post("/items", response_model=CartResponse, status_code=201)
async def add_item(data: CartItemAdd, current_user: CurrentUser, db: DBSession):
    """Add a product to the cart."""
    service = CartService(db)
    cart = await service.add_item(current_user.id, data)
    return _build_response(cart)


@router.patch("/items/{product_id}", response_model=CartResponse)
async def update_item(product_id: int, data: CartItemUpdate, current_user: CurrentUser, db: DBSession):
    """Update quantity of a cart item."""
    service = CartService(db)
    cart = await service.update_item(current_user.id, product_id, data)
    return _build_response(cart)


@router.delete("/items/{product_id}", response_model=CartResponse)
async def remove_item(product_id: int, current_user: CurrentUser, db: DBSession):
    """Remove a product from the cart."""
    service = CartService(db)
    cart = await service.remove_item(current_user.id, product_id)
    return _build_response(cart)


@router.delete("", response_model=CartResponse)
async def clear_cart(current_user: CurrentUser, db: DBSession):
    """Remove all items from the cart."""
    service = CartService(db)
    cart = await service.clear(current_user.id)
    return _build_response(cart)
