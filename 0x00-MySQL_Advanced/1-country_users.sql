-- a SQL script that creates a table users
-- with the following columns:
-- id INT PRIMARY KEY
-- name VARCHAR(255)
-- email VARCHAR(255)
-- country enum('USA', 'CAN', 'MEX')
CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255) NOT NULL UNIQUE,
   country CHAR(2) NOT NULL DEFAULT 'US',
	CHECK (country = 'US' OR country = 'CO' OR country = 'TN')
);
