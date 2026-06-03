-- ══════════════════════════════════════════════════════════════════════════════
-- DATA CLEANING: Employee Records
-- ══════════════════════════════════════════════════════════════════════════════

-- ── Setup ─────────────────────────────────────────────────────────────────────

CREATE TABLE employees (
    employee_id   INT PRIMARY KEY,
    employee_name VARCHAR(50),
    salary        DECIMAL(10, 2),
    hire_date     VARCHAR(20),
    department    VARCHAR(50)
);

INSERT INTO employees (employee_id, employee_name, salary, hire_date, department) VALUES
(1,  'Amy West',    60000.00, '2021-01-15', 'HR'),
(2,  'Ivy Lee',     75000.50, '2020-05-22', 'Sales'),
(3,  'joe smith',   80000.75, '2019-08-10', 'Marketing'),
(4,  'John White',  90000.00, '2020-11-05', 'Finance'),
(5,  'Jane Hill',   55000.25, '2022-02-28', 'IT'),
(6,  'Dave West',   72000.00, '2020-03-12', 'Marketing'),
(7,  'Fanny Lee',   85000.50, '2018-06-25', 'Sales'),
(8,  'Amy Smith',   95000.25, '2019-11-30', 'Finance'),
(9,  'Ivy Hill',    62000.75, '2021-07-18', 'IT'),
(10, 'Joe White',   78000.00, '2022-04-05', 'Marketing'),
(11, 'John Lee',    68000.50, '2018-12-10', 'HR'),
(12, 'Jane West',   89000.25, '2017-09-15', 'Sales'),
(13, 'Dave Smith',  60000.75, '2022-01-08', NULL),
(14, 'Fanny White', 72000.00, '2019-04-22', 'IT'),
(15, 'Amy Hill',    84000.50, '2020-08-17', 'Marketing'),
(16, 'Ivy West',    92000.25, '2021-02-03', 'Finance'),
(17, 'Joe Lee',     58000.75, '2018-05-28', 'IT'),
(18, 'John Smith',  77000.00, '2019-10-10', 'HR'),
(19, 'Jane Hill',   81000.50, '2022-03-15', 'Sales'),
(20, 'Dave White',  70000.25, '2017-12-20', 'Marketing');

-- Verify initial load
SELECT * FROM employees;

-- ══════════════════════════════════════════════════════════════════════════════
-- STEP 1: Identify and Handle Missing Values
-- ══════════════════════════════════════════════════════════════════════════════

-- Find all rows with NULL or empty values in any column
SELECT *
FROM employees
WHERE employee_name IS NULL OR employee_name = ''
   OR salary        IS NULL
   OR hire_date     IS NULL OR hire_date     = ''
   OR department    IS NULL OR department    = '';

-- Result: employee_id=13 (Dave Smith) has NULL department

-- Option A: assign to 'Unknown' so the row is not lost
UPDATE employees
SET department = 'Unknown'
WHERE department IS NULL;

-- Option B (alternative): delete if a NULL department is unacceptable
-- DELETE FROM employees WHERE department IS NULL;

-- Verify fix
SELECT * FROM employees WHERE employee_id = 13;

-- ══════════════════════════════════════════════════════════════════════════════
-- STEP 2: Check for and Eliminate Duplicate Rows
-- ══════════════════════════════════════════════════════════════════════════════

-- Check for duplicate names + department combinations
-- (employee_id is PK so it is always unique — we check logical duplicates)
SELECT
    employee_name,
    department,
    COUNT(*) AS occurrences
FROM employees
GROUP BY employee_name, department
HAVING COUNT(*) > 1;

-- Result: 'Jane Hill' in Sales appears twice (ids 5 and 19 differ in dept,
-- but same name exists across different departments — not a true duplicate)
-- Let's check all Jane Hills specifically:
SELECT * FROM employees WHERE employee_name = 'Jane Hill';

