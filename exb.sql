-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2: dvdrental database
-- ══════════════════════════════════════════════════════════════════════════════

-- 1. All columns from the customer table
SELECT *
FROM customer;

-- 2. First and last name as alias "full_name"
SELECT first_name || ' ' || last_name AS full_name
FROM customer;

-- 3. All DISTINCT account creation dates
SELECT DISTINCT create_date
FROM customer;

-- 4. All customer details ordered by first name descending
SELECT *
FROM customer
ORDER BY first_name DESC;

-- 5. Film ID, title, description, release year, rental rate ordered by rental rate ASC
SELECT film_id, title, description, release_year, rental_rate
FROM film
ORDER BY rental_rate ASC;

-- 6. Address and phone of customers in Texas district
SELECT address, phone
FROM address
WHERE district = 'Texas';

-- 7. All movie details where film_id is 15 or 150
SELECT *
FROM film
WHERE film_id IN (15, 150);

-- 8. Search for favorite movie "Inception"
SELECT film_id, title, description, length, rental_rate
FROM film
WHERE title = 'Inception';

-- 9. Search by first two letters "In" if exact match not found
SELECT film_id, title, description, length, rental_rate
FROM film
WHERE title LIKE 'In%';

-- 10. The 10 cheapest movies
SELECT film_id, title, rental_rate
FROM film
ORDER BY rental_rate ASC
LIMIT 10;

-- 11. The next 10 cheapest movies (11-20) with OFFSET
SELECT film_id, title, rental_rate
FROM film
ORDER BY rental_rate ASC
LIMIT 10 OFFSET 10;

-- 11. Bonus: next 10 cheapest WITHOUT using LIMIT
SELECT film_id, title, rental_rate
FROM (
    SELECT film_id,
           title,
           rental_rate,
           ROW_NUMBER() OVER (ORDER BY rental_rate ASC) AS rn
    FROM film
) ranked
WHERE rn BETWEEN 11 AND 20;

-- 12. JOIN customer + payment: name, amount, date ordered by customer_id
SELECT c.first_name, c.last_name, p.amount, p.payment_date
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
ORDER BY c.customer_id ASC;

-- 13. Movies NOT in inventory
SELECT f.film_id, f.title
FROM film f
WHERE f.film_id NOT IN (
    SELECT DISTINCT film_id
    FROM inventory
);

-- 14. Which city is in which country
SELECT ci.city, co.country
FROM city ci
JOIN country co ON ci.country_id = co.country_id
ORDER BY co.country ASC, ci.city ASC;

-- 15. Bonus: customer id, names, payment amount and date ordered by staff_id
SELECT c.customer_id, c.first_name, c.last_name,
       p.amount, p.payment_date, p.staff_id
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
ORDER BY p.staff_id ASC, c.customer_id ASC;
