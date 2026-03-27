const prisma = require('../config/db');

const getOrdersByUserId = async (userId) => {
  return await prisma.order.findMany({
    where: { userId },
    include: {
      items: {
        include: {
          product: true,
        },
      },
      payment: true,
    },
    orderBy: {
      createdAt: 'desc',
    },
  });
};

const getOrderById = async (userId, orderId) => {
  const order = await prisma.order.findUnique({
    where: { id: Number(orderId) },
    include: {
      items: {
        include: {
          product: true,
        },
      },
      payment: true,
    },
  });

  if (!order || order.userId !== userId) {
    throw new Error('ORDER_NOT_FOUND');
  }

  return order;
};

module.exports = {
  getOrdersByUserId,
  getOrderById,
};