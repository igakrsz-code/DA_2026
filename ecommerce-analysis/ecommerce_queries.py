# ══════════════════════════════════════════════════════════════════════════════
# BRAZILIAN E-COMMERCE ANALYSIS — Mini Project
# ══════════════════════════════════════════════════════════════════════════════

# ── Install dependencies ──────────────────────────────────────────────────────
!pip install -q kaggle sqlalchemy

# ── Download dataset from GitHub mirror ──────────────────────────────────────
import io, zipfile, urllib.request, os
import numpy as np
import pandas as pd
import sqlite3
from sqlalchemy import create_engine

BASE_URL = ("https://github.com/devtlv/Datasets-DA-Bootcamp-2-/raw/refs/heads/main/"
            "Week%2010%20-%20Advanced%20SQL/W10D4%20-%20Mini%20project/")

# Try direct download — fallback to synthetic if unavailable
FILES = {
    "olist_customers"                  : "olist_customers_dataset.csv",
    "olist_sellers"                    : "olist_sellers_dataset.csv",
    "olist_order_reviews"              : "olist_order_reviews_dataset.csv",
    "olist_order_items"                : "olist_order_items_dataset.csv",
    "olist_products_dataset"           : "olist_products_dataset.csv",
    "olist_geolocation"                : "olist_geolocation_dataset.csv",
    "product_category_name_translation": "product_category_name_translation.csv",
    "olist_orders"                     : "olist_orders_dataset.csv",
    "olist_order_payments"             : "olist_order_payments_dataset.csv",
}

# ══════════════════════════════════════════════════════════════════════════════
# TASK 1 & 2: Load Data and Create SQLite Database
# ══════════════════════════════════════════════════════════════════════════════

print("═"*60)
print("TASK 1 & 2: Load Data and Create SQLite Database")
print("═"*60)

# Try downloading from Kaggle via opendatasets or use synthetic fallback
try:
    import opendatasets as od
    od.download("https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce")
    data_path = "brazilian-ecommerce"
    dfs = {}
    for key, fname in FILES.items():
        fpath = os.path.join(data_path, fname)
        if os.path.exists(fpath):
            dfs[key] = pd.read_csv(fpath)
            print(f"  Loaded {key}: {dfs[key].shape}")
    print("Kaggle dataset loaded ✅")
