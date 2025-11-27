-- create_sacis.sql
CREATE DATABASE IF NOT EXISTS sacis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sacis_db;

-- Tabla de usuarios (operadores / analistas)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('operador','analista','admin') DEFAULT 'operador',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de satélites
CREATE TABLE IF NOT EXISTS satellites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    status ENUM('operativo','en_mantenimiento','no_operativo') DEFAULT 'operativo',
    last_telemetry DATETIME NULL,
    orbit_params JSON NULL,
    available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de zonas de vigilancia
CREATE TABLE IF NOT EXISTS zones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    polygon_geo TEXT, -
    priority ENUM('CRITICO','ALTO','MEDIO','BAJO') DEFAULT 'MEDIO',
    restricted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de asignaciones (ordenes de vigilancia)
CREATE TABLE IF NOT EXISTS assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    satellite_id INT NOT NULL,
    zone_id INT NOT NULL,
    frequency_minutes INT DEFAULT 60,
    status ENUM('pendiente','en_curso','completada','cancelada') DEFAULT 'pendiente',
    assigned_by INT NULL, 
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (satellite_id) REFERENCES satellites(id) ON DELETE CASCADE,
    FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Tabla de logs / bitácora
CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_type VARCHAR(100),
    details TEXT,
    created_by INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);