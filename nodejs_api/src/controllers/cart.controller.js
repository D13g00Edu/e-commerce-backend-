const cartService = require('../services/cart.service');

const getMyCart = async (req, res, next) => {
  try {
    const cart = await cartService.getCartByUserId(req.user.id);
    res.json(cart);
  } catch (error) {
    next(error);
  }
};

const addItemToCart = async (req, res, next) => {
  try {
    const { productId, quantity } = req.body;

    if (!productId || !quantity) {
      return res.status(400).json({
        message: 'productId y quantity son obligatorios',
      });
    }

    await cartService.addItemToCart(
      req.user.id,
      Number(productId),
      Number(quantity)
    );

    const cart = await cartService.getCartByUserId(req.user.id);
    res.status(201).json(cart);
  } catch (error) {
    if (error.message === 'PRODUCT_NOT_FOUND') {
      return res.status(404).json({ message: 'Producto no encontrado' });
    }

    if (error.message === 'INSUFFICIENT_STOCK') {
      return res.status(400).json({ message: 'Stock insuficiente' });
    }

    next(error);
  }
};

const updateCartItem = async (req, res, next) => {
  try {
    const { quantity } = req.body;

    await cartService.updateCartItem(
      req.user.id,
      req.params.itemId,
      Number(quantity)
    );

    const cart = await cartService.getCartByUserId(req.user.id);
    res.json(cart);
  } catch (error) {
    if (error.message === 'ITEM_NOT_FOUND') {
      return res.status(404).json({ message: 'Item no encontrado' });
    }

    if (error.message === 'INVALID_QUANTITY') {
      return res.status(400).json({ message: 'Cantidad inválida' });
    }

    if (error.message === 'INSUFFICIENT_STOCK') {
      return res.status(400).json({ message: 'Stock insuficiente' });
    }

    next(error);
  }
};

const removeCartItem = async (req, res, next) => {
  try {
    await cartService.removeCartItem(req.user.id, req.params.itemId);

    const cart = await cartService.getCartByUserId(req.user.id);
    res.json(cart);
  } catch (error) {
    if (error.message === 'ITEM_NOT_FOUND') {
      return res.status(404).json({ message: 'Item no encontrado' });
    }

    next(error);
  }
};

module.exports = {
  getMyCart,
  addItemToCart,
  updateCartItem,
  removeCartItem,
};