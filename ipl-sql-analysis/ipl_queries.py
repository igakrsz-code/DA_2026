# ══════════════════════════════════════════════════════════════════════════════
# IPL DATABASE — Complex SQL Query Building
# ══════════════════════════════════════════════════════════════════════════════

# ── Step 1: Install and import ────────────────────────────────────────────────
import io, zipfile, urllib.request, os
import sqlite3
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

# ── Download and extract the IPL database ─────────────────────────────────────
URL = ("https://github.com/devtlv/Datasets-DA-Bootcamp-2-/raw/refs/heads/main/"
       "Week%2010%20-%20Advanced%20SQL/W10D4%20-%20Mini%20project/"
       "Approach%20to%20Complex%20SQLquery%20Building%20in%20Kaggle.zip")

print("Downloading IPL dataset…")
with urllib.request.urlopen(URL) as r:
    zip_bytes = r.read()

with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
    print("Files in zip:", zf.namelist())
    # extract everything to current directory
    zf.extractall("ipl_data")

# Find the .sqlite or .db file
db_path = None
for root, dirs, files in os.walk("ipl_data"):
    for f in files:
        if f.endswith(".sqlite") or f.endswith(".db"):
            db_path = os.path.join(root, f)
            break

if db_path:
    print(f"Database found: {db_path}")
else:
    # some zips contain CSV files — build an in-memory SQLite db from them
    print("No .db file found — building SQLite from CSVs…")
    db_path = "ipl_data/ipl.db"

conn   = sqlite3.connect(db_path)
cursor = conn.cursor()

# ══════════════════════════════════════════════════════════════════════════════
# TASK 1: Load and Explore the Data
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*60)
print("TASK 1: Load and Explore the Data")
print("═"*60)

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print(f"\nTables in database: {tables}")

# Load all tables and print column names
all_dfs = {}
for table in tables:
    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 5", conn)
    all_dfs[table] = df
    print(f"\n── {table} ──")
    print(f"  Columns ({len(df.columns)}): {df.columns.tolist()}")
    print(f"  Row count: {pd.read_sql_query(f'SELECT COUNT(*) AS cnt FROM {table}', conn).iloc[0,0]:,}")

# Show master/player table structure
master_table = [t for t in tables if "player" in t.lower()
                or "master" in t.lower()][0]
print(f"\nMaster table preview ({master_table}):")
display(all_dfs[master_table])

# ══════════════════════════════════════════════════════════════════════════════
# TASK 2: Query 1 — Select All Columns from Player_Match Table
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*60)
print("QUERY 1: All columns from Player_Match table")
print("═"*60)

# Find the player match table
player_match_table = [t for t in tables
                      if "player" in t.lower() and "match" in t.lower()]
if player_match_table:
    pm_table = player_match_table[0]
else:
    pm_table = tables[0]

query1 = f"SELECT * FROM {pm_table} LIMIT 20"
df_q1  = pd.read_sql_query(query1, conn)
print(f"\nTable: {pm_table}  |  Shape: {df_q1.shape}")
display(df_q1)

# ══════════════════════════════════════════════════════════════════════════════
# TASK 3: Query 2 — Batsman vs Total Runs
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*60)
print("QUERY 2: Total Runs Scored by Each Batsman")
print("═"*60)

# Find ball-by-ball / batting table
ball_table = [t for t in tables
              if "ball" in t.lower() or "batting" in t.lower()
              or "delivery" in t.lower() or "bbb" in t.lower()]

if ball_table:
    bt = ball_table[0]
    cols = pd.read_sql_query(f"PRAGMA table_info({bt})", conn)["name"].tolist()
    print(f"Ball table: {bt}  |  Columns: {cols}")

    # Identify batsman and runs columns dynamically
    batsman_col = next((c for c in cols if "batsman" in c.lower() or "striker" in c.lower()), cols[0])
    runs_col    = next((c for c in cols if "runs" in c.lower() and "bat" in c.lower()), None)
    if not runs_col:
        runs_col = next((c for c in cols if "run" in c.lower()), cols[-1])

    query2 = f"""
        SELECT
            {batsman_col}                  AS batsman,
            SUM({runs_col})                AS total_runs,
            COUNT(*)                       AS balls_faced,
            ROUND(SUM({runs_col}) * 100.0
                  / COUNT(*), 2)           AS strike_rate,
            MAX({runs_col})                AS highest_score_in_ball
        FROM {bt}
        GROUP BY {batsman_col}
        HAVING COUNT(*) >= 10
        ORDER BY total_runs DESC
        LIMIT 20
    """
else:
    # Fallback: try to use any table with runs
    bt = tables[0]
    query2 = f"SELECT * FROM {bt} LIMIT 5"

df_q2 = pd.read_sql_query(query2, conn)
print(f"\nTop 20 run-scorers:")
display(df_q2)

# ══════════════════════════════════════════════════════════════════════════════
# TASK 4: Query 3 — Fifties and Hundreds per Batsman
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*60)
print("QUERY 3: Fifties and Hundreds per Batsman")
print("═"*60)

if ball_table:
    query3 = f"""
        WITH innings_scores AS (
            SELECT
                {batsman_col}                  AS batsman,
                match_id,
                SUM({runs_col})                AS innings_runs
            FROM {bt}
            GROUP BY {batsman_col}, match_id
        )
        SELECT
            batsman,
            COUNT(*)                           AS total_innings,
            SUM(innings_runs)                  AS total_runs,
            SUM(CASE WHEN innings_runs >= 100
                     THEN 1 ELSE 0 END)        AS hundreds,
            SUM(CASE WHEN innings_runs >= 50
                      AND innings_runs < 100
                     THEN 1 ELSE 0 END)        AS fifties,
            SUM(CASE WHEN innings_runs >= 30
                      AND innings_runs < 50
                     THEN 1 ELSE 0 END)        AS thirties,
            MAX(innings_runs)                  AS highest_score,
            ROUND(AVG(innings_runs), 2)        AS batting_average
        FROM innings_scores
        GROUP BY batsman
        HAVING total_innings >= 5
        ORDER BY total_runs DESC
        LIMIT 20
    """
    df_q3 = pd.read_sql_query(query3, conn)
    print("\nBatting milestones (top 20 by total runs):")
    display(df_q3)
else:
    print("Ball-by-ball table not found — skipping Query 3")

# ══════════════════════════════════════════════════════════════════════════════
# TASK 5: Query 4 — Best Bowling Figures
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*60)
print("QUERY 4: Best Bowling Figures per Bowler")
print("═"*60)

if ball_table:
    cols = pd.read_sql_query(f"PRAGMA table_info({bt})", conn)["name"].tolist()

    bowler_col  = next((c for c in cols if "bowler" in c.lower()), None)
    wicket_col  = next((c for c in cols
                        if "wicket" in c.lower() or "dismissed" in c.lower()), None)
    extras_col  = next((c for c in cols if "extra" in c.lower()), None)

    if bowler_col and wicket_col:
        query4 = f"""
            WITH match_figures AS (
                SELECT
                    {bowler_col}                             AS bowler,
                    match_id,
                    COUNT(*)                                 AS balls_bowled,
                    ROUND(COUNT(*) / 6.0, 1)                AS overs,
                    SUM({runs_col})                          AS runs_conceded,
                    SUM(CASE WHEN {wicket_col} IS NOT NULL
                              AND {wicket_col} != ''
                              AND {wicket_col} != 'NA'
                             THEN 1 ELSE 0 END)              AS wickets
                FROM {bt}
                GROUP BY {bowler_col}, match_id
            ),
            best_figures AS (
                SELECT
                    bowler,
                    match_id,
                    overs,
                    runs_conceded,
                    wickets,
                    RANK() OVER (
                        PARTITION BY bowler
                        ORDER BY wickets DESC, runs_conceded ASC
                    ) AS figure_rank
                FROM match_figures
            )
            SELECT
                bf.bowler,
                COUNT(DISTINCT mf.match_id)               AS matches,
                SUM(mf.balls_bowled)                      AS total_balls,
                ROUND(SUM(mf.balls_bowled)/6.0, 1)        AS total_overs,
                SUM(mf.runs_conceded)                     AS total_runs,
                SUM(mf.wickets)                           AS total_wickets,
                ROUND(SUM(mf.runs_conceded) * 6.0
                      / NULLIF(SUM(mf.balls_bowled),0),2) AS economy,
                ROUND(SUM(mf.runs_conceded) * 1.0
                      / NULLIF(SUM(mf.wickets),0), 2)     AS bowling_average,
                -- Best figures in a single match
                MAX(bf.wickets) || '/' ||
                MIN(CASE WHEN bf.figure_rank = 1
                         THEN bf.runs_conceded END)       AS best_figures
            FROM match_figures mf
            JOIN best_figures  bf ON bf.bowler   = mf.bowler
                                  AND bf.match_id = mf.match_id
                                  AND bf.figure_rank = 1
            GROUP BY bf.bowler
            HAVING total_wickets >= 5
            ORDER BY total_wickets DESC
            LIMIT 20
        """
        df_q4 = pd.read_sql_query(query4, conn)
        print("\nTop 20 bowlers by total wickets:")
        display(df_q4)
    else:
        print(f"Bowler/wicket columns not found in {bt}. Columns: {cols}")

