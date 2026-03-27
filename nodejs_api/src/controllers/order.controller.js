const orderService = require('../services/order.service');

const getMyOrders = async (req, res, next) => {
  try {
    const orders = await orderService.getOrdersByUserId(req.user.id);
    res.json(orders);
  } catch (error) {
    next(error);
  }
};

const getMyOrderById = async (req, res, next) => {
  try {
    const order = await orderService.getOrderById(req.user.id, req.params.id);
    res.json(order);
  } catch (error) {
    if (error.message === 'ORDER_NOT_FOUND') {
      return res.status(404).json({ message: 'Orden no encontrada' });
    }

    next(error);
  }
};

module.exports = {
  getMyOrders,
  getMyOrderById,
};