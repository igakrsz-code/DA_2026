-- ══════════════════════════════════════════════════════════════════════════════
-- Exercise 1 - Task 3
-- Temporary table: total medals per competitor
-- Filter to show only competitors with more than 2 medals
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TEMPORARY TABLE IF NOT EXISTS competitor_medals AS
SELECT
    ae.id,
    ae.name,
    COUNT(ae.medal) AS total_medals
FROM athlete_events ae
WHERE ae.medal IS NOT NULL
GROUP BY ae.id, ae.name;

-- Show only competitors with more than 2 medals
SELECT *
FROM competitor_medals
WHERE total_medals > 2
ORDER BY total_medals DESC;
