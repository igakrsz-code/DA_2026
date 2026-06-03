-- ══════════════════════════════════════════════════════════════════════════════
-- Exercise 2 - Task 1
-- Update NULL heights using the average height of competitors
-- from the same region — correlated subquery inside UPDATE
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
