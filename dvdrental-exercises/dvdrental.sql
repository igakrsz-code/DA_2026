
-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 1: DVD Rental
-- ══════════════════════════════════════════════════════════════════════════════

-- 1. All languages from the language table
SELECT *
FROM language;

-- 2. All films joined with their language (INNER JOIN)
--    Only films that have a matching language
SELECT f.title,
       f.description,
       l.name AS language_name
FROM film f
JOIN language l ON f.language_id = l.language_id;

-- 3. All languages even if no films exist in that language (LEFT JOIN from language)
SELECT f.title,
       f.description,
       l.name AS language_name
FROM language l
LEFT JOIN film f ON l.language_id = f.language_id;

-- 4. Create new_film table and insert some films
CREATE TABLE IF NOT EXISTS new_film (
    id   SERIAL       PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO new_film (name) VALUES
    ('Inception'),
    ('Interstellar'),
    ('The Dark Knight'),
    ('Parasite'),
    ('Dune');

SELECT * FROM new_film;

-- 5. Create customer_review table
--    ON DELETE CASCADE: deleting a film auto-deletes its reviews
CREATE TABLE IF NOT EXISTS customer_review (
    review_id   SERIAL       PRIMARY KEY NOT NULL,
    film_id     INT          NOT NULL REFERENCES new_film(id) ON DELETE CASCADE,
    language_id INT          NOT NULL REFERENCES language(language_id),
    title       VARCHAR(255) NOT NULL,
    score       INT          NOT NULL CHECK (score BETWEEN 1 AND 10),
    review_text TEXT,
    last_update TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- 6. Add 2 movie reviews (linked to valid new_film and language rows)
INSERT INTO customer_review (film_id, language_id, title, score, review_text, last_update)
VALUES
    (1, 1, 'Mind-blowing experience',    9,  'Inception is a masterpiece of layered storytelling.', NOW()),
    (2, 1, 'Visually stunning sci-fi',   10, 'Interstellar left me speechless. Nolan at his best.',  NOW());

SELECT * FROM customer_review;

-- 7. Delete a film that has a review — observe CASCADE behaviour
DELETE FROM new_film
WHERE name = 'Inception';

-- Check customer_review: the review for Inception should be automatically deleted
SELECT * FROM customer_review;
-- RESULT: The review with film_id=1 (Inception) is gone automatically.
-- ON DELETE CASCADE removed it the moment the parent row in new_film was deleted.
-- The review for Interstellar remains untouched.

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2: DVD Rental
-- ══════════════════════════════════════════════════════════════════════════════

-- 1. UPDATE language of some films (must use valid language_id values)
--    language table typically has: 1=English, 2=Italian, 3=Japanese,
--    4=Mandarin, 5=French, 6=German
UPDATE film
SET language_id = 3          -- Japanese
WHERE film_id IN (1, 2, 3);

-- Verify
SELECT film_id, title, language_id
FROM film
WHERE film_id IN (1, 2, 3);

-- Reset back to English
UPDATE film
SET language_id = 1
WHERE film_id IN (1, 2, 3);

-- 2. Foreign keys defined on the customer table
--    Query the information schema to find all FK constraints
SELECT
    tc.constraint_name,
    tc.table_name,
    kcu.column_name,
    ccu.table_name  AS referenced_table,
    ccu.column_name AS referenced_column
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage  AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_name = 'customer';

-- RESULT: customer references:
--   store(store_id)   — must INSERT with a valid store_id
--   address(address_id) — must INSERT with a valid address_id
-- This means when INSERTing a new customer you MUST supply
-- a store_id and address_id that already exist in those tables,
-- otherwise PostgreSQL will throw a foreign key violation error.

-- 3. Drop the customer_review table
--    This is EASY because no other table references customer_review.
--    If other tables had FK references TO it, we would need to drop those first
--    or use CASCADE.
DROP TABLE IF EXISTS customer_review;
-- Straightforward — no dependent objects, no extra checking needed.

-- 4. Rentals still outstanding (not yet returned)
SELECT COUNT(*) AS outstanding_rentals
FROM rental
WHERE return_date IS NULL;

-- 5. Top 30 most expensive outstanding movies (by replacement_cost)
SELECT f.film_id,
       f.title,
       f.rental_rate,
       f.replacement_cost,
       r.rental_date
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film     f ON i.film_id       = f.film_id
WHERE r.return_date IS NULL
ORDER BY f.replacement_cost DESC
LIMIT 30;

-- 6. Help your friend find 4 movies
-- ─────────────────────────────────────────────────────────────────────────────

-- 6.1 Film about a sumo wrestler starring Penelope Monroe
SELECT f.film_id,
       f.title,
       f.description
FROM film f
JOIN film_actor fa ON f.film_id    = fa.film_id
JOIN actor      a  ON fa.actor_id  = a.actor_id
WHERE (f.description ILIKE '%sumo%')
  AND (a.first_name ILIKE 'Penelope'
   AND a.last_name  ILIKE 'Monroe');

-- 6.2 Short documentary under 60 minutes, rated R
SELECT film_id,
       title,
       description,
       length,
       rating
FROM film
WHERE length  < 60
  AND rating  = 'R'
  AND (description ILIKE '%documentary%'
    OR special_features ILIKE '%documentary%');

-- 6.3 Film rented by Matthew Mahan, paid over $4.00,
--     returned between 28 July and 1 August 2005
SELECT DISTINCT f.film_id,
                f.title,
                f.description,
                p.amount        AS payment_amount,
                r.return_date
FROM customer  c
JOIN rental    r  ON c.customer_id  = r.customer_id
JOIN payment   p  ON r.rental_id    = p.rental_id
JOIN inventory i  ON r.inventory_id = i.inventory_id
JOIN film      f  ON i.film_id      = f.film_id
WHERE c.first_name ILIKE 'Matthew'
  AND c.last_name  ILIKE 'Mahan'
  AND p.amount      > 4.00
  AND r.return_date BETWEEN '2005-07-28' AND '2005-08-01';

-- 6.4 Film Matthew Mahan watched with "boat" in title/description,
--     very expensive replacement cost
SELECT DISTINCT f.film_id,
                f.title,
                f.description,
                f.replacement_cost
FROM customer  c
JOIN rental    r  ON c.customer_id  = r.customer_id
JOIN inventory i  ON r.inventory_id = i.inventory_id
JOIN film      f  ON i.film_id      = f.film_id
WHERE c.first_name ILIKE 'Matthew'
  AND c.last_name  ILIKE 'Mahan'
  AND (f.title       ILIKE '%boat%'
    OR f.description ILIKE '%boat%')
ORDER BY f.replacement_cost DESC
LIMIT 5;
