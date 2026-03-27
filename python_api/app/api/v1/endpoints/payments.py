from fastapi import APIRouter, Header, Request

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.payment import CheckoutResponse
from app.services.payment import PaymentService

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/checkout/{order_id}", response_model=CheckoutResponse)
async def checkout(order_id: int, current_user: CurrentUser, db: DBSession):
    """
    Initiate Stripe payment for an order.
    Returns a client_secret to confirm the payment on the frontend.
    """
    service = PaymentService(db)
    return await service.create_checkout(order_id, current_user.id)


@router.post("/webhook", include_in_schema=False)
async def stripe_webhook(
    request: Request,
    db: DBSession,
    stripe_signature: str = Header(None, alias="stripe-signature"),
):
    """Stripe webhook handler (called by Stripe, not the client)."""
    payload = await request.body()
    service = PaymentService(db)
    return await service.handle_webhook(payload, stripe_signature)
