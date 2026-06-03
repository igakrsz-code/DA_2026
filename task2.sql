-- ── Task 2: Temp table — competitors in multiple events in the same games ──────

CREATE TEMPORARY TABLE IF NOT EXISTS multi_event_competitors AS
SELECT
    id,
    name,
    games,
    COUNT(DISTINCT event) AS total_events
FROM athlete_events
WHERE id IN (
    -- nested subquery: only competitors who appeared in >1 event in same games
    SELECT id
    FROM athlete_events
    GROUP BY id, games
    HAVING COUNT(DISTINCT event) > 1
)
GROUP BY id, name, games
HAVING COUNT(DISTINCT event) > 1
ORDER BY total_events DESC;

SELECT * FROM multi_event_competitors
ORDER BY total_events DESC
LIMIT 20;

-- ── Task 3: Regions where avg medals per competitor > overall average ──────────

-- Step 1: overall average medals per competitor across all regions
-- Step 2: calculate per-region average
-- Step 3: filter regions above the overall average

SELECT
    nr.region,
    ROUND(
        COUNT(CASE WHEN ae.medal IS NOT NULL THEN 1 END)::NUMERIC
        / COUNT(DISTINCT ae.id), 4
    ) AS avg_medals_per_competitor
FROM athlete_events ae
JOIN noc_regions nr ON nr.noc = ae.noc
GROUP BY nr.region
HAVING
    COUNT(CASE WHEN ae.medal IS NOT NULL THEN 1 END)::NUMERIC
    / COUNT(DISTINCT ae.id)
    > (
        -- overall average medals per competitor (global)
        SELECT
            COUNT(CASE WHEN medal IS NOT NULL THEN 1 END)::NUMERIC
            / COUNT(DISTINCT id)
        FROM athlete_events
    )
ORDER BY avg_medals_per_competitor DESC;

-- ── Task 4: Temp table — competitors who competed in BOTH Summer and Winter ────

CREATE TEMPORARY TABLE IF NOT EXISTS both_seasons AS
SELECT
    id,
    name
FROM athlete_events
GROUP BY id, name
HAVING
    COUNT(DISTINCT season) = 2          -- appeared in exactly 2 distinct seasons
    AND MAX(CASE WHEN season = 'Summer' THEN 1 ELSE 0 END) = 1
    AND MAX(CASE WHEN season = 'Winter' THEN 1 ELSE 0 END) = 1;

SELECT COUNT(*) AS competitors_in_both_seasons FROM both_seasons;

-- Full list with their games details
SELECT
    bs.id,
    bs.name,
    ae.season,
    ae.games,
    ae.sport
FROM both_seasons bs
JOIN athlete_events ae ON ae.id = bs.id
ORDER BY bs.id, ae.season, ae.games
LIMIT 50;