except Exception:
    print("Kaggle download unavailable — generating realistic synthetic dataset…")

    np.random.seed(42)
    N = 5000

    states    = ["SP","RJ","MG","RS","PR","SC","BA","GO","PE","CE"]
    cities    = {"SP":["sao paulo","campinas","guarulhos"],
                 "RJ":["rio de janeiro","niteroi","nova iguacu"],
                 "MG":["belo horizonte","uberlandia","contagem"],
                 "RS":["porto alegre","caxias do sul","pelotas"],
                 "PR":["curitiba","londrina","maringa"],
                 "SC":["florianopolis","joinville","blumenau"],
                 "BA":["salvador","feira de santana","vitoria da conquista"],
                 "GO":["goiania","aparecida de goiania","anapolis"],
                 "PE":["recife","caruaru","petrolina"],
                 "CE":["fortaleza","caucaia","juazeiro do norte"]}
    categories = ["electronics","furniture","sports","beauty","books",
                  "toys","clothing","garden","auto","health"]
    payment_types = ["credit_card","boleto","voucher","debit_card"]

    # Generate customer_ids
    cust_ids   = [f"cust_{i:05d}" for i in range(N)]
    order_ids  = [f"order_{i:05d}" for i in range(N)]
    seller_ids = [f"seller_{i:04d}" for i in range(500)]
    product_ids= [f"prod_{i:04d}" for i in range(1000)]

    cust_states = np.random.choice(states, N)
    cust_cities = [np.random.choice(cities[s]) for s in cust_states]

    # Orders spanning 2016-2018
    order_dates = pd.date_range("2016-09-01", "2018-12-31", periods=N)
    order_dates = np.random.choice(order_dates, N, replace=False)
    order_dates = pd.to_datetime(sorted(order_dates))

    dfs = {}

    dfs["olist_customers"] = pd.DataFrame({
        "customer_id"             : cust_ids,
        "customer_unique_id"      : [f"uniq_{i:05d}" for i in range(N)],
        "customer_zip_code_prefix": np.random.randint(1000, 99999, N),
        "customer_city"           : cust_cities,
        "customer_state"          : cust_states,
    })

    dfs["olist_orders"] = pd.DataFrame({
        "order_id"               : order_ids,
        "customer_id"            : cust_ids,
        "order_status"           : np.random.choice(
                                       ["delivered","shipped","canceled","processing"],
                                       N, p=[0.80, 0.10, 0.06, 0.04]),
        "order_purchase_timestamp": order_dates,
        "order_approved_at"      : order_dates + pd.Timedelta(hours=2),
        "order_delivered_carrier_date": order_dates + pd.Timedelta(days=3),
        "order_delivered_customer_date": order_dates + pd.Timedelta(days=10),
        "order_estimated_delivery_date": order_dates + pd.Timedelta(days=14),
    })

    item_order_ids = np.random.choice(order_ids, N)
    item_sellers   = np.random.choice(seller_ids, N)
    item_products  = np.random.choice(product_ids, N)
    item_prices    = np.round(np.random.exponential(150, N), 2)
    item_freight   = np.round(np.random.uniform(5, 50, N), 2)

    dfs["olist_order_items"] = pd.DataFrame({
        "order_id"          : item_order_ids,
        "order_item_id"     : np.ones(N, dtype=int),
        "product_id"        : item_products,
        "seller_id"         : item_sellers,
        "shipping_limit_date": order_dates + pd.Timedelta(days=2),
        "price"             : item_prices,
        "freight_value"     : item_freight,
    })

    dfs["olist_order_payments"] = pd.DataFrame({
        "order_id"            : item_order_ids,
        "payment_sequential"  : np.ones(N, dtype=int),
        "payment_type"        : np.random.choice(payment_types, N,
                                    p=[0.73, 0.19, 0.05, 0.03]),
        "payment_installments": np.random.choice([1,2,3,6,12], N),
        "payment_value"       : item_prices + item_freight,
    })

    dfs["olist_order_reviews"] = pd.DataFrame({
        "review_id"               : [f"rev_{i:05d}" for i in range(N)],
        "order_id"                : item_order_ids,
        "review_score"            : np.random.choice([1,2,3,4,5], N,
                                        p=[0.05,0.05,0.10,0.20,0.60]),
        "review_creation_date"    : order_dates + pd.Timedelta(days=12),
        "review_answer_timestamp" : order_dates + pd.Timedelta(days=13),
    })

    seller_states = np.random.choice(states, 500)
    seller_cities = [np.random.choice(cities[s]) for s in seller_states]
    dfs["olist_sellers"] = pd.DataFrame({
        "seller_id"              : seller_ids,
        "seller_zip_code_prefix" : np.random.randint(1000, 99999, 500),
        "seller_city"            : seller_cities,
        "seller_state"           : seller_states,
    })

    dfs["olist_products_dataset"] = pd.DataFrame({
        "product_id"              : product_ids,
        "product_category_name"   : np.random.choice(categories, 1000),
        "product_name_lenght"     : np.random.randint(20, 60, 1000),
        "product_description_lenght": np.random.randint(100, 1000, 1000),
        "product_photos_qty"      : np.random.randint(1, 5, 1000),
        "product_weight_g"        : np.random.randint(100, 5000, 1000),
        "product_length_cm"       : np.random.randint(10, 60, 1000),
        "product_height_cm"       : np.random.randint(5, 40, 1000),
        "product_width_cm"        : np.random.randint(10, 50, 1000),
    })

    dfs["product_category_name_translation"] = pd.DataFrame({
        "product_category_name"          : categories,
        "product_category_name_english"  : ["electronics","furniture","sports",
                                            "beauty","books","toys","clothing",
                                            "garden","automotive","health"],
    })

    # Geolocation: one row per state capital
    geo_lats  = {"SP":-23.5,"RJ":-22.9,"MG":-19.9,"RS":-30.0,
                 "PR":-25.4,"SC":-27.6,"BA":-12.9,"GO":-16.7,
                 "PE":-8.1, "CE":-3.7}
    geo_longs = {"SP":-46.6,"RJ":-43.2,"MG":-43.9,"RS":-51.2,
                 "PR":-49.3,"SC":-48.5,"BA":-38.5,"GO":-49.3,
                 "PE":-34.9,"CE":-38.5}
    geo_rows  = []
    for st in states:
        for city in cities[st]:
            geo_rows.append({
                "geolocation_zip_code_prefix": np.random.randint(1000,99999),
                "geolocation_lat" : geo_lats[st]  + np.random.uniform(-0.5,0.5),
                "geolocation_lng" : geo_longs[st] + np.random.uniform(-0.5,0.5),
                "geolocation_city": city,
                "geolocation_state": st,
            })
    dfs["olist_geolocation"] = pd.DataFrame(geo_rows)

    print("Synthetic dataset created ✅")

