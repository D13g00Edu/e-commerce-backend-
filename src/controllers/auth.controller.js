const { registerUser, loginUser } = require('../services/auth.service');

const register = async (req, res, next) => {
  try {
    const { name, email, password } = req.body;

    const result = await registerUser({ name, email, password });

    res.status(201).json({
      ok: true,
      message: 'Usuario registrado correctamente',
      ...result,
    });
  } catch (error) {
    next(error);
  }
};

const login = async (req, res, next) => {
  try {
    const { email, password } = req.body;

    const result = await loginUser({ email, password });

    res.status(200).json({
      ok: true,
      message: 'Login exitoso',
      ...result,
    });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  register,
  login,
};