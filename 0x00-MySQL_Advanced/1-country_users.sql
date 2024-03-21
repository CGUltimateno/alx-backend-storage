-- a SQL script that creates a table users
-- with the following columns:
-- id INT PRIMARY KEY
-- name VARCHAR(255)
-- email VARCHAR(255)
-- country enum('USA', 'CAN', 'MEX')
CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255) NOT NULL UNIQUE,
   country CHAR(2) NOT NULL DEFAULT 'US',
    CHECK (country IN ('US', 'CO', 'TN'))
);
