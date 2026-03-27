from fastapi import APIRouter

from app.api.v1.endpoints import auth, cart, orders, payments, products, users

router = APIRouter()

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(products.router)
router.include_router(cart.router)
router.include_router(orders.router)
router.include_router(payments.router)
