-- Pilna SQL schema, skirta rankiniam importavimui ar automatinėms migracijoms
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
