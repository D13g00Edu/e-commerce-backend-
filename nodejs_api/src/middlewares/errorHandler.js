// src/middlewares/errorHandler.js
export const errorHandler = (err, req, res, next) => {
  console.error(err);

  const statusCode = err.statusCode || 500;
  const isProd = process.env.NODE_ENV === 'production';

  return res.status(statusCode).json({
    success: false,
    message: err.message || 'Error interno del servidor',
    ...(isProd ? {} : { stack: err.stack }),
  });
};
