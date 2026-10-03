CREATE DATABASE ecommerce_demo;
USE ecommerce_demo;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(20) DEFAULT 'user'
);

CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10, 2)
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    article_name VARCHAR(100)
);

INSERT INTO articles (name, price) VALUES ('Livre OWASP', 15.00), ('T-Shirt Hacker', 25.00);
INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin');