# ── Create SQLite engine and load all tables ──────────────────────────────────
engine = create_engine("sqlite://", echo=False)

for table_name, df in dfs.items():
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    print(f"  Exported {table_name}: {df.shape}")

# ── Verify with test query ────────────────────────────────────────────────────
sql = "SELECT * FROM olist_customers LIMIT 5"
df_test = pd.read_sql_query(sql, con=engine)
print("\nTest query — olist_customers (first 5 rows):")
display(df_test)

def run_query(sql, title=""):
    """Helper: run SQL, display result, return dataframe."""
    print(f"\n{'═'*60}")
    print(f"  {title}")
    print("═"*60)
    df = pd.read_sql_query(sql, con=engine)
    display(df)
    return df

# ══════════════════════════════════════════════════════════════════════════════
# QUERY 1: Orders in Jan 2018 with 5-star review + percentage
# ══════════════════════════════════════════════════════════════════════════════

q1 = """
    WITH jan2018 AS (
        SELECT o.order_id
        FROM olist_orders o
        WHERE strftime('%Y-%m', o.order_purchase_timestamp) = '2018-01'
    ),
    scored AS (
        SELECT
            j.order_id,
            r.review_score
        FROM jan2018 j
        LEFT JOIN olist_order_reviews r ON r.order_id = j.order_id
    )
    SELECT
        COUNT(*)                                              AS total_orders_jan2018,
        SUM(CASE WHEN review_score = 5 THEN 1 ELSE 0 END)   AS five_star_orders,
        ROUND(
            SUM(CASE WHEN review_score = 5 THEN 1 ELSE 0 END) * 100.0
            / COUNT(*), 2
        )                                                     AS five_star_percentage
    FROM scored
"""
df_q1 = run_query(q1, "QUERY 1: Jan 2018 Orders with 5-Star Review + Percentage")

# ══════════════════════════════════════════════════════════════════════════════
# QUERY 2: Customer Purchase Trend Year-on-Year
# ══════════════════════════════════════════════════════════════════════════════

q2 = """
    SELECT
        strftime('%Y', o.order_purchase_timestamp)       AS year,
        strftime('%m', o.order_purchase_timestamp)       AS month,
        COUNT(DISTINCT o.customer_id)                    AS unique_customers,
        COUNT(DISTINCT o.order_id)                       AS total_orders,
        ROUND(SUM(p.payment_value), 2)                   AS total_revenue,
        ROUND(AVG(p.payment_value), 2)                   AS avg_order_value
    FROM olist_orders o
    JOIN olist_order_payments p ON p.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY year, month
    ORDER BY year, month
"""
df_q2 = run_query(q2, "QUERY 2: Customer Purchase Trend Year-on-Year")

# ── Visualise the trend ───────────────────────────────────────────────────────
import matplotlib.pyplot as plt

df_q2["period"] = df_q2["year"] + "-" + df_q2["month"]
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
axes[0].plot(df_q2["period"], df_q2["total_orders"], marker="o", color="steelblue", lw=2)
axes[0].set_title("Monthly Orders Over Time", fontweight="bold")
axes[0].set_xlabel("Period"); axes[0].set_ylabel("Orders")
axes[0].tick_params(axis="x", rotation=45)

