-- ══════════════════════════════════════════════════════════════════════════════
-- SQL Basics: Actors Table
-- ══════════════════════════════════════════════════════════════════════════════

-- ── Setup: create and populate the actors table ───────────────────────────────
CREATE TABLE IF NOT EXISTS actors (
    id         SERIAL       PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL,
    age        INT          NOT NULL,
    nationality VARCHAR(100) NOT NULL
);

INSERT INTO actors (first_name, last_name, age, nationality) VALUES
    ('Tom',        'Hanks',      67,  'American'),
    ('Meryl',      'Streep',     74,  'American'),
    ('Leonardo',   'DiCaprio',   49,  'American'),
    ('Cate',       'Blanchett',  54,  'Australian'),
    ('Denzel',     'Washington', 69,  'American'),
    ('Natalie',    'Portman',    42,  'Israeli-American'),
    ('Brad',       'Pitt',       60,  'American'),
    ('Scarlett',   'Johansson',  39,  'American'),
    ('Anthony',    'Hopkins',    86,  'British'),
    ('Viola',      'Davis',      58,  'American');

-- ══════════════════════════════════════════════════════════════════════════════
-- 1. Count how many actors are in the table
-- ══════════════════════════════════════════════════════════════════════════════

SELECT COUNT(*) AS total_actors
FROM actors;

-- Expected outcome: 10
-- COUNT(*) counts every row regardless of null values.
-- This is the safest way to count all records in a table.

-- ══════════════════════════════════════════════════════════════════════════════
-- 2. Try to add a new actor with blank (NULL) fields
-- ══════════════════════════════════════════════════════════════════════════════

-- Attempt A: Insert with NULL values in NOT NULL columns
-- Expected outcome: ERROR — violates NOT NULL constraint.
-- PostgreSQL will reject this insert entirely; no partial row is saved.
INSERT INTO actors (first_name, last_name, age, nationality)
VALUES (NULL, NULL, NULL, NULL);

-- Attempt B: Insert with empty strings instead of NULL
-- Expected outcome: SUCCESS — empty strings are valid VARCHAR values.
-- The row is inserted, but the data is meaningless/dirty.
-- This highlights why CHECK constraints or application-level validation matter.
INSERT INTO actors (first_name, last_name, age, nationality)
VALUES ('', '', 0, '');

-- Check the table after both attempts
SELECT * FROM actors;
SELECT COUNT(*) AS total_actors_after FROM actors;

-- ══════════════════════════════════════════════════════════════════════════════
-- Commentary
-- ══════════════════════════════════════════════════════════════════════════════

-- NULL insert (Attempt A):
--   PostgreSQL throws: "ERROR: null value in column violates not-null constraint"
--   The NOT NULL constraint is enforced at the database level,
--   acting as a safety net regardless of what the application sends.

-- Empty string insert (Attempt B):
--   Succeeds because '' is a valid string — NOT NULL only blocks true NULLs.
--   To block empty strings too, add a CHECK constraint:
--   CHECK (first_name <> '' AND last_name <> '' AND nationality <> '')

-- Clean up the blank row if Attempt B succeeded
DELETE FROM actors
WHERE first_name = '' AND last_name = '';
