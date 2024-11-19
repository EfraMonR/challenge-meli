
# Challenge Mercado Libre

## Description

This is a challenge for the opportunity to enter Mercado Libre. The goal of this project is to showcase skills and creativity in solving specific problems related to database management and data classification.

## Requirements

Before running the application, make sure you have the following installed:

- Python 3.10+
- Docker
- Docker Compose
- MySQL Server

## Clone the Repository

To clone the repository, run:

```bash
git clone https://github.com/EfraMonR/challenge-meli.git
```
## Create `.env` File

Create a `.env` file in the root directory of the project with the following content:

```plaintext
MYSQL_HOST = db
MYSQL_USER = root
MYSQL_PORT = 3306
MYSQL_PASSWORD = rootpassword1
MYSQL_DATABASE = db_meli_challenge
FERNET_KEY = fn1bLd5uFKQtncmdB_oNtvXpStmbkfkcRMhkaw1N1Bc=
SECRET_KEY=mysecretkeysupersecure
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Initialize with Docker

To set up the application using Docker, follow these steps:

1. **Create the Docker image:**

   Run the following command to build the Docker image:

   ```bash
   docker-compose build
   ```

2. **Start the service:**

   Run the following command to start the Docker container in the background:

   ```bash
   docker compose up -d
   ```

   Once the Docker service is up, the required databases will be automatically created.

## Alternative Setup (Without Docker)

If you don't have Docker, you can download the repository and manually set up the environment.

1. **Install dependencies:**

   After downloading the repository, navigate to the project folder and install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

2. **Create the MySQL database:**

   Use the following SQL script to set up the database in MySQL:

   ```sql
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
   ```

## Run the Application

Once you have completed the setup (whether using Docker or the manual process), you can run the application with the following Python command:

```bash
uvicorn app.main:app --reload
```

This will start the server and the application will be available for testing.

## Documentation

For more information about how the application works and to learn about the API functionality, please refer to the official documentation.