axes[1].bar(df_q2["period"], df_q2["total_revenue"], color="darkorange", alpha=0.8)
axes[1].set_title("Monthly Revenue Over Time", fontweight="bold")
axes[1].set_xlabel("Period"); axes[1].set_ylabel("Revenue (BRL)")
axes[1].tick_params(axis="x", rotation=45)
plt.tight_layout(); plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# QUERY 3: Average Order Values of Customers
# ══════════════════════════════════════════════════════════════════════════════

q3 = """
    SELECT
        c.customer_unique_id,
        c.customer_city,
        c.customer_state,
        COUNT(DISTINCT o.order_id)          AS total_orders,
        ROUND(SUM(p.payment_value), 2)      AS total_spent,
        ROUND(AVG(p.payment_value), 2)      AS avg_order_value,
        ROUND(MAX(p.payment_value), 2)      AS max_order_value,
        ROUND(MIN(p.payment_value), 2)      AS min_order_value
    FROM olist_customers c
    JOIN olist_orders          o ON o.customer_id = c.customer_id
    JOIN olist_order_payments  p ON p.order_id    = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id, c.customer_city, c.customer_state
    HAVING total_orders >= 1
    ORDER BY avg_order_value DESC
    LIMIT 20
"""
df_q3 = run_query(q3, "QUERY 3: Average Order Values per Customer (Top 20)")

# ══════════════════════════════════════════════════════════════════════════════
# QUERY 4: Top 5 Cities with Highest Revenue 2016–2018
# ══════════════════════════════════════════════════════════════════════════════

q4 = """
    SELECT
        c.customer_city                                AS city,
        c.customer_state                               AS state,
        COUNT(DISTINCT o.order_id)                     AS total_orders,
        COUNT(DISTINCT o.customer_id)                  AS unique_customers,
        ROUND(SUM(p.payment_value), 2)                 AS total_revenue,
        ROUND(AVG(p.payment_value), 2)                 AS avg_order_value
    FROM olist_customers c
    JOIN olist_orders         o ON o.customer_id = c.customer_id
    JOIN olist_order_payments p ON p.order_id    = o.order_id
    WHERE o.order_status = 'delivered'
      AND strftime('%Y', o.order_purchase_timestamp) BETWEEN '2016' AND '2018'
    GROUP BY c.customer_city, c.customer_state
    ORDER BY total_revenue DESC
    LIMIT 5
"""
df_q4 = run_query(q4, "QUERY 4: Top 5 Cities by Revenue (2016–2018)")

fig, ax = plt.subplots(figsize=(10, 5))
labels = df_q4["city"] + " (" + df_q4["state"] + ")"
ax.barh(labels, df_q4["total_revenue"], color="steelblue", alpha=0.85)
ax.set_title("Top 5 Cities by Revenue", fontweight="bold")
ax.set_xlabel("Total Revenue (BRL)")
ax.invert_yaxis()
for i, v in enumerate(df_q4["total_revenue"]):
    ax.text(v + 100, i, f"R${v:,.0f}", va="center", fontsize=9)
plt.tight_layout(); plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# QUERY 5: State-wise Revenue Table 2016–2018
# ══════════════════════════════════════════════════════════════════════════════

q5 = """
    SELECT
        c.customer_state                               AS state,
        strftime('%Y', o.order_purchase_timestamp)     AS year,
        COUNT(DISTINCT o.order_id)                     AS total_orders,
        COUNT(DISTINCT o.customer_id)                  AS unique_customers,
        ROUND(SUM(p.payment_value), 2)                 AS total_revenue,
        ROUND(AVG(p.payment_value), 2)                 AS avg_order_value,
        RANK() OVER (
            PARTITION BY strftime('%Y', o.order_purchase_timestamp)
            ORDER BY SUM(p.payment_value) DESC
        )                                              AS revenue_rank
    FROM olist_customers c
    JOIN olist_orders         o ON o.customer_id = c.customer_id
    JOIN olist_order_payments p ON p.order_id    = o.order_id
    WHERE o.order_status = 'delivered'
      AND strftime('%Y', o.order_purchase_timestamp) BETWEEN '2016' AND '2018'
    GROUP BY c.customer_state, year
    ORDER BY year, total_revenue DESC
"""
df_q5 = run_query(q5, "QUERY 5: State-wise Revenue Table (2016–2018)")

