const prisma = require('../config/db');
const fakeStripe = require('./fakeStripe.service');

const createCheckoutSession = async (userId) => {
  return await prisma.$transaction(async (tx) => {
    const cart = await tx.cart.findUnique({
      where: { userId },
      include: {
        items: {
          include: {
            product: true,
          },
        },
      },
    });

    if (!cart || cart.items.length === 0) {
      throw new Error('EMPTY_CART');
    }

    for (const item of cart.items) {
      if (!item.product) {
        throw new Error('PRODUCT_NOT_FOUND');
      }

      if (item.product.stock < item.quantity) {
        throw new Error('INSUFFICIENT_STOCK');
      }
    }

    const total = cart.items.reduce((acc, item) => {
      return acc + Number(item.product.price) * item.quantity;
    }, 0);

    const order = await tx.order.create({
      data: {
        userId,
        total,
        status: 'PENDING',
      },
    });

    for (const item of cart.items) {
      const unitPrice = Number(item.product.price);
      const subtotal = unitPrice * item.quantity;

      await tx.orderItem.create({
        data: {
          orderId: order.id,
          productId: item.productId,
          quantity: item.quantity,
          unitPrice,
          subtotal,
        },
      });
    }

    const paymentIntent = await fakeStripe.createFakePaymentIntent({
      amount: Math.round(total * 100),
      currency: 'usd',
    });

    const payment = await tx.payment.create({
      data: {
        orderId: order.id,
        amount: total,
        provider: 'fake_stripe',
        providerRef: paymentIntent.id,
        status: 'PENDING',
      },
    });

    return {
      message: 'Checkout creado correctamente',
      orderId: order.id,
      paymentId: payment.id,
      total,
      paymentIntent,
    };
  });
};

const confirmCheckoutPayment = async (userId, orderId) => {
  return await prisma.$transaction(async (tx) => {
    const order = await tx.order.findUnique({
      where: { id: Number(orderId) },
      include: {
        user: true,
        payment: true,
        items: {
          include: {
            product: true,
          },
        },
      },
    });

    if (!order || order.userId !== userId) {
      throw new Error('ORDER_NOT_FOUND');
    }

    if (!order.payment) {
      throw new Error('PAYMENT_NOT_FOUND');
    }

    if (order.status === 'PAID') {
      throw new Error('ORDER_ALREADY_PAID');
    }

    for (const item of order.items) {
      if (!item.product) {
        throw new Error('PRODUCT_NOT_FOUND');
      }

      if (item.product.stock < item.quantity) {
        throw new Error('INSUFFICIENT_STOCK');
      }
    }

    await fakeStripe.confirmFakePaymentIntent(order.payment.providerRef);

    for (const item of order.items) {
      await tx.product.update({
        where: { id: item.productId },
        data: {
          stock: {
            decrement: item.quantity,
          },
        },
      });
    }

    await tx.payment.update({
      where: { id: order.payment.id },
      data: {
        status: 'SUCCEEDED',
      },
    });

    await tx.order.update({
      where: { id: order.id },
      data: {
        status: 'PAID',
      },
    });

    const cart = await tx.cart.findUnique({
      where: { userId },
    });

    if (cart) {
      await tx.cartItem.deleteMany({
        where: { cartId: cart.id },
      });
    }

    return {
      message: 'Pago simulado correctamente',
      orderId: order.id,
      paymentStatus: 'SUCCEEDED',
      orderStatus: 'PAID',
    };
  });
};

module.exports = {
  createCheckoutSession,
  confirmCheckoutPayment,
};