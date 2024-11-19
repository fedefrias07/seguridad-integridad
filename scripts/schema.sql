CREATE DATABASE IF NOT EXISTS mydatabase;
USE mydatabase;
CREATE TABLE IF NOT EXISTS usuarios (
    email varchar(50) primary key,
    nombre varchar(100),
    apellido varchar(100),
    fechanac date
);