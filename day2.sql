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


-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2: dvdrental database
-- ══════════════════════════════════════════════════════════════════════════════

-- 1. All columns from the customer table
SELECT *
FROM customer;

-- 2. First and last name displayed as alias "full_name"
SELECT first_name || ' ' || last_name AS full_name
FROM customer;

-- 3. All DISTINCT account creation dates (no duplicates)
SELECT DISTINCT create_date
FROM customer;

-- 4. All customer details ordered by first name descending (Z-A)
SELECT *
FROM customer
ORDER BY first_name DESC;

-- 5. Film ID, title, description, release year, rental rate
--    ordered by rental rate ascending
SELECT film_id,
       title,
       description,
       release_year,
       rental_rate
FROM film
ORDER BY rental_rate ASC;

-- 6. Address and phone number of customers in the Texas district
SELECT address,
       phone
FROM address
WHERE district = 'Texas';

-- 7. All movie details where film_id is 15 or 150
SELECT *
FROM film
WHERE film_id IN (15, 150);

-- 8. Check if a favorite movie exists — searching for "Inception"
--    Get film_id, title, description, length, rental_rate
SELECT film_id,
       title,
       description,
       length,
       rental_rate
FROM film
WHERE title = 'Inception';

-- 9. No exact match? Search by first two letters of the title (e.g. "In")
SELECT film_id,
       title,
       description,
       length,
       rental_rate
FROM film
WHERE title LIKE 'In%';

-- 10. The 10 cheapest movies
SELECT film_id,
       title,
       rental_rate
FROM film
ORDER BY rental_rate ASC
LIMIT 10;

-- 11. The NEXT 10 cheapest movies (movies 11-20)
--     Method A: using OFFSET
SELECT film_id,
       title,
       rental_rate
FROM film
ORDER BY rental_rate ASC
LIMIT 10 OFFSET 10;

-- 11. Bonus: without using LIMIT
--     Uses a subquery to exclude the 10 cheapest and picks the next 10
SELECT film_id,
       title,
       rental_rate
FROM film
WHERE rental_rate > (
    SELECT MIN(rental_rate)
    FROM film
)
ORDER BY rental_rate ASC
FETCH FIRST 10 ROWS ONLY;

-- 12. JOIN customer and payment tables
--     Get first name, last name, payment amount and payment date
--     ordered by customer_id ascending
SELECT c.first_name,
       c.last_name,
       p.amount,
       p.payment_date
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
ORDER BY c.customer_id ASC;

-- 13. Movies NOT in inventory
SELECT f.film_id,
       f.title
FROM film f
WHERE f.film_id NOT IN (
    SELECT DISTINCT film_id
    FROM inventory
);

-- 14. Which city is in which country
SELECT ci.city,
       co.country
FROM city ci
JOIN country co ON ci.country_id = co.country_id
ORDER BY co.country ASC, ci.city ASC;

-- 15. BONUS: Customer id, names, payment amount and date
--     ordered by the staff member who made the sale
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       p.amount,
       p.payment_date,
       p.staff_id
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
ORDER BY p.staff_id ASC, c.customer_id ASC;
