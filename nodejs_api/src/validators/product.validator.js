// src/validators/product.validator.js
import { z } from 'zod';

export const createProductSchema = {
  body: z.object({
    name: z.string().trim().min(1, 'El nombre es requerido'),
    description: z.string().trim().optional(),
    price: z.number().positive('El precio debe ser mayor a 0'),
    stock: z.number().int().min(0, 'El stock no puede ser negativo'),
    category: z.string().trim().min(1, 'La categoría es requerida'),
    imageUrl: z.string().url('imageUrl debe ser una URL válida').optional(),
  }),
};

export const updateProductSchema = {
  params: z.object({
    id: z.coerce.number().int().positive(),
  }),
  body: z.object({
    name: z.string().trim().min(1).optional(),
    description: z.string().trim().optional(),
    price: z.number().positive().optional(),
    stock: z.number().int().min(0).optional(),
    category: z.string().trim().min(1).optional(),
    imageUrl: z.string().url().optional(),
  }),
};

export const productIdParamSchema = {
  params: z.object({
    id: z.coerce.number().int().positive(),
  }),
};

export const productQuerySchema = {
  query: z.object({
    search: z.string().trim().optional(),
    category: z.string().trim().optional(),
    minPrice: z.coerce.number().min(0).optional(),
    maxPrice: z.coerce.number().min(0).optional(),
  }),
};