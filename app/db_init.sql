CREATE DATABASE IF NOT EXISTS db_meli_challenge;

USE db_meli_challenge;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS database_persistence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    host VARCHAR(255),
    port VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255),
    date_add TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_user INT NOT NULL,
    FOREIGN KEY (id_user) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS excluded_database (
    id INT AUTO_INCREMENT PRIMARY KEY,
    database_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS information_classification (
    id INT AUTO_INCREMENT PRIMARY KEY,
    information_type VARCHAR(255) NOT NULL,
    information_expression TEXT NOT NULL,
    id_user INT NULL,
    FOREIGN KEY (id_user) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS historic_scan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_scan DATETIME NOT NULL,
    classification LONGTEXT NOT NULL,
    id_database INT NOT NULL,
    deleted INT NULL,
    id_user INT NOT NULL,
    FOREIGN KEY (id_user) REFERENCES user(id) ON DELETE CASCADE
);

CREATE DATABASE IF NOT EXISTS db_school_meli;

USE db_school_meli;

CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Addresses (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    street_address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS CreditCards (
    credit_card_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    credit_card_number VARCHAR(20) NOT NULL UNIQUE,
    credit_card_holder_name VARCHAR(100) NOT NULL,
    expiration_date DATE NOT NULL,
    card_type VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS UserProfiles (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date_of_birth DATE,
    phone_number VARCHAR(20),
    gender ENUM('Male', 'Female', 'Other') DEFAULT 'Other',
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

USE db_meli_challenge;

INSERT IGNORE INTO excluded_database (database_name)
VALUES 
('information_schema'),
('mysql'),
('performance_schema'),
('sys');

INSERT IGNORE INTO user (username, password) VALUES 
('root', 'gAAAAABnOrR8gBbolTP3jlbhHDH7eF5Q5CmX8BFMKHa8-pRSF2ZBmulnFiwdcFwxVIWTa1s5NszD7SUsF_8P1_U7VzLnF5R_Ew==');

INSERT IGNORE INTO information_classification (information_type, information_expression, id_user) VALUES
('username', 'USERNAME', 1),
('mail', 'EMAIL_ADDRESS', 1),
('address', 'ADDRESS_UBICATION', 1),
('credit', 'CREDIT_CARD_NUMBER', 1),
('date', 'DATE_INFORMATION', 1),
('phone', 'PHONE_INFORMATION', 1),
('pass', 'PASSWORD_INFORMATION', 1);