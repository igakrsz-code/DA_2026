-- ══════════════════════════════════════════════════════════════════════════════
-- Exercise 1 - Task 1
-- Average age of competitors who won at least one medal, grouped by medal type
-- Uses a correlated subquery
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
