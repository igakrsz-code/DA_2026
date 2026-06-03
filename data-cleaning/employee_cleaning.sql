-- ══════════════════════════════════════════════════════════════════════════════
-- DATA CLEANING & TRANSFORMATION — Exercises 1-5
-- ══════════════════════════════════════════════════════════════════════════════

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 1: Building a Comprehensive Dataset
-- ══════════════════════════════════════════════════════════════════════════════

-- Step 1: Create temp table joining all 4 source tables
CREATE TEMPORARY TABLE IF NOT EXISTS emp_dataset AS
SELECT
    e.employee_id,
    e.employee_name,
    e.gender,
    e.age,
    e.function_id,
    s.date,
    s.salary,
    f.function_group,
    c.company_name,
    c.company_city,
    c.company_state,
    c.company_type,
    c.const_site_category
FROM employees  e
LEFT JOIN salaries  s ON s.employee_id = e.employee_id
LEFT JOIN functions f ON f.function_id = e.function_id
LEFT JOIN company   c ON c.company_id  = e.company_id;

-- Verify the join
SELECT * FROM emp_dataset LIMIT 10;

-- Step 2-4: Create final df_employee table with unique id and DATE conversion
CREATE TABLE df_employee AS
SELECT
    employee_id || '_' || CAST(date AS TEXT)  AS id,
    DATE(date)                                AS month_year,
    employee_id,
    employee_name,
    `gender`                                  AS gender,
    age,
    salary,
    function_group,
    company_name,
    company_city,
    company_state,
    company_type,
    const_site_category
FROM emp_dataset;

-- Verify df_employee
SELECT * FROM df_employee LIMIT 10;
SELECT COUNT(*) AS total_rows FROM df_employee;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2: Data Cleaning
-- ══════════════════════════════════════════════════════════════════════════════

-- Step 1: Observe the table
SELECT * FROM df_employee;

-- Step 2: Remove unwanted spaces from all text columns using TRIM
UPDATE df_employee
SET
    id                 = TRIM(id),
    month_year         = TRIM(month_year),
    employee_id        = TRIM(employee_id),
    employee_name      = TRIM(employee_name),
    gender             = TRIM(gender),
    age                = TRIM(CAST(age AS TEXT)),
    salary             = TRIM(CAST(salary AS TEXT)),
    function_group     = TRIM(function_group),
    company_name       = TRIM(company_name),
    company_city       = TRIM(company_city),
    company_state      = TRIM(company_state),
    company_type       = TRIM(company_type),
    const_site_category = TRIM(const_site_category);

-- Step 3: Check for NULL and empty values
SELECT *
FROM df_employee
WHERE id                  IS NULL OR id                  = ''
   OR month_year          IS NULL OR month_year          = ''
   OR employee_id         IS NULL OR employee_id         = ''
   OR employee_name       IS NULL OR employee_name       = ''
   OR gender              IS NULL OR gender              = ''
   OR age                 IS NULL OR age                 = ''
   OR salary              IS NULL OR salary              = ''
   OR function_group      IS NULL OR function_group      = ''
   OR company_name        IS NULL OR company_name        = ''
   OR company_city        IS NULL OR company_city        = ''
   OR company_state       IS NULL OR company_state       = ''
   OR company_type        IS NULL OR company_type        = ''
   OR const_site_category IS NULL OR const_site_category = '';

-- Step 4: Delete rows with missing/empty salary (most critical field)
DELETE FROM df_employee
WHERE salary IS NULL
   OR salary = ''
   OR salary = ' ';

-- Also delete rows missing other critical fields
DELETE FROM df_employee
WHERE employee_id   IS NULL OR employee_id   = ''
   OR employee_name IS NULL OR employee_name = ''
   OR month_year    IS NULL OR month_year    = '';

-- Verify clean row count
SELECT COUNT(*) AS clean_rows FROM df_employee;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 3: Current Employee Counts by Company
-- How many employees do the companies have today? Grouped by company
-- ══════════════════════════════════════════════════════════════════════════════

SELECT
    company_name,
    COUNT(DISTINCT employee_id)   AS current_employee_count
FROM df_employee
WHERE month_year = (
    -- most recent date in the dataset = "today"
    SELECT MAX(month_year)
    FROM df_employee
)
GROUP BY company_name
ORDER BY current_employee_count DESC;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 4: Employee Distribution by City and Over Time
-- ══════════════════════════════════════════════════════════════════════════════

-- 4a: Total employees per city + percentage column
SELECT
    company_city,
    COUNT(DISTINCT employee_id)                           AS total_employees,
    ROUND(
        COUNT(DISTINCT employee_id) * 100.0
        / (SELECT COUNT(DISTINCT employee_id) FROM df_employee)
    , 2)                                                  AS percentage
FROM df_employee
GROUP BY company_city
ORDER BY total_employees DESC;

-- 4b: Total number of employees each month
SELECT
    month_year,
    COUNT(DISTINCT employee_id)   AS total_employees
FROM df_employee
GROUP BY month_year
ORDER BY month_year;

-- 4c: Average number of employees each month (across all months)
SELECT
    ROUND(AVG(monthly_count), 2) AS avg_employees_per_month
FROM (
    SELECT
        month_year,
        COUNT(DISTINCT employee_id) AS monthly_count
    FROM df_employee
    GROUP BY month_year
) monthly_totals;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 5: Employment Trends and Salary Metrics
-- ══════════════════════════════════════════════════════════════════════════════

-- 5a: Minimum and maximum employee counts + which months they occurred
WITH monthly_counts AS (
    SELECT
        month_year,
        COUNT(DISTINCT employee_id) AS employee_count
    FROM df_employee
    GROUP BY month_year
)
SELECT
    'Maximum' AS metric,
    month_year,
    employee_count
FROM monthly_counts
WHERE employee_count = (SELECT MAX(employee_count) FROM monthly_counts)

UNION ALL

SELECT
    'Minimum' AS metric,
    month_year,
    employee_count
FROM monthly_counts
WHERE employee_count = (SELECT MIN(employee_count) FROM monthly_counts)

ORDER BY metric;

-- 5b: Monthly average number of employees by function group
SELECT
    function_group,
    month_year,
    COUNT(DISTINCT employee_id)                    AS employee_count,
    ROUND(
        AVG(COUNT(DISTINCT employee_id)) OVER (
            PARTITION BY function_group
            ORDER BY month_year
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        )
    , 2)                                           AS rolling_avg_employees
FROM df_employee
GROUP BY function_group, month_year
ORDER BY function_group, month_year;

-- Simpler: average headcount per month per function group (overall)
SELECT
    function_group,
    ROUND(AVG(monthly_count), 2) AS avg_monthly_employees
FROM (
    SELECT
        function_group,
        month_year,
        COUNT(DISTINCT employee_id) AS monthly_count
    FROM df_employee
    GROUP BY function_group, month_year
) grouped
GROUP BY function_group
ORDER BY avg_monthly_employees DESC;

-- 5c: Annual average salary
SELECT
    STRFTIME('%Y', month_year)   AS year,
    ROUND(AVG(CAST(salary AS NUMERIC)), 2) AS avg_annual_salary
FROM df_employee
WHERE salary IS NOT NULL
  AND salary != ''
GROUP BY year
ORDER BY year;
