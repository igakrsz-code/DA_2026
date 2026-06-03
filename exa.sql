-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 1: Items and Customers (public database)
-- ══════════════════════════════════════════════════════════════════════════════

-- 1. All items ordered by price (lowest to highest)
SELECT *
FROM items
ORDER BY price ASC;

-- 2. Items with price >= 80, ordered by price (highest to lowest)
SELECT *
FROM items
WHERE price >= 80
ORDER BY price DESC;

-- 3. First 3 customers alphabetically by first name (no primary key column)
SELECT first_name, last_name
FROM customers
ORDER BY first_name ASC
LIMIT 3;

-- 4. All last names only, in reverse alphabetical order (Z-A)
SELECT last_name
FROM customers
ORDER BY last_name DESC;