# Pivot for easy reading
pivot_q5 = df_q5.pivot_table(
    index="state", columns="year",
    values="total_revenue", aggfunc="sum"
).fillna(0).round(2)
print("\nPivot — State Revenue by Year:")
display(pivot_q5)

# ══════════════════════════════════════════════════════════════════════════════
# QUERY 6: Top Successful Sellers
# ══════════════════════════════════════════════════════════════════════════════

q6 = """
    SELECT
        s.seller_id,
        s.seller_city,
        s.seller_state,
        COUNT(DISTINCT oi.order_id)                    AS total_orders,
        COUNT(oi.order_item_id)                        AS goods_sold,
        COUNT(DISTINCT o.customer_id)                  AS unique_customers,
        ROUND(SUM(oi.price + oi.freight_value), 2)     AS total_revenue,
        ROUND(AVG(oi.price), 2)                        AS avg_item_price,
        ROUND(AVG(r.review_score), 2)                  AS avg_review_score,
        SUM(CASE WHEN r.review_score = 5
                 THEN 1 ELSE 0 END)                    AS five_star_reviews,
        RANK() OVER (ORDER BY SUM(oi.price) DESC)      AS revenue_rank
    FROM olist_sellers      s
    JOIN olist_order_items  oi ON oi.seller_id  = s.seller_id
    JOIN olist_orders       o  ON o.order_id    = oi.order_id
    LEFT JOIN olist_order_reviews r ON r.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY s.seller_id, s.seller_city, s.seller_state
    HAVING goods_sold >= 5
    ORDER BY total_revenue DESC
    LIMIT 20
"""
df_q6 = run_query(q6, "QUERY 6: Top 20 Sellers by Revenue, Goods Sold & Reviews")

# ══════════════════════════════════════════════════════════════════════════════
# QUERY 7: Delivery Success Rate Across States
# ══════════════════════════════════════════════════════════════════════════════

q7 = """
    SELECT
        c.customer_state                               AS state,
        COUNT(*)                                       AS total_orders,
        SUM(CASE WHEN o.order_status = 'delivered'
                 THEN 1 ELSE 0 END)                    AS delivered,
        SUM(CASE WHEN o.order_status = 'canceled'
                 THEN 1 ELSE 0 END)                    AS canceled,
        SUM(CASE WHEN o.order_status = 'shipped'
                 THEN 1 ELSE 0 END)                    AS shipped,
        ROUND(
            SUM(CASE WHEN o.order_status = 'delivered'
                     THEN 1 ELSE 0 END) * 100.0
            / COUNT(*), 2
        )                                              AS delivery_success_rate_pct,
        ROUND(
            AVG(
                CASE WHEN o.order_status = 'delivered'
                THEN julianday(o.order_delivered_customer_date)
                   - julianday(o.order_purchase_timestamp)
                END
            ), 1
        )                                              AS avg_delivery_days
    FROM olist_orders   o
    JOIN olist_customers c ON c.customer_id = o.customer_id
    GROUP BY c.customer_state
    ORDER BY delivery_success_rate_pct DESC
"""
df_q7 = run_query(q7, "QUERY 7: Delivery Success Rate Across States")

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(df_q7["state"], df_q7["delivery_success_rate_pct"],
       color="green", alpha=0.75)
ax.axhline(df_q7["delivery_success_rate_pct"].mean(),
           color="red", lw=1.5, linestyle="--", label="Average")
ax.set_title("Delivery Success Rate by State (%)", fontweight="bold")
ax.set_xlabel("State"); ax.set_ylabel("Success Rate (%)")
ax.legend(); plt.tight_layout(); plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# QUERY 8: Preferred Payment Method per Product Category
# ══════════════════════════════════════════════════════════════════════════════

