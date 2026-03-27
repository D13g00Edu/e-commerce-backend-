# 🛒 E-commerce API

REST API para plataforma de comercio electrónico construida con **FastAPI**, **SQLAlchemy async** y **PostgreSQL**.

---

## Stack

| Capa | Tecnología |
|---|---|
| Framework | FastAPI 0.111 |
| ORM | SQLAlchemy 2.0 (async) |
| Base de datos | PostgreSQL 16 |
| Migraciones | Alembic |
| Auth | JWT (python-jose) + bcrypt |
| Pagos | Stripe |
| Rate limiting | SlowAPI |
| Logging | structlog |
| Tests | pytest + pytest-asyncio + httpx |

---

## Estructura del proyecto

```
ecommerce-api/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/        # auth, users, products, cart, orders, payments
│   │   └── router.py
│   ├── core/
│   │   ├── config.py         # Settings con pydantic-settings
│   │   ├── dependencies.py   # get_db, CurrentUser, CurrentAdmin
│   │   ├── exceptions.py     # Excepciones HTTP centralizadas
│   │   └── security.py       # JWT + bcrypt
│   ├── db/
│   │   ├── base.py           # DeclarativeBase
│   │   └── session.py        # AsyncEngine + AsyncSession
│   ├── models/               # SQLAlchemy ORM models
│   ├── repositories/         # Capa de acceso a datos
│   ├── schemas/              # Pydantic schemas (request/response)
│   ├── services/             # Lógica de negocio
│   └── main.py               # App factory
├── alembic/                  # Migraciones
├── tests/
│   ├── integration/
│   └── conftest.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## Quickstart

### 1. Clonar y configurar entorno

```bash
git clone <repo>
cd ecommerce-api
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Variables de entorno

```bash
cp .env.example .env
# Edita .env con tus valores reales
```

Variables requeridas:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ecommerce_db
JWT_SECRET_KEY=tu-clave-secreta-muy-larga
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 3. Levantar PostgreSQL

```bash
docker-compose up db -d
```

### 4. Ejecutar migraciones

```bash
# Generar migración inicial desde los modelos
alembic revision --autogenerate -m "initial schema"

# Aplicar migraciones
alembic upgrade head
```

### 5. Correr el servidor

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`

---

## Documentación interactiva

| URL | Descripción |
|---|---|
| `http://localhost:8000/docs` | Swagger UI |
| `http://localhost:8000/redoc` | ReDoc |

---

## Endpoints principales

### Auth
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/auth/register` | Registro de usuario |
| POST | `/api/v1/auth/login` | Login → JWT |
| POST | `/api/v1/auth/refresh` | Renovar access token |

### Productos
| Método | Ruta | Auth |
|---|---|---|
| GET | `/api/v1/products` | Público |
| GET | `/api/v1/products/{id}` | Público |
| POST | `/api/v1/products` | Admin |
| PATCH | `/api/v1/products/{id}` | Admin |
| DELETE | `/api/v1/products/{id}` | Admin |

### Carrito
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/cart` | Ver carrito |
| POST | `/api/v1/cart/items` | Agregar producto |
| PATCH | `/api/v1/cart/items/{product_id}` | Actualizar cantidad |
| DELETE | `/api/v1/cart/items/{product_id}` | Eliminar item |
| DELETE | `/api/v1/cart` | Vaciar carrito |

### Órdenes
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/orders` | Crear orden desde el carrito |
| GET | `/api/v1/orders` | Mis órdenes |
| GET | `/api/v1/orders/{id}` | Detalle de orden |
| PATCH | `/api/v1/orders/{id}/status` | Cambiar estado (Admin) |

### Pagos
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/payments/checkout/{order_id}` | Crear PaymentIntent en Stripe |
| POST | `/api/v1/payments/webhook` | Webhook de Stripe |

---

## Flujo de compra completo

```
1. POST /auth/register        → crear cuenta
2. POST /auth/login           → obtener JWT
3. GET  /products             → buscar productos
4. POST /cart/items           → agregar al carrito
5. POST /orders               → crear orden (descuenta stock)
6. POST /payments/checkout/{order_id} → obtener client_secret de Stripe
7. [Frontend confirma el pago con Stripe.js]
8. Stripe envía webhook → orden pasa a PAID → carrito se vacía
```

---

## Correr tests

```bash
# Asegúrate de tener una DB de test corriendo
pytest tests/ -v
```

---

## Docker (todo en uno)

```bash
docker-compose up --build
```

---

## Roles

| Rol | Permisos |
|---|---|
| `customer` | Carrito, órdenes propias, perfil |
| `admin` | Todo lo anterior + gestión de productos, usuarios y órdenes |

Para crear el primer admin, actualiza el campo `role` directamente en la DB o agrega un script seed.
