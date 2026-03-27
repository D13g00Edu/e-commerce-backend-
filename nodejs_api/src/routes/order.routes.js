const express = require('express');
const router = express.Router();

const orderController = require('../controllers/order.controller');
const authMiddleware = require('../middlewares/auth.middleware');

router.use(authMiddleware);

router.get('/', orderController.getMyOrders);
router.get('/:id', orderController.getMyOrderById);

module.exports = router;