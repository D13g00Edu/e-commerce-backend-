import stripe
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import BadRequestException, NotFoundException, PaymentException
from app.models.order import OrderStatus
from app.models.payment import Payment, PaymentStatus
from app.repositories.order import OrderRepository
from app.repositories.payment import PaymentRepository
from app.repositories.cart import CartRepository
from app.schemas.payment import CheckoutResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    def __init__(self, db: AsyncSession):
        self.payment_repo = PaymentRepository(db)
        self.order_repo = OrderRepository(db)
        self.cart_repo = CartRepository(db)

    async def create_checkout(self, order_id: int, user_id: int) -> CheckoutResponse:
        order = await self.order_repo.get_by_id(order_id)
        if not order or order.user_id != user_id:
            raise NotFoundException("Order not found")
        if order.status != OrderStatus.PENDING:
            raise BadRequestException("Order is not in pending state")

        existing = await self.payment_repo.get_by_order_id(order_id)
        if existing and existing.status == PaymentStatus.SUCCEEDED:
            raise BadRequestException("Order already paid")

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(order.total * 100),  # Stripe uses cents
                currency="usd",
                metadata={"order_id": order_id, "user_id": user_id},
            )
        except stripe.StripeError as e:
            raise PaymentException(str(e))

        if existing:
            payment = await self.payment_repo.update(
                existing,
                {
                    "stripe_payment_intent_id": intent.id,
                    "stripe_client_secret": intent.client_secret,
                    "status": PaymentStatus.PENDING,
                },
            )
        else:
            payment = Payment(
                order_id=order_id,
                stripe_payment_intent_id=intent.id,
                stripe_client_secret=intent.client_secret,
                amount=order.total,
                currency="usd",
                status=PaymentStatus.PENDING,
            )
            payment = await self.payment_repo.create(payment)

        return CheckoutResponse(
            order_id=order_id,
            payment_id=payment.id,
            client_secret=intent.client_secret,
            amount=order.total,
            currency="usd",
        )

    async def handle_webhook(self, payload: bytes, sig_header: str) -> dict:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except stripe.SignatureVerificationError:
            raise BadRequestException("Invalid webhook signature")

        if event["type"] == "payment_intent.succeeded":
            intent = event["data"]["object"]
            await self._on_payment_succeeded(intent["id"])
        elif event["type"] == "payment_intent.payment_failed":
            intent = event["data"]["object"]
            await self._on_payment_failed(intent["id"])

        return {"received": True}

    async def _on_payment_succeeded(self, intent_id: str) -> None:
        payment = await self.payment_repo.get_by_stripe_intent(intent_id)
        if not payment:
            return
        await self.payment_repo.update_status(payment.id, PaymentStatus.SUCCEEDED)
        await self.order_repo.update_status(payment.order_id, OrderStatus.PAID)
        # Clear cart after successful payment
        order = await self.order_repo.get_by_id(payment.order_id)
        if order:
            cart = await self.cart_repo.get_by_user_id(order.user_id)
            if cart:
                await self.cart_repo.clear(cart.id)

    async def _on_payment_failed(self, intent_id: str) -> None:
        payment = await self.payment_repo.get_by_stripe_intent(intent_id)
        if not payment:
            return
        await self.payment_repo.update_status(payment.id, PaymentStatus.FAILED)
        await self.order_repo.update_status(payment.order_id, OrderStatus.CANCELLED)
