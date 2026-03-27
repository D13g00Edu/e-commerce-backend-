const productService = require('../services/product.service');

const getProducts = async (req, res, next) => {
  try {
    const products = await productService.getAllProducts(req.query);
    res.json(products);
  } catch (error) {
    next(error);
  }
};

const getProduct = async (req, res, next) => {
  try {
    const product = await productService.getProductById(req.params.id);

    if (!product) {
      return res.status(404).json({ message: 'Producto no encontrado' });
    }

    res.json(product);
  } catch (error) {
    next(error);
  }
};

const createProduct = async (req, res, next) => {
  try {
    const { name, price, stock } = req.body;

    if (!name || price == null || stock == null) {
      return res.status(400).json({
        message: 'name, price y stock son obligatorios',
      });
    }

    const product = await productService.createProduct({
      ...req.body,
      price: Number(price),
      stock: Number(stock),
    });

    res.status(201).json(product);
  } catch (error) {
    next(error);
  }
};

const updateProduct = async (req, res, next) => {
  try {
    const existing = await productService.getProductById(req.params.id);

    if (!existing) {
      return res.status(404).json({ message: 'Producto no encontrado' });
    }

    const updated = await productService.updateProduct(req.params.id, {
      ...req.body,
      price: req.body.price != null ? Number(req.body.price) : existing.price,
      stock: req.body.stock != null ? Number(req.body.stock) : existing.stock,
    });

    res.json(updated);
  } catch (error) {
    next(error);
  }
};

const deleteProduct = async (req, res, next) => {
  try {
    const existing = await productService.getProductById(req.params.id);

    if (!existing) {
      return res.status(404).json({ message: 'Producto no encontrado' });
    }

    await productService.deleteProduct(req.params.id);

    res.json({ message: 'Producto eliminado correctamente' });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getProducts,
  getProduct,
  createProduct,
  updateProduct,
  deleteProduct,
};