-- They have different salaries, hire_dates and departments → NOT duplicates.
-- If true duplicates existed (all columns identical except PK), remove like so:
-- DELETE FROM employees
-- WHERE employee_id NOT IN (
--     SELECT MIN(employee_id)
--     FROM employees
--     GROUP BY employee_name, salary, hire_date, department
-- );

-- Confirm no fully duplicate rows exist
SELECT
    employee_name, salary, hire_date, department,
    COUNT(*) AS cnt
FROM employees
GROUP BY employee_name, salary, hire_date, department
HAVING COUNT(*) > 1;

-- ══════════════════════════════════════════════════════════════════════════════
-- STEP 3: Fix Structural Issues — Naming Conventions and Formatting
-- ══════════════════════════════════════════════════════════════════════════════

-- Check for names that are not in Title Case
SELECT employee_id, employee_name
FROM employees
WHERE employee_name != (
    -- SQLite: manual title case check — first letter upper, rest lower
    UPPER(SUBSTR(employee_name, 1, 1)) ||
    LOWER(SUBSTR(employee_name, 2))
);

-- Result: employee_id=3 'joe smith' should be 'Joe Smith'

-- Fix: apply proper Title Case to all names
-- SQLite does not have a native INITCAP, so we handle first + last name
UPDATE employees
SET employee_name =
    UPPER(SUBSTR(TRIM(employee_name), 1, 1)) ||
    LOWER(SUBSTR(TRIM(employee_name), 2,
        INSTR(TRIM(employee_name), ' ') - 2
    )) || ' ' ||
    UPPER(SUBSTR(TRIM(employee_name),
        INSTR(TRIM(employee_name), ' ') + 1, 1
    )) ||
    LOWER(SUBSTR(TRIM(employee_name),
        INSTR(TRIM(employee_name), ' ') + 2
    ))
WHERE employee_name != UPPER(SUBSTR(employee_name,1,1)) || SUBSTR(employee_name,2);

-- Verify
SELECT employee_id, employee_name FROM employees ORDER BY employee_id;

-- Trim all text columns of any accidental whitespace
UPDATE employees
SET
    employee_name = TRIM(employee_name),
    hire_date     = TRIM(hire_date),
    department    = TRIM(department);

-- Standardise department capitalisation (Title Case)
UPDATE employees
SET department =
    UPPER(SUBSTR(department, 1, 1)) ||
    LOWER(SUBSTR(department, 2));

-- Verify departments are consistent
SELECT DISTINCT department FROM employees ORDER BY department;

-- ══════════════════════════════════════════════════════════════════════════════
-- STEP 4: Ensure Correct Data Types — Convert hire_date from VARCHAR to DATE
-- ══════════════════════════════════════════════════════════════════════════════

-- Check current hire_date values and format
SELECT employee_id, hire_date FROM employees;

-- Validate all dates are in YYYY-MM-DD format (SQLite stores as text)
SELECT employee_id, hire_date
FROM employees
WHERE hire_date NOT LIKE '____-__-__'
   OR DATE(hire_date) IS NULL;

-- All dates are valid ISO format — add a proper DATE column
ALTER TABLE employees ADD COLUMN hire_date_clean DATE;

UPDATE employees
SET hire_date_clean = DATE(hire_date);

-- Verify conversion
SELECT employee_id, hire_date, hire_date_clean FROM employees;

-- Confirm no conversion failures
SELECT COUNT(*) AS failed_conversions
FROM employees
WHERE hire_date_clean IS NULL;

-- ══════════════════════════════════════════════════════════════════════════════
-- STEP 5: Detect and Address Salary Outliers
-- ══════════════════════════════════════════════════════════════════════════════

