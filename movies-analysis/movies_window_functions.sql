-- ══════════════════════════════════════════════════════════════════════════════
-- MOVIES DATABASE — Window Functions & CTEs
-- Exercise 1 & 2
-- ══════════════════════════════════════════════════════════════════════════════

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 1 - TASK 1
-- Rank movies by popularity within each genre using RANK()
-- ══════════════════════════════════════════════════════════════════════════════

SELECT
    g.genre_name,
    m.title,
    m.popularity,
    RANK() OVER (
        PARTITION BY g.genre_name
        ORDER BY m.popularity DESC
    ) AS popularity_rank
FROM movies m
JOIN movie_genres mg ON mg.movie_id  = m.movie_id
JOIN genres       g  ON g.genre_id   = mg.genre_id
ORDER BY g.genre_name, popularity_rank;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 1 - TASK 2
-- Divide movies into quartiles by revenue within each production company
-- using NTILE(4)
-- ══════════════════════════════════════════════════════════════════════════════

SELECT
    pc.company_name,
    m.title,
    m.revenue,
    NTILE(4) OVER (
        PARTITION BY pc.company_name
        ORDER BY m.revenue DESC
    ) AS revenue_quartile
FROM movies               m
JOIN movie_companies      mpc ON mpc.movie_id   = m.movie_id
JOIN production_companies pc  ON pc.company_id  = mpc.company_id
WHERE m.revenue > 0
ORDER BY pc.company_name, revenue_quartile, m.revenue DESC;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 1 - TASK 3
-- Running total of movie budgets within each genre using SUM() + ROWS frame
-- ══════════════════════════════════════════════════════════════════════════════

SELECT
    g.genre_name,
    m.title,
    m.budget,
    SUM(m.budget) OVER (
        PARTITION BY g.genre_name
        ORDER BY m.release_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_budget
FROM movies       m
JOIN movie_genres mg ON mg.movie_id = m.movie_id
JOIN genres       g  ON g.genre_id  = mg.genre_id
WHERE m.budget > 0
ORDER BY g.genre_name, m.release_date;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 1 - TASK 4
-- Most recent movie for each genre using FIRST_VALUE()
-- ══════════════════════════════════════════════════════════════════════════════

SELECT DISTINCT
    g.genre_name,
    FIRST_VALUE(m.title) OVER (
        PARTITION BY g.genre_name
        ORDER BY m.release_date DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS most_recent_title,
    FIRST_VALUE(m.release_date) OVER (
        PARTITION BY g.genre_name
        ORDER BY m.release_date DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS most_recent_date
FROM movies       m
JOIN movie_genres mg ON mg.movie_id = m.movie_id
JOIN genres       g  ON g.genre_id  = mg.genre_id
WHERE m.release_date IS NOT NULL
ORDER BY g.genre_name;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2 - TASK 1
-- Rank actors by number of movie appearances using DENSE_RANK()
-- ══════════════════════════════════════════════════════════════════════════════

SELECT
    p.person_name                          AS actor_name,
    COUNT(DISTINCT mc.movie_id)            AS movie_count,
    DENSE_RANK() OVER (
        ORDER BY COUNT(DISTINCT mc.movie_id) DESC
    )                                      AS appearance_rank
FROM movie_cast mc
JOIN persons    p ON p.person_id = mc.person_id
GROUP BY p.person_id, p.person_name
ORDER BY appearance_rank
LIMIT 50;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2 - TASK 2
-- Top director by average movie rating using CTE + RANK()
-- ══════════════════════════════════════════════════════════════════════════════

WITH director_avg_rating AS (
    SELECT
        p.person_name                        AS director_name,
        ROUND(AVG(m.vote_average), 4)        AS avg_rating,
        COUNT(DISTINCT mc.movie_id)          AS movies_directed
    FROM movie_crew mc
    JOIN persons    p ON p.person_id  = mc.person_id
    JOIN movies     m ON m.movie_id   = mc.movie_id
    WHERE mc.job = 'Director'
      AND m.vote_count > 10          -- filter out movies with too few votes
    GROUP BY p.person_id, p.person_name
    HAVING COUNT(DISTINCT mc.movie_id) >= 2  -- at least 2 films directed
),
ranked_directors AS (
    SELECT
        director_name,
        avg_rating,
        movies_directed,
        RANK() OVER (ORDER BY avg_rating DESC) AS rating_rank
    FROM director_avg_rating
)
SELECT *
FROM ranked_directors
WHERE rating_rank <= 10
ORDER BY rating_rank;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2 - TASK 3
-- Cumulative revenue of movies for each actor using SUM() window function
-- ══════════════════════════════════════════════════════════════════════════════

SELECT
    p.person_name                AS actor_name,
    m.title,
    m.release_date,
    m.revenue,
    SUM(m.revenue) OVER (
        PARTITION BY p.person_id
        ORDER BY m.release_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )                            AS cumulative_revenue
FROM movie_cast mc
JOIN persons    p ON p.person_id = mc.person_id
JOIN movies     m ON m.movie_id  = mc.movie_id
WHERE m.revenue > 0
ORDER BY p.person_name, m.release_date;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2 - TASK 4
-- Director with highest total budget using CTE + window function
-- ══════════════════════════════════════════════════════════════════════════════

WITH director_budgets AS (
    SELECT
        p.person_id,
        p.person_name                              AS director_name,
        SUM(m.budget)                              AS total_budget,
        COUNT(DISTINCT mc.movie_id)                AS movies_directed,
        RANK() OVER (ORDER BY SUM(m.budget) DESC)  AS budget_rank
    FROM movie_crew mc
    JOIN persons    p ON p.person_id = mc.person_id
    JOIN movies     m ON m.movie_id  = mc.movie_id
    WHERE mc.job    = 'Director'
      AND m.budget  > 0
    GROUP BY p.person_id, p.person_name
)
SELECT
    director_name,
    total_budget,
    movies_directed,
    budget_rank
FROM director_budgets
WHERE budget_rank <= 10
ORDER BY budget_rank;
