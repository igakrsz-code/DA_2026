-- ══════════════════════════════════════════════════════════════════════════════
-- Exercise 2 - Task 2
-- Temp table: competitors who participated in more than one event
-- in the same games, with their total event count
-- Uses nested subqueries
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
