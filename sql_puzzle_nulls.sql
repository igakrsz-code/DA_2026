-- ══════════════════════════════════════════════════════════════════════════════
-- SQL PUZZLE: Table Relationships & NULL Behaviour
-- ══════════════════════════════════════════════════════════════════════════════

-- ── Setup ─────────────────────────────────────────────────────────────────────

CREATE TABLE FirstTab (
    id   INTEGER,
    name VARCHAR(10)
);

INSERT INTO FirstTab VALUES
    (5,    'Pawan'),
    (6,    'Sharlee'),
    (7,    'Krish'),
    (NULL, 'Avtaar');

SELECT * FROM FirstTab;
-- ID   | Name
-- 5    | Pawan
-- 6    | Sharlee
-- 7    | Krish
-- NULL | Avtaar

CREATE TABLE SecondTab (
    id INTEGER
);

INSERT INTO SecondTab VALUES
    (5),
    (NULL);

SELECT * FROM SecondTab;
-- ID
-- 5
-- NULL

-- ══════════════════════════════════════════════════════════════════════════════
-- Q1.
-- Subquery: SELECT id FROM SecondTab WHERE id IS NULL → returns { NULL }
-- NOT IN (NULL) → every comparison with NULL yields UNKNOWN, not TRUE/FALSE
-- SQL treats UNKNOWN as "not matching" → 0 rows pass the filter
--
-- MY PREDICTION: 0
-- ══════════════════════════════════════════════════════════════════════════════

SELECT COUNT(*)
FROM FirstTab AS ft
WHERE ft.id NOT IN (
    SELECT id FROM SecondTab WHERE id IS NULL
);

-- ACTUAL OUTPUT: 0
-- EXPLANATION:
--   The subquery returns a single NULL value.
--   NOT IN (NULL) forces every row comparison to evaluate as UNKNOWN.
--   In SQL, UNKNOWN is never TRUE, so no rows satisfy the WHERE clause.
--   Result: 0

-- ══════════════════════════════════════════════════════════════════════════════
-- Q2.
-- Subquery: SELECT id FROM SecondTab WHERE id = 5 → returns { 5 }
-- NOT IN (5) checks each FirstTab row:
--   id=5    → 5 NOT IN (5) → FALSE  → excluded
--   id=6    → 6 NOT IN (5) → TRUE   → included
--   id=7    → 7 NOT IN (5) → TRUE   → included
--   id=NULL → NULL NOT IN (5) → UNKNOWN → excluded
--
-- MY PREDICTION: 2
-- ══════════════════════════════════════════════════════════════════════════════

SELECT COUNT(*)
FROM FirstTab AS ft
WHERE ft.id NOT IN (
    SELECT id FROM SecondTab WHERE id = 5
);

-- ACTUAL OUTPUT: 2
-- EXPLANATION:
--   Subquery returns only {5}.
--   Rows with id=6 and id=7 pass (NOT IN 5 = TRUE).
--   id=5 is excluded (IN the list).
--   id=NULL evaluates as UNKNOWN → excluded.
--   Result: 2 (Sharlee, Krish)

-- ══════════════════════════════════════════════════════════════════════════════
-- Q3.
-- Subquery: SELECT id FROM SecondTab → returns { 5, NULL }
-- NOT IN (5, NULL):
--   id=5    → 5 NOT IN (5, NULL)    → FALSE   → excluded
--   id=6    → 6 NOT IN (5, NULL)    → UNKNOWN (because of NULL) → excluded
--   id=7    → 7 NOT IN (5, NULL)    → UNKNOWN (because of NULL) → excluded
--   id=NULL → NULL NOT IN (5, NULL) → UNKNOWN → excluded
--
-- MY PREDICTION: 0
-- ══════════════════════════════════════════════════════════════════════════════

SELECT COUNT(*)
FROM FirstTab AS ft
WHERE ft.id NOT IN (
    SELECT id FROM SecondTab
);

-- ACTUAL OUTPUT: 0
-- EXPLANATION:
--   This is the classic NULL trap in NOT IN.
--   Whenever a subquery contains even one NULL, NOT IN returns UNKNOWN
--   for every row that doesn't match an explicit value — because SQL cannot
--   confirm "x is definitely not equal to NULL".
--   All 4 rows are excluded → Result: 0
--   ⚠️ This is why NOT EXISTS is safer than NOT IN when NULLs may be present.

-- ══════════════════════════════════════════════════════════════════════════════
-- Q4.
-- Subquery: SELECT id FROM SecondTab WHERE id IS NOT NULL → returns { 5 }
-- NOT IN (5):
--   id=5    → FALSE   → excluded
--   id=6    → TRUE    → included
--   id=7    → TRUE    → included
--   id=NULL → UNKNOWN → excluded
--
-- MY PREDICTION: 2
-- ══════════════════════════════════════════════════════════════════════════════

SELECT COUNT(*)
FROM FirstTab AS ft
WHERE ft.id NOT IN (
    SELECT id FROM SecondTab WHERE id IS NOT NULL
);

-- ACTUAL OUTPUT: 2
-- EXPLANATION:
--   Filtering NULLs out of the subquery with IS NOT NULL leaves only {5}.
--   Now NOT IN behaves predictably — no NULL poison in the list.
--   id=6 and id=7 pass. id=5 excluded. id=NULL still UNKNOWN → excluded.
--   Result: 2 (Sharlee, Krish)

-- ══════════════════════════════════════════════════════════════════════════════
-- SUMMARY TABLE
-- ══════════════════════════════════════════════════════════════════════════════

-- Q  | Subquery returns | Predicted | Actual | Key lesson
-- ───┼──────────────────┼───────────┼────────┼──────────────────────────────
-- Q1 | { NULL }         |     0     |   0    | NOT IN (NULL) → always UNKNOWN
-- Q2 | { 5 }            |     2     |   2    | NOT IN clean list works fine
-- Q3 | { 5, NULL }      |     0     |   0    | One NULL poisons the whole IN
-- Q4 | { 5 }            |     2     |   2    | Filter NULLs out → safe NOT IN

-- ══════════════════════════════════════════════════════════════════════════════
-- BEST PRACTICE: use NOT EXISTS instead of NOT IN when NULLs may exist
-- ══════════════════════════════════════════════════════════════════════════════

-- Safe equivalent of Q3 using NOT EXISTS (returns correct 2 rows):
SELECT COUNT(*)
FROM FirstTab ft
WHERE NOT EXISTS (
    SELECT 1
    FROM SecondTab st
    WHERE st.id = ft.id
);
-- Returns 2 — NOT EXISTS handles NULLs correctly.

-- ── Cleanup ───────────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS FirstTab;
DROP TABLE IF EXISTS SecondTab;
