const checkoutService = require('../services/checkout.service');

const createCheckout = async (req, res, next) => {
  try {
    const result = await checkoutService.createCheckoutSession(req.user.id);
    res.status(201).json(result);
  } catch (error) {
    if (error.message === 'EMPTY_CART') {
      return res.status(400).json({ message: 'El carrito está vacío' });
    }

    if (error.message === 'PRODUCT_NOT_FOUND') {
      return res.status(404).json({ message: 'Producto no encontrado' });
    }

    if (error.message === 'INSUFFICIENT_STOCK') {
      return res.status(400).json({ message: 'Stock insuficiente' });
    }

    next(error);
  }
};

const confirmPayment = async (req, res, next) => {
  try {
    const result = await checkoutService.confirmCheckoutPayment(
      req.user.id,
      req.params.orderId
    );

    res.json(result);
  } catch (error) {
    if (error.message === 'ORDER_NOT_FOUND') {
      return res.status(404).json({ message: 'Orden no encontrada' });
    }

    if (error.message === 'PAYMENT_NOT_FOUND') {
      return res.status(404).json({ message: 'Pago no encontrado' });
    }

    if (error.message === 'ORDER_ALREADY_PAID') {
      return res.status(400).json({ message: 'La orden ya fue pagada' });
    }

    if (error.message === 'PRODUCT_NOT_FOUND') {
      return res.status(404).json({ message: 'Producto no encontrado' });
    }

    if (error.message === 'INSUFFICIENT_STOCK') {
      return res.status(400).json({ message: 'Stock insuficiente' });
    }

    next(error);
  }
};

module.exports = {
  createCheckout,
  confirmPayment,
};