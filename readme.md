# 🛒 E-commerce API

## 📌 Descripción

Este proyecto consiste en el desarrollo de una API para una plataforma de comercio electrónico.  
El sistema permite gestionar usuarios, productos, carritos de compra y procesos de pago.

La solución fue desarrollada utilizando una combinación de **Node.js** y **Python**, aprovechando las fortalezas de cada tecnología en distintas partes del sistema.

---

## ⚙️ Tecnologías utilizadas

- **Node.js** → Backend principal de la API
- **Python** → Procesamiento auxiliar / servicios complementarios
- **JWT** → Autenticación de usuarios
- **Base de datos relacional** → Manejo de datos transaccionales
- **Pasarela de pagos (Stripe)** → Procesamiento de pagos

---

## 🚀 Funcionalidades principales

- Registro e inicio de sesión de usuarios
- Autenticación mediante JWT
- Gestión de productos (CRUD)
- Búsqueda y visualización de productos
- Carrito de compras
  - Agregar productos
  - Eliminar productos
  - Actualizar cantidades
- Proceso de checkout
- Integración con sistema de pagos
- Creación de órdenes

---

## 🧠 Arquitectura

El sistema sigue una arquitectura basada en servicios:

- **Node.js** se encarga de:
  - Exposición de endpoints
  - Lógica principal de negocio
  - Manejo de autenticación y autorización

- **Python** se utiliza para:
  - Procesamiento adicional
  - Posibles tareas de análisis o servicios auxiliares

- **Base de datos relacional**:
  - Manejo de entidades críticas como usuarios, órdenes y pagos

---

## 📦 Estado del proyecto

Se cuenta con una versión funcional (MVP) que incluye:

- Autenticación de usuarios
- Gestión de productos
- Carrito de compras
- Checkout básico
- Integración de pagos

---

## 📌 Notas

Este proyecto está diseñado con enfoque en escalabilidad, permitiendo integrar nuevos servicios o tecnologías según sea necesario.