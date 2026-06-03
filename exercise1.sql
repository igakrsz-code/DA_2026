-- ══════════════════════════════════════════════════════════════════════════════
-- Exercise 1: Items and Customers
-- ══════════════════════════════════════════════════════════════════════════════

-- 1. Create database
CREATE DATABASE IF NOT EXISTS public;
USE public;

-- ══════════════════════════════════════════════════════════════════════════════
-- 2. Create Tables
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS items (
    id    INT          PRIMARY KEY,
    name  VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS customers (
    id         INT          PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL
);

-- ══════════════════════════════════════════════════════════════════════════════
-- 3. Insert Data
-- ══════════════════════════════════════════════════════════════════════════════

-- Items
INSERT INTO items (id, name, price) VALUES
    (1, 'Small Desk', 100),
    (2, 'Large Desk', 300),
    (3, 'Fan',         80);

-- Customers
INSERT INTO customers (id, first_name, last_name) VALUES
    (1, 'Greg',    'Jones'),
    (2, 'Sandra',  'Jones'),
    (3, 'Scott',   'Scott'),
    (4, 'Trevor',  'Green'),
    (5, 'Melanie', 'Johnson');

-- ══════════════════════════════════════════════════════════════════════════════
-- 4. Queries
-- ══════════════════════════════════════════════════════════════════════════════

-- 4.1 All items
SELECT * FROM items;

-- 4.2 Items with price ABOVE 80 (not included)
SELECT * FROM items
WHERE price > 80;

-- 4.3 Items with price BELOW 300 (300 included)
SELECT * FROM items
WHERE price <= 300;

-- 4.4 Customers whose last name is 'Smith'
-- Expected outcome: 0 rows — no customer named Smith exists in the table.
SELECT * FROM customers
WHERE last_name = 'Smith';

-- 4.5 Customers whose last name is 'Jones'
SELECT * FROM customers
WHERE last_name = 'Jones';

-- 4.6 Customers whose first name is NOT 'Scott'
SELECT * FROM customers
WHERE first_name != 'Scott';
