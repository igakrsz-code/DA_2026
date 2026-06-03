-- ══════════════════════════════════════════════════════════════════════════════
-- Exercise 2 - Task 3
-- Regions where the average medals per competitor is greater
-- than the overall global average
-- Uses subquery to calculate global average for comparison
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
        -- global average medals per competitor
        SELECT
            COUNT(CASE WHEN medal IS NOT NULL THEN 1 END)::NUMERIC
            / COUNT(DISTINCT id)
        FROM athlete_events
    )
ORDER BY avg_medals_per_competitor DESC;
