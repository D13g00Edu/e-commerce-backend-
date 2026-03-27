const { PrismaClient } = require('@prisma/client');
const { PrismaPg } = require('@prisma/adapter-pg');
require('dotenv').config();

const connectionString = process.env.DATABASE_URL;

if (!connectionString) {
  throw new Error('DATABASE_URL no está definida en el archivo .env');
}

const adapter = new PrismaPg({ connectionString });
const prisma = new PrismaClient({ adapter });

module.exports = prisma;