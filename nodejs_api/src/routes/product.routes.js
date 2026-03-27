// src/routes/product.routes.js
import { Router } from 'express';
import * as productController from '../controllers/product.controller.js';
import { auth } from '../middlewares/auth.middleware.js';
import { authorizeRoles } from '../middlewares/authorizeRoles.js';
import { validateRequest } from '../middlewares/validateRequest.js';
import {
  createProductSchema,
  updateProductSchema,
  productIdParamSchema,
  productQuerySchema,
} from '../validators/product.validator.js';

const router = Router();

// Públicos
router.get(
  '/',
  validateRequest(productQuerySchema),
  productController.getProducts
);

router.get(
  '/:id',
  validateRequest(productIdParamSchema),
  productController.getProductById
);

// Solo ADMIN
router.post(
  '/',
  auth,
  authorizeRoles('ADMIN'),
  validateRequest(createProductSchema),
  productController.createProduct
);

router.put(
  '/:id',
  auth,
  authorizeRoles('ADMIN'),
  validateRequest(updateProductSchema),
  productController.updateProduct
);

router.delete(
  '/:id',
  auth,
  authorizeRoles('ADMIN'),
  validateRequest(productIdParamSchema),
  productController.deleteProduct
);

export default router;