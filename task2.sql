-- ══════════════════════════════════════════════════════════════════════════════
-- Exercise 1 - Task 2
-- Top 5 regions with highest number of unique competitors
-- who participated in more than 3 different events
-- Uses nested subqueries
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
