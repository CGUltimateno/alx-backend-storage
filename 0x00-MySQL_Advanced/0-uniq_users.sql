-- a SQL script that creates a table users
-- with the following columns:
-- id INT PRIMARY KEY
-- name VARCHAR(255)
-- email VARCHAR(255)
CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  email VARCHAR(255)
);