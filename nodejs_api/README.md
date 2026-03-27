# Ecommerce Backend (Node.js + Express + Prisma)

Proyecto backend de ejemplo para una tienda ecommerce, construido con Node.js, Express, Prisma y PostgreSQL.

## 🚀 Tecnologías

- Node.js
- Express (v5)
- Prisma (ORM)
- PostgreSQL
- JWT
- bcryptjs
- helmet + cors
- express-rate-limit
- zod

## 📁 Estructura principal

- `src/app.js` - configuración de app Express y middlewares.
- `src/server.js` - arranque del servidor.
- `src/config/db.js` - conexión a Prisma/PostgreSQL.
- `src/controllers/` - controladores de rutas.
- `src/routes/` - definiciones de rutas.
- `src/services/` - lógica de negocio.
- `src/middlewares/` - validaciones y manejo de errores.
- `src/utils/` - utilidad para errores y JWT.
- `src/validators/` - validaciones con zod.

## 🔧 Configuración

1. Clonar el repositorio.

2. Instalar dependencias:

```bash
npm install
```

3. Crear archivo `.env` con variables necesarias:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
JWT_SECRET=tu_clave_secreta
JWT_EXPIRES_IN=1h
PORT=3000
```

4. Generar o aplicar migraciones Prisma:

```bash
npx prisma migrate dev --name init
```

5. Ejecutar en modo desarrollo:

```bash
npm run dev
```

## ▶️ Scripts

- `npm run dev`: nodemon en `src/server.js`.
- `npm start`: arranca `src/server.js` en producción.
- `npm run prisma:init`: inicializa Prisma.

## 🔐 Funcionalidades esperadas

- Registro de usuarios
- Login con JWT
- CRUD de productos
- Carrito de compras
- Checkout y órdenes
- Autorización por roles
- Sanitización y validación de requests

## ✅ Swagger / Postman

(Agregar colección de Postman o Swagger si se implementa en el futuro.)

## 🛠 Mejores prácticas

- Mantener `DATABASE_URL` y `JWT_SECRET` en `.env` seguro.
- No subir archivos de migración generados en entornos temporales.

## 📄 Más información

- Prisma: https://www.prisma.io/
- Express: https://expressjs.com/
- JWT: https://jwt.io/
