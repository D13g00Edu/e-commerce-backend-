const express = require('express');
const router = express.Router();

const authRoutes = require('./auth.routes');
const authMiddleware = require('../middlewares/auth.middleware');

router.get('/health', (req, res) => {
  res.status(200).json({
    ok: true,
    message: 'API funcionando correctamente',
  });
});

router.use('/auth', authRoutes);

router.get('/profile', authMiddleware, (req, res) => {
  res.status(200).json({
    ok: true,
    message: 'Ruta privada',
    user: req.user,
  });
});

module.exports = router;