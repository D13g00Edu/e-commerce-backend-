const express = require('express');
const router = express.Router();

const checkoutController = require('../controllers/checkout.controller');
const authMiddleware = require('../middlewares/auth.middleware');

router.use(authMiddleware);

router.post('/', checkoutController.createCheckout);
router.post('/:orderId/confirm', checkoutController.confirmPayment);

module.exports = router;