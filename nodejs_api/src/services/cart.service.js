const prisma = require('../config/db');

const getOrCreateCart = async (userId) => {
  let cart = await prisma.cart.findUnique({
    where: { userId },
  });

  if (!cart) {
    cart = await prisma.cart.create({
      data: { userId },
    });
  }

  return cart;
};

const getCartByUserId = async (userId) => {
  const cart = await getOrCreateCart(userId);

  const fullCart = await prisma.cart.findUnique({
    where: { id: cart.id },
    include: {
      items: {
        include: {
          product: true,
        },
      },
    },
  });

  const subtotal = fullCart.items.reduce((acc, item) => {
    return acc + Number(item.product.price) * item.quantity;
  }, 0);

  return {
    ...fullCart,
    subtotal,
  };
};

const addItemToCart = async (userId, productId, quantity) => {
  const cart = await getOrCreateCart(userId);

  const product = await prisma.product.findUnique({
    where: { id: Number(productId) },
  });

  if (!product) {
    throw new Error('PRODUCT_NOT_FOUND');
  }

  if (product.stock < quantity) {
    throw new Error('INSUFFICIENT_STOCK');
  }

  const existingItem = await prisma.cartItem.findUnique({
    where: {
      cartId_productId: {
        cartId: cart.id,
        productId: Number(productId),
      },
    },
  });

  if (existingItem) {
    const newQuantity = existingItem.quantity + quantity;

    if (product.stock < newQuantity) {
      throw new Error('INSUFFICIENT_STOCK');
    }

    return await prisma.cartItem.update({
      where: { id: existingItem.id },
      data: { quantity: newQuantity },
    });
  }

  return await prisma.cartItem.create({
    data: {
      cartId: cart.id,
      productId: Number(productId),
      quantity,
    },
  });
};

const updateCartItem = async (userId, itemId, quantity) => {
  const item = await prisma.cartItem.findUnique({
    where: { id: Number(itemId) },
    include: {
      cart: true,
      product: true,
    },
  });

  if (!item || item.cart.userId !== userId) {
    throw new Error('ITEM_NOT_FOUND');
  }

  if (quantity <= 0) {
    throw new Error('INVALID_QUANTITY');
  }

  if (item.product.stock < quantity) {
    throw new Error('INSUFFICIENT_STOCK');
  }

  return await prisma.cartItem.update({
    where: { id: Number(itemId) },
    data: { quantity },
  });
};

const removeCartItem = async (userId, itemId) => {
  const item = await prisma.cartItem.findUnique({
    where: { id: Number(itemId) },
    include: {
      cart: true,
    },
  });

  if (!item || item.cart.userId !== userId) {
    throw new Error('ITEM_NOT_FOUND');
  }

  await prisma.cartItem.delete({
    where: { id: Number(itemId) },
  });

  return { message: 'Producto eliminado del carrito' };
};

module.exports = {
  getCartByUserId,
  addItemToCart,
  updateCartItem,
  removeCartItem,
};