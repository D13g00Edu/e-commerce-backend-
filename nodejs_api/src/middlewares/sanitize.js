// src/middlewares/sanitize.js
const cleanString = (value) => {
  if (typeof value !== 'string') return value;

  return value
    .replace(/<script.*?>.*?<\/script>/gi, '')
    .replace(/[<>]/g, '')
    .trim();
};

const deepSanitize = (obj) => {
  if (Array.isArray(obj)) {
    return obj.map(deepSanitize);
  }

  if (obj && typeof obj === 'object') {
    const sanitized = {};
    for (const key in obj) {
      sanitized[key] = deepSanitize(obj[key]);
    }
    return sanitized;
  }

  return cleanString(obj);
};

export const sanitizeInput = (req, res, next) => {
  if (req.body) req.body = deepSanitize(req.body);
  if (req.query) req.query = deepSanitize(req.query);
  if (req.params) req.params = deepSanitize(req.params);

  next();
};