-- Calculate salary statistics
SELECT
    ROUND(AVG(salary), 2)                          AS mean_salary,
    MIN(salary)                                    AS min_salary,
    MAX(salary)                                    AS max_salary,
    ROUND(AVG(salary) - 2 * (
        SELECT ROUND(
            SQRT(AVG((salary - sub.avg_sal) * (salary - sub.avg_sal))), 2)
        FROM employees,
             (SELECT AVG(salary) AS avg_sal FROM employees) sub
    ), 2)                                          AS lower_bound_2sd,
    ROUND(AVG(salary) + 2 * (
        SELECT ROUND(
            SQRT(AVG((salary - sub.avg_sal) * (salary - sub.avg_sal))), 2)
        FROM employees,
             (SELECT AVG(salary) AS avg_sal FROM employees) sub
    ), 2)                                          AS upper_bound_2sd
FROM employees;

-- Flag potential outliers (beyond 2 standard deviations)
WITH stats AS (
    SELECT
        AVG(salary)  AS mean_sal,
        SQRT(AVG((salary - AVG(salary)) * (salary - AVG(salary))))
                     AS std_sal
    FROM employees
)
SELECT
    e.employee_id,
    e.employee_name,
    e.salary,
    ROUND(stats.mean_sal, 2) AS mean_salary,
    ROUND(stats.std_sal,  2) AS std_dev,
    CASE
        WHEN e.salary > stats.mean_sal + 2 * stats.std_sal THEN 'High outlier'
        WHEN e.salary < stats.mean_sal - 2 * stats.std_sal THEN 'Low outlier'
        ELSE 'Normal'
    END AS outlier_flag
FROM employees e, stats
ORDER BY e.salary DESC;

-- Result: no extreme outliers in this dataset (all within 2 SDs)
-- If outliers existed, options would be:
--   a) Cap to boundary: UPDATE employees SET salary = <upper_bound> WHERE salary > <upper_bound>
--   b) Remove:          DELETE FROM employees WHERE salary > <upper_bound>
--   c) Investigate:     flag for manual review

-- ══════════════════════════════════════════════════════════════════════════════
-- STEP 6: Standardise and Normalise Data
-- ══════════════════════════════════════════════════════════════════════════════

-- 6a: Add a normalised salary column (Min-Max normalisation: 0 to 1)
ALTER TABLE employees ADD COLUMN salary_normalised REAL;

UPDATE employees
SET salary_normalised = ROUND(
    (salary - (SELECT MIN(salary) FROM employees)) * 1.0
    / ((SELECT MAX(salary) FROM employees) - (SELECT MIN(salary) FROM employees))
, 4);

-- 6b: Add a salary band / tier column for categorical grouping
ALTER TABLE employees ADD COLUMN salary_band VARCHAR(10);

UPDATE employees
SET salary_band =
    CASE
        WHEN salary <  65000 THEN 'Low'
        WHEN salary <  80000 THEN 'Mid'
        WHEN salary <  90000 THEN 'High'
        ELSE                      'Senior'
    END;

-- 6c: Add tenure in years based on hire_date (relative to 2024-01-01)
ALTER TABLE employees ADD COLUMN tenure_years INT;

UPDATE employees
SET tenure_years = (
    CAST(
        (JULIANDAY('2024-01-01') - JULIANDAY(hire_date_clean)) / 365.25
    AS INT)
);

-- ══════════════════════════════════════════════════════════════════════════════
-- FINAL: View the fully cleaned and transformed dataset
-- ══════════════════════════════════════════════════════════════════════════════

SELECT
    employee_id,
    employee_name,
    department,
    salary,
    salary_normalised,
    salary_band,
    hire_date_clean   AS hire_date,
    tenure_years
FROM employees
ORDER BY employee_id;

-- Summary statistics on the clean dataset
SELECT
    department,
    COUNT(*)                        AS headcount,
    ROUND(AVG(salary), 2)           AS avg_salary,
    ROUND(MIN(salary), 2)           AS min_salary,
    ROUND(MAX(salary), 2)           AS max_salary,
    ROUND(AVG(tenure_years), 1)     AS avg_tenure_years
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;
