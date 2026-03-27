// src/middlewares/authorizeRoles.js
export const authorizeRoles = (...allowedRoles) => {
  return (req, res, next) => {
    try {
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'No autenticado',
        });
      }

      if (!allowedRoles.includes(req.user.role)) {
        return res.status(403).json({
          success: false,
          message: 'No autorizado para acceder a este recurso',
        });
      }

      next();
    } catch (error) {
      next(error);
    }
  };
};