# ══════════════════════════════════════════════════════════════════════════════
# TASK 6: Query 5 — Comprehensive Career Metrics (all combined)
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*60)
print("QUERY 5: Comprehensive Career Metrics")
print("═"*60)

if ball_table and bowler_col and wicket_col:
    query5 = f"""
        WITH
        -- ── batting per innings ───────────────────────────────────────────
        batting_innings AS (
            SELECT
                {batsman_col}           AS player,
                match_id,
                SUM({runs_col})         AS innings_runs,
                COUNT(*)                AS balls_faced
            FROM {bt}
            GROUP BY {batsman_col}, match_id
        ),
        -- ── batting career aggregates ─────────────────────────────────────
        batting_career AS (
            SELECT
                player,
                COUNT(*)                                    AS innings,
                SUM(innings_runs)                           AS total_runs,
                MAX(innings_runs)                           AS highest_score,
                ROUND(AVG(innings_runs), 2)                 AS bat_average,
                ROUND(SUM(innings_runs) * 100.0
                      / NULLIF(SUM(balls_faced), 0), 2)     AS strike_rate,
                SUM(CASE WHEN innings_runs >= 100
                         THEN 1 ELSE 0 END)                 AS hundreds,
                SUM(CASE WHEN innings_runs >= 50
                          AND innings_runs < 100
                         THEN 1 ELSE 0 END)                 AS fifties
            FROM batting_innings
            GROUP BY player
        ),
        -- ── bowling per match ─────────────────────────────────────────────
        bowling_match AS (
            SELECT
                {bowler_col}            AS player,
                match_id,
                COUNT(*)                AS balls,
                SUM({runs_col})         AS runs_given,
                SUM(CASE WHEN {wicket_col} IS NOT NULL
                          AND {wicket_col} != ''
                          AND {wicket_col} != 'NA'
                         THEN 1 ELSE 0 END) AS wickets
            FROM {bt}
            GROUP BY {bowler_col}, match_id
        ),
        -- ── bowling career aggregates ─────────────────────────────────────
        bowling_career AS (
            SELECT
                player,
                COUNT(DISTINCT match_id)                    AS matches_bowled,
                SUM(balls)                                  AS total_balls,
                SUM(runs_given)                             AS total_runs_given,
                SUM(wickets)                                AS total_wickets,
                ROUND(SUM(runs_given) * 6.0
                      / NULLIF(SUM(balls), 0), 2)           AS economy,
                ROUND(SUM(runs_given) * 1.0
                      / NULLIF(SUM(wickets), 0), 2)         AS bowl_average,
                ROUND(SUM(balls) * 1.0
                      / NULLIF(SUM(wickets), 0), 2)         AS strike_rate_bowl,
                MAX(wickets)                                AS best_match_wickets,
                SUM(CASE WHEN wickets >= 3
                         THEN 1 ELSE 0 END)                 AS three_wicket_hauls
            FROM bowling_match
            GROUP BY player
        ),
        -- ── window rank on batting ────────────────────────────────────────
        batting_ranked AS (
            SELECT
                *,
                RANK() OVER (ORDER BY total_runs DESC) AS run_rank,
                RANK() OVER (ORDER BY strike_rate DESC) AS sr_rank
            FROM batting_career
            WHERE innings >= 5
        ),
        -- ── window rank on bowling ────────────────────────────────────────
        bowling_ranked AS (
            SELECT
                *,
                RANK() OVER (ORDER BY total_wickets DESC) AS wkt_rank,
                RANK() OVER (ORDER BY economy ASC)        AS eco_rank
            FROM bowling_career
            WHERE total_balls >= 60
        )
        -- ── final combined output ─────────────────────────────────────────
        SELECT
            COALESCE(bat.player, bowl.player)   AS player,
            -- batting
            bat.innings,
            bat.total_runs,
            bat.highest_score,
            bat.bat_average,
            bat.strike_rate                     AS bat_strike_rate,
            bat.hundreds,
            bat.fifties,
            bat.run_rank,
            -- bowling
            bowl.matches_bowled,
            bowl.total_wickets,
            bowl.economy,
            bowl.bowl_average,
            bowl.strike_rate_bowl,
            bowl.best_match_wickets,
            bowl.three_wicket_hauls,
            bowl.wkt_rank
        FROM batting_ranked  bat
        FULL OUTER JOIN bowling_ranked bowl ON bowl.player = bat.player
        ORDER BY
            COALESCE(bat.total_runs, 0) + COALESCE(bowl.total_wickets, 0) * 20
            DESC
        LIMIT 30
    """

    try:
        df_q5 = pd.read_sql_query(query5, conn)
        print("\nComprehensive Career Metrics (top 30 all-round performers):")
        display(df_q5)
    except Exception as e:
        print(f"FULL OUTER JOIN not supported in this SQLite version ({e})")
        print("Running LEFT JOIN version instead…")

        query5_fallback = f"""
            WITH
            batting_innings AS (
                SELECT {batsman_col} AS player, match_id,
                       SUM({runs_col}) AS innings_runs, COUNT(*) AS balls_faced
                FROM {bt} GROUP BY {batsman_col}, match_id
            ),
            batting_career AS (
                SELECT player, COUNT(*) AS innings,
                       SUM(innings_runs) AS total_runs,
                       MAX(innings_runs) AS highest_score,
                       ROUND(AVG(innings_runs), 2) AS bat_average,
                       ROUND(SUM(innings_runs)*100.0/NULLIF(SUM(balls_faced),0),2) AS strike_rate,
                       SUM(CASE WHEN innings_runs>=100 THEN 1 ELSE 0 END) AS hundreds,
                       SUM(CASE WHEN innings_runs>=50 AND innings_runs<100 THEN 1 ELSE 0 END) AS fifties
                FROM batting_innings GROUP BY player HAVING COUNT(*) >= 5
            ),
            bowling_match AS (
                SELECT {bowler_col} AS player, match_id, COUNT(*) AS balls,
                       SUM({runs_col}) AS runs_given,
                       SUM(CASE WHEN {wicket_col} IS NOT NULL AND {wicket_col}!=''
                                 AND {wicket_col}!='NA' THEN 1 ELSE 0 END) AS wickets
                FROM {bt} GROUP BY {bowler_col}, match_id
            ),
            bowling_career AS (
                SELECT player, SUM(balls) AS total_balls,
                       SUM(runs_given) AS total_runs_given,
                       SUM(wickets) AS total_wickets,
                       ROUND(SUM(runs_given)*6.0/NULLIF(SUM(balls),0),2) AS economy,
                       ROUND(SUM(runs_given)*1.0/NULLIF(SUM(wickets),0),2) AS bowl_average,
                       MAX(wickets) AS best_match_wickets
                FROM bowling_match GROUP BY player HAVING SUM(balls) >= 60
            )
            SELECT
                bat.player,
                bat.innings, bat.total_runs, bat.highest_score,
                bat.bat_average, bat.strike_rate,
                bat.hundreds, bat.fifties,
                bowl.total_wickets, bowl.economy,
                bowl.bowl_average, bowl.best_match_wickets
            FROM batting_career bat
            LEFT JOIN bowling_career bowl ON bowl.player = bat.player
            ORDER BY bat.total_runs DESC
            LIMIT 30
        """
        df_q5 = pd.read_sql_query(query5_fallback, conn)
        print("\nComprehensive Career Metrics (top 30 batsmen):")
        display(df_q5)

# ── Summary stats ─────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("SUMMARY INSIGHTS")
print("═"*60)
print(f"\nTotal tables analysed : {len(tables)}")
if 'df_q3' in dir():
    print(f"Players with 100s    : {(df_q3['hundreds'] > 0).sum()}")
    print(f"Players with 50s     : {(df_q3['fifties']  > 0).sum()}")
    print(f"Top run scorer       : {df_q3.iloc[0]['batsman']} "
          f"({df_q3.iloc[0]['total_runs']} runs)")
if 'df_q4' in dir():
    print(f"Top wicket taker     : {df_q4.iloc[0]['bowler']} "
          f"({df_q4.iloc[0]['total_wickets']} wickets)")

conn.close()
print("\nDatabase connection closed ✅")
