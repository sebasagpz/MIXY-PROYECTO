CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    nacimiento DATE,
    password TEXT NOT NULL
);
