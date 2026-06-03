-- ══════════════════════════════════════════════════════════════════════════════
-- OLYMPIC DAILY CHALLENGE — Exercise 1 & 2
-- ══════════════════════════════════════════════════════════════════════════════

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 1 - TASK 1
-- Competitors who won medals in BOTH Summer and Winter Olympics
-- Temp table stores their medal counts per season
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TEMPORARY TABLE IF NOT EXISTS both_season_medalists AS
SELECT
    ae.id,
    ae.name,
    ae.season,
    COUNT(ae.medal) AS medal_count
FROM athlete_events ae
WHERE ae.medal IS NOT NULL
  AND ae.id IN (
      -- subquery: only competitors who have medals in BOTH seasons
      SELECT id
      FROM athlete_events
      WHERE medal IS NOT NULL
      GROUP BY id
      HAVING
          MAX(CASE WHEN season = 'Summer' THEN 1 ELSE 0 END) = 1
          AND MAX(CASE WHEN season = 'Winter' THEN 1 ELSE 0 END) = 1
  )
GROUP BY ae.id, ae.name, ae.season
ORDER BY ae.name, ae.season;

-- Display the temp table
SELECT *
FROM both_season_medalists
ORDER BY name, season;

-- Summary: total medals per competitor across both seasons
SELECT
    id,
    name,
    SUM(medal_count)                                              AS total_medals,
    MAX(CASE WHEN season = 'Summer' THEN medal_count ELSE 0 END) AS summer_medals,
    MAX(CASE WHEN season = 'Winter' THEN medal_count ELSE 0 END) AS winter_medals
FROM both_season_medalists
GROUP BY id, name
ORDER BY total_medals DESC
LIMIT 20;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 1 - TASK 2
-- Temp table: competitors who won medals in exactly 2 different sports
-- Then find the top 3 by total medal count using a subquery
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TEMPORARY TABLE IF NOT EXISTS two_sport_medalists AS
SELECT
    ae.id,
    ae.name,
    COUNT(ae.medal)        AS total_medals,
    COUNT(DISTINCT ae.sport) AS distinct_sports
FROM athlete_events ae
WHERE ae.medal IS NOT NULL
  AND ae.id IN (
      -- subquery: competitors with medals in exactly 2 sports
      SELECT id
      FROM athlete_events
      WHERE medal IS NOT NULL
      GROUP BY id
      HAVING COUNT(DISTINCT sport) = 2
  )
GROUP BY ae.id, ae.name
ORDER BY total_medals DESC;

-- Display full temp table
SELECT *
FROM two_sport_medalists
ORDER BY total_medals DESC;

-- Top 3 competitors with highest total medals from this group
SELECT *
FROM (
    SELECT
        id,
        name,
        total_medals,
        distinct_sports
    FROM two_sport_medalists
    ORDER BY total_medals DESC
    LIMIT 3
) top3;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2 - TASK 1
-- Top 5 regions with highest total medals
-- Uses subquery to find the event with most medals per competitor
-- ══════════════════════════════════════════════════════════════════════════════

SELECT
    nr.region,
    COUNT(ae.medal) AS total_medals
FROM athlete_events ae
JOIN noc_regions nr ON nr.noc = ae.noc
WHERE ae.medal IS NOT NULL
  AND ae.event IN (
      -- subquery: events where any competitor has won the most medals
      SELECT event
      FROM athlete_events
      WHERE medal IS NOT NULL
      GROUP BY id, event
      HAVING COUNT(medal) = (
          -- innermost subquery: the maximum medals one person won in one event
          SELECT MAX(event_medals)
          FROM (
              SELECT COUNT(medal) AS event_medals
              FROM athlete_events
              WHERE medal IS NOT NULL
              GROUP BY id, event
          ) max_sub
      )
  )
GROUP BY nr.region
ORDER BY total_medals DESC
LIMIT 5;

-- ══════════════════════════════════════════════════════════════════════════════
-- EXERCISE 2 - TASK 2
-- Temp table: competitors who joined more than 3 Olympic Games
-- but have NEVER won a medal
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TEMPORARY TABLE IF NOT EXISTS no_medal_veterans AS
SELECT
    ae.id,
    ae.name,
    COUNT(DISTINCT ae.games) AS games_participated
FROM athlete_events ae
WHERE ae.id NOT IN (
        -- subquery: exclude anyone who has ever won a medal
        SELECT DISTINCT id
        FROM athlete_events
        WHERE medal IS NOT NULL
    )
GROUP BY ae.id, ae.name
HAVING COUNT(DISTINCT ae.games) > 3
ORDER BY games_participated DESC;

-- Display the temp table
SELECT *
FROM no_medal_veterans
ORDER BY games_participated DESC;

-- Summary stats
SELECT
    COUNT(*)                        AS total_competitors,
    MAX(games_participated)         AS max_games,
    ROUND(AVG(games_participated), 2) AS avg_games
FROM no_medal_veterans;