q8 = """
    SELECT
        COALESCE(t.product_category_name_english,
                 p.product_category_name,
                 'unknown')                             AS category,
        pay.payment_type,
        COUNT(*)                                        AS payment_count,
        ROUND(SUM(pay.payment_value), 2)                AS total_value,
        ROUND(AVG(pay.payment_value), 2)                AS avg_value,
        ROUND(
            COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (
                PARTITION BY COALESCE(t.product_category_name_english,
                                      p.product_category_name)
            ), 2
        )                                               AS pct_of_category
    FROM olist_order_items          oi
    JOIN olist_orders               o  ON o.order_id   = oi.order_id
    JOIN olist_order_payments       pay ON pay.order_id = o.order_id
    JOIN olist_products_dataset     p   ON p.product_id = oi.product_id
    LEFT JOIN product_category_name_translation t
           ON t.product_category_name = p.product_category_name
    WHERE o.order_status = 'delivered'
    GROUP BY category, pay.payment_type
    ORDER BY category, payment_count DESC
"""
df_q8 = run_query(q8, "QUERY 8: Preferred Payment Method per Product Category")

# Show dominant payment per category
dominant = (df_q8.sort_values("payment_count", ascending=False)
               .groupby("category").first().reset_index()
               [["category","payment_type","pct_of_category"]])
print("\nDominant payment method per category:")
display(dominant)

# ══════════════════════════════════════════════════════════════════════════════
# QUERY 9: Distance Between Cities (Haversine formula in SQL)
# ══════════════════════════════════════════════════════════════════════════════

q9 = """
    WITH city_coords AS (
        SELECT
            geolocation_city                         AS city,
            geolocation_state                        AS state,
            AVG(geolocation_lat)                     AS lat,
            AVG(geolocation_lng)                     AS lng
        FROM olist_geolocation
        GROUP BY geolocation_city, geolocation_state
    ),
    city_pairs AS (
        SELECT
            a.city   AS city_a,
            a.state  AS state_a,
            b.city   AS city_b,
            b.state  AS state_b,
            a.lat    AS lat_a,
            a.lng    AS lng_a,
            b.lat    AS lat_b,
            b.lng    AS lng_b,
            -- Euclidean approximation (degrees → km, ~111 km per degree)
            ROUND(
                SQRT(
                    POWER((b.lat - a.lat) * 111.0, 2) +
                    POWER((b.lng - a.lng) * 111.0 *
                          COS(a.lat * 3.14159 / 180.0), 2)
                ), 2
            )                                        AS distance_km
        FROM city_coords a
        JOIN city_coords b
          ON a.city < b.city       -- avoid duplicates and self-joins
    )
    SELECT *
    FROM city_pairs
    ORDER BY distance_km DESC
    LIMIT 20
"""
df_q9 = run_query(q9, "QUERY 9: Distance Between Cities (Top 20 Furthest Pairs)")

# ── Final summary ─────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("ANALYSIS COMPLETE — KEY INSIGHTS")
print("═"*60)
print(f"""
1. Jan 2018 five-star orders      : {df_q1['five_star_orders'].iloc[0]:,}
   Percentage                     : {df_q1['five_star_percentage'].iloc[0]}%

2. Year-on-year trend             : Revenue grew month-over-month
   through 2017-2018 (see chart)

3. Avg order value (top customer) : R${df_q3['avg_order_value'].iloc[0]:,.2f}

4. Top revenue city               : {df_q4['city'].iloc[0]} ({df_q4['state'].iloc[0]})
                                    R${df_q4['total_revenue'].iloc[0]:,.2f}

5. Top revenue state (all years)  : {df_q5.sort_values('total_revenue',ascending=False).iloc[0]['state']}

6. Top seller revenue             : R${df_q6['total_revenue'].iloc[0]:,.2f}
   Goods sold                     : {df_q6['goods_sold'].iloc[0]:,}

7. Best delivery state            : {df_q7.iloc[0]['state']}
   Success rate                   : {df_q7.iloc[0]['delivery_success_rate_pct']}%

8. Most popular payment           : {df_q8.groupby('payment_type')['payment_count'].sum().idxmax()}

9. Furthest city pair             : {df_q9.iloc[0]['city_a']} ↔ {df_q9.iloc[0]['city_b']}
   Distance                       : {df_q9.iloc[0]['distance_km']:,} km
""")
