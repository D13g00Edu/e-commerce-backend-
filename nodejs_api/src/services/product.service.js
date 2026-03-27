const prisma = require('../config/db');

const getAllProducts = async (filters = {}) => {
  const { search, category, minPrice, maxPrice } = filters;

  return await prisma.product.findMany({
    where: {
      AND: [
        search
          ? {
              OR: [
                { name: { contains: search, mode: 'insensitive' } },
                { description: { contains: search, mode: 'insensitive' } },
              ],
            }
          : {},
        category ? { category: { equals: category, mode: 'insensitive' } } : {},
        minPrice ? { price: { gte: Number(minPrice) } } : {},
        maxPrice ? { price: { lte: Number(maxPrice) } } : {},
      ],
    },
    orderBy: { createdAt: 'desc' },
  });
};

const getProductById = async (id) => {
  return await prisma.product.findUnique({
    where: { id: Number(id) },
  });
};

const createProduct = async (data) => {
  return await prisma.product.create({
    data: {
      name: data.name,
      description: data.description,
      price: data.price,
      stock: data.stock,
      imageUrl: data.imageUrl,
      category: data.category,
    },
  });
};

const updateProduct = async (id, data) => {
  return await prisma.product.update({
    where: { id: Number(id) },
    data: {
      name: data.name,
      description: data.description,
      price: data.price,
      stock: data.stock,
      imageUrl: data.imageUrl,
      category: data.category,
    },
  });
};

const deleteProduct = async (id) => {
  return await prisma.product.delete({
    where: { id: Number(id) },
  });
};

module.exports = {
  getAllProducts,
  getProductById,
  createProduct,
  updateProduct,
  deleteProduct,
};