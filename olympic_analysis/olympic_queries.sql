-- ══════════════════════════════════════════════════════════════════════════════
-- OLYMPIC DATA ANALYSIS — All Exercises & Tasks
-- ══════════════════════════════════════════════════════════════════════════════

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 1 - TASK 1
-- Average age of medal winners grouped by medal type (correlated subquery)
-- ══════════════════════════════════════════════════════════════════════════════

SELECT
    medal,
    ROUND(AVG(age), 2) AS avg_age
FROM athlete_events ae1
WHERE medal IS NOT NULL
  AND EXISTS (
      SELECT 1
      FROM athlete_events ae2
      WHERE ae2.id    = ae1.id
        AND ae2.medal IS NOT NULL
  )
GROUP BY medal
ORDER BY medal;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 1 - TASK 2
-- Top 5 regions with most unique competitors who joined 3+ different events
-- ══════════════════════════════════════════════════════════════════════════════

SELECT
    nr.region,
    COUNT(DISTINCT sub.id) AS unique_competitors
FROM (
    SELECT id
    FROM athlete_events
    GROUP BY id
    HAVING COUNT(DISTINCT event) > 3
) sub
JOIN athlete_events ae ON ae.id  = sub.id
JOIN noc_regions    nr ON nr.noc = ae.noc
GROUP BY nr.region
ORDER BY unique_competitors DESC
LIMIT 5;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 1 - TASK 3
-- Temp table: total medals per competitor, show only those with more than 2
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TEMPORARY TABLE IF NOT EXISTS competitor_medals AS
SELECT
    ae.id,
    ae.name,
    COUNT(ae.medal) AS total_medals
FROM athlete_events ae
WHERE ae.medal IS NOT NULL
GROUP BY ae.id, ae.name;

SELECT *
FROM competitor_medals
WHERE total_medals > 2
ORDER BY total_medals DESC;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 1 - TASK 4
-- Temp table of all competitors, then DELETE those with zero medals
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TEMPORARY TABLE IF NOT EXISTS analysis_competitors AS
SELECT
    id,
    name,
    COUNT(medal) AS total_medals
FROM athlete_events
GROUP BY id, name;

-- Count before delete
SELECT COUNT(*) AS before_delete FROM analysis_competitors;

-- Delete zero-medal competitors using subquery
DELETE FROM analysis_competitors
WHERE id IN (
    SELECT id
    FROM athlete_events
    GROUP BY id
    HAVING COUNT(medal) = 0
);

-- Count after delete — only medal winners remain
SELECT COUNT(*) AS after_delete FROM analysis_competitors;

SELECT *
FROM analysis_competitors
ORDER BY total_medals DESC
LIMIT 20;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2 - TASK 1
-- UPDATE null heights using average height from same region (correlated subquery)
-- ══════════════════════════════════════════════════════════════════════════════

UPDATE athlete_events ae
SET height = (
    SELECT ROUND(AVG(ae2.height), 0)
    FROM athlete_events ae2
    JOIN noc_regions nr2 ON nr2.noc = ae2.noc
    WHERE nr2.region = (
        SELECT nr3.region
        FROM noc_regions nr3
        WHERE nr3.noc = ae.noc
        LIMIT 1
    )
    AND ae2.height IS NOT NULL
)
WHERE ae.height IS NULL
  AND EXISTS (
      SELECT 1
      FROM noc_regions nr
      WHERE nr.noc = ae.noc
  );

-- Verify sample of updated rows
SELECT id, name, noc, height
FROM athlete_events
WHERE height IS NOT NULL
LIMIT 10;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2 - TASK 2
-- Temp table: competitors in more than one event in the same games
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TEMPORARY TABLE IF NOT EXISTS multi_event_competitors AS
SELECT
    id,
    name,
    games,
    COUNT(DISTINCT event) AS total_events
FROM athlete_events
WHERE id IN (
    SELECT id
    FROM athlete_events
    GROUP BY id, games
    HAVING COUNT(DISTINCT event) > 1
)
GROUP BY id, name, games
HAVING COUNT(DISTINCT event) > 1
ORDER BY total_events DESC;

SELECT *
FROM multi_event_competitors
ORDER BY total_events DESC
LIMIT 20;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2 - TASK 3
-- Regions where avg medals per competitor > overall global average
-- ══════════════════════════════════════════════════════════════════════════════

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
        SELECT
            COUNT(CASE WHEN medal IS NOT NULL THEN 1 END)::NUMERIC
            / COUNT(DISTINCT id)
        FROM athlete_events
    )
ORDER BY avg_medals_per_competitor DESC;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2 - TASK 4
-- Temp table: competitors who participated in BOTH Summer and Winter games
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TEMPORARY TABLE IF NOT EXISTS both_seasons AS
SELECT
    id,
    name
FROM athlete_events
GROUP BY id, name
HAVING
    COUNT(DISTINCT season)                                  = 2
    AND MAX(CASE WHEN season = 'Summer' THEN 1 ELSE 0 END) = 1
    AND MAX(CASE WHEN season = 'Winter' THEN 1 ELSE 0 END) = 1;

-- Total count
SELECT COUNT(*) AS competitors_in_both_seasons
FROM both_seasons;

-- Full breakdown with season and games details
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
