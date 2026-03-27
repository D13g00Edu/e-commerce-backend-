// src/app.js
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';

import { errorHandler } from './middlewares/errorHandler.js';
import { publicLimiter } from './middlewares/rateLimit.js';
import { sanitizeInput } from './middlewares/sanitize.js';

import productRoutes from './routes/product.routes.js';
import cartRoutes from './routes/cart.routes.js';
import orderRoutes from './routes/order.routes.js';
import authRoutes from './routes/auth.routes.js';

const app = express();

app.disable('x-powered-by');

app.use(helmet());

app.use(cors({
  origin: ['http://localhost:3000'], // cambia esto para tu frontend real
  credentials: true,
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(sanitizeInput);

// Rate limit para rutas públicas generales
app.use('/api', publicLimiter);

app.use('/api/auth', authRoutes);
app.use('/api/products', productRoutes);
app.use('/api/cart', cartRoutes);
app.use('/api/orders', orderRoutes);

app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: 'Ruta no encontrada',
  });
});

app.use(errorHandler);

export default app;