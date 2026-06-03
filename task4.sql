-- ══════════════════════════════════════════════════════════════════════════════
-- Exercise 1 - Task 4
-- Create a temp table with all competitors
-- Delete those who have not won any medals using a subquery
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TEMPORARY TABLE IF NOT EXISTS analysis_competitors AS
SELECT
    id,
    name,
    COUNT(medal) AS total_medals
FROM athlete_events
GROUP BY id, name;

-- Row count before delete
SELECT COUNT(*) AS before_delete FROM analysis_competitors;

-- Delete competitors with zero medals
DELETE FROM analysis_competitors
WHERE id IN (
    SELECT id
    FROM athlete_events
    GROUP BY id
    HAVING COUNT(medal) = 0
);

-- Row count after delete — only medal winners remain
SELECT COUNT(*) AS after_delete FROM analysis_competitors;

SELECT *
FROM analysis_competitors
ORDER BY total_medals DESC
LIMIT 20;
