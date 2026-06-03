-- ══════════════════════════════════════════════════════════════════════════════
-- ADVANCED MOVIE DATA ANALYSIS — Daily Challenge
-- Tasks 1-4: Window Functions & CTEs
-- ══════════════════════════════════════════════════════════════════════════════

-- ══════════════════════════════════════════════════════════════════════════════
-- TASK 1
-- Average budget growth rate for each production company
-- LAG() gets the previous movie's budget, then we calculate % growth
-- and average it across all movies per company
-- ══════════════════════════════════════════════════════════════════════════════

WITH ordered_budgets AS (
    -- attach company name and order movies by release date per company
    SELECT
        pc.company_name,
        m.title,
        m.release_date,
        m.budget,
        LAG(m.budget) OVER (
            PARTITION BY pc.company_id
            ORDER BY m.release_date
        ) AS prev_budget
    FROM movies               m
    JOIN movie_companies      mpc ON mpc.movie_id  = m.movie_id
    JOIN production_companies pc  ON pc.company_id = mpc.company_id
    WHERE m.budget > 0
),
growth_rates AS (
    -- calculate % growth from one movie to the next
    SELECT
        company_name,
        title,
        release_date,
        budget,
        prev_budget,
        CASE
            WHEN prev_budget > 0
            THEN ROUND(
                    ((budget - prev_budget)::NUMERIC / prev_budget) * 100
                 , 2)
            ELSE NULL
        END AS budget_growth_pct
    FROM ordered_budgets
    WHERE prev_budget IS NOT NULL
      AND prev_budget > 0
)
SELECT
    company_name,
    COUNT(*)                              AS movies_analysed,
    ROUND(AVG(budget_growth_pct), 2)      AS avg_budget_growth_rate_pct,
    ROUND(MAX(budget_growth_pct), 2)      AS max_growth_pct,
    ROUND(MIN(budget_growth_pct), 2)      AS min_growth_pct
FROM growth_rates
GROUP BY company_name
HAVING COUNT(*) >= 2          -- need at least 2 movies to measure growth
ORDER BY avg_budget_growth_rate_pct DESC
LIMIT 20;

-- ══════════════════════════════════════════════════════════════════════════════
-- TASK 2
-- Most consistently high-rated actor
-- Finds actors who appeared in the most movies rated ABOVE the global average
-- ══════════════════════════════════════════════════════════════════════════════

WITH global_avg AS (
    -- step 1: calculate the overall average rating across all movies
    SELECT AVG(vote_average) AS overall_avg_rating
    FROM movies
    WHERE vote_count > 10       -- exclude movies with too few votes
),
above_avg_movies AS (
    -- step 2: filter movies that are above the global average
    SELECT m.movie_id,
           m.title,
           m.vote_average
    FROM movies m, global_avg g
    WHERE m.vote_average > g.overall_avg_rating
      AND m.vote_count   > 10
),
actor_above_avg_counts AS (
    -- step 3: count how many above-average movies each actor appeared in
    SELECT
        p.person_id,
        p.person_name                        AS actor_name,
        COUNT(DISTINCT mc.movie_id)          AS above_avg_movie_count,
        ROUND(AVG(aam.vote_average), 4)      AS avg_rating_in_those_films
    FROM movie_cast    mc
    JOIN persons       p   ON p.person_id  = mc.person_id
    JOIN above_avg_movies aam ON aam.movie_id = mc.movie_id
    GROUP BY p.person_id, p.person_name
),
ranked_actors AS (
    -- step 4: rank actors by how many above-average movies they appeared in
    SELECT
        actor_name,
        above_avg_movie_count,
        avg_rating_in_those_films,
        DENSE_RANK() OVER (
            ORDER BY above_avg_movie_count DESC
        ) AS consistency_rank
    FROM actor_above_avg_counts
)
SELECT
    actor_name,
    above_avg_movie_count,
    ROUND(avg_rating_in_those_films, 2) AS avg_rating,
    consistency_rank
FROM ranked_actors
WHERE consistency_rank <= 10
ORDER BY consistency_rank;

-- ══════════════════════════════════════════════════════════════════════════════
-- TASK 3
-- Rolling average revenue for each genre
-- Considers only the last 3 movies released in each genre
-- Uses ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
-- ══════════════════════════════════════════════════════════════════════════════

SELECT
    g.genre_name,
    m.title,
    m.release_date,
    m.revenue,
    ROUND(
        AVG(m.revenue) OVER (
            PARTITION BY g.genre_id
            ORDER BY m.release_date
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW   -- last 3 movies
        )
    , 2) AS rolling_avg_revenue_last3
FROM movies       m
JOIN movie_genres mg ON mg.movie_id = m.movie_id
JOIN genres       g  ON g.genre_id  = mg.genre_id
WHERE m.revenue      > 0
  AND m.release_date IS NOT NULL
ORDER BY g.genre_name, m.release_date;

-- ══════════════════════════════════════════════════════════════════════════════
-- TASK 4
-- Highest-grossing movie series based on shared keywords
-- Groups movies by keyword and sums their revenue
-- Uses CTE + SUM() window function to find the top series
-- ══════════════════════════════════════════════════════════════════════════════

WITH keyword_revenues AS (
    -- step 1: join movies to their keywords and get revenue per keyword group
    SELECT
        k.keyword_name                       AS series_keyword,
        m.movie_id,
        m.title,
        m.revenue,
        m.release_date
    FROM movies        m
    JOIN movie_keywords mk ON mk.movie_id   = m.movie_id
    JOIN keywords       k  ON k.keyword_id  = mk.keyword_id
    WHERE m.revenue > 0
),
series_totals AS (
    -- step 2: sum revenue per keyword (= series) and count movies in series
    SELECT
        series_keyword,
        COUNT(DISTINCT movie_id)             AS movies_in_series,
        SUM(revenue)                         AS total_series_revenue,
        RANK() OVER (
            ORDER BY SUM(revenue) DESC
        )                                    AS revenue_rank
    FROM keyword_revenues
    GROUP BY series_keyword
    HAVING COUNT(DISTINCT movie_id) >= 2     -- a series needs 2+ movies
),
top_series AS (
    -- step 3: keep only the top 10 series by total revenue
    SELECT *
    FROM series_totals
    WHERE revenue_rank <= 10
)
-- step 4: display top series with their individual movies
SELECT
    ts.revenue_rank,
    ts.series_keyword,
    ts.movies_in_series,
    ts.total_series_revenue,
    kr.title,
    kr.revenue        AS individual_movie_revenue,
    kr.release_date
FROM top_series      ts
JOIN keyword_revenues kr ON kr.series_keyword = ts.series_keyword
ORDER BY ts.revenue_rank, kr.release_date;
