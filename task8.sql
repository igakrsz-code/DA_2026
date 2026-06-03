-- ══════════════════════════════════════════════════════════════════════════════
-- Exercise 2 - Task 4
-- Temp table: competitors who participated in BOTH Summer and Winter games
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TEMPORARY TABLE IF NOT EXISTS both_seasons AS
SELECT
    id,
    name
FROM athlete_events
GROUP BY id, name
HAVING
    COUNT(DISTINCT season)                                    = 2
    AND MAX(CASE WHEN season = 'Summer' THEN 1 ELSE 0 END)   = 1
    AND MAX(CASE WHEN season = 'Winter' THEN 1 ELSE 0 END)   = 1;

-- Total count
SELECT COUNT(*) AS competitors_in_both_seasons
FROM both_seasons;

-- Full breakdown with games details
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
