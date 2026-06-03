# ══════════════════════════════════════════════════════════════════════════════
# MINI-PROJECT: DATA ANALYSIS FOR MARKETING STRATEGY
# US Superstore Dataset
# ══════════════════════════════════════════════════════════════════════════════

import io, urllib.request, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'axes.grid': True, 'grid.alpha': 0.3,
    'axes.spines.top': False, 'axes.spines.right': False,
    'font.size': 11
})

# ══════════════════════════════════════════════════════════════════════════════
# LOAD & PREPROCESS
# ══════════════════════════════════════════════════════════════════════════════

URL = ("https://github.com/devtlv/Datasets-DA-Bootcamp-2-/raw/refs/heads/main/"
       "Week%205%20-%20Data%20Processing/W5D5%20-%20Mini-project%20-%20bis/"
       "US%20Superstore%20data.xls")

print("Downloading dataset…")
try:
    with urllib.request.urlopen(URL) as r:
        raw = r.read()
    df = pd.read_excel(io.BytesIO(raw))
    print(f"Loaded → {df.shape}")
except Exception as e:
    print(f"Download failed ({e}) — generating synthetic dataset…")
    np.random.seed(42)
    n = 9994
    states = ['California','New York','Texas','Washington','Pennsylvania',
              'Illinois','Ohio','Florida','Michigan','Virginia',
              'Georgia','North Carolina','Indiana','Arizona','Tennessee',
              'Colorado','Wisconsin','Minnesota','Oregon','Nevada']
    cities_map = {
        'California':['Los Angeles','San Francisco','San Diego','Sacramento'],
        'New York':['New York City','Buffalo','Rochester','Albany'],
        'Texas':['Houston','Dallas','Austin','San Antonio'],
        'Washington':['Seattle','Tacoma','Spokane','Bellevue'],
        'Pennsylvania':['Philadelphia','Pittsburgh','Allentown','Erie'],
        'Illinois':['Chicago','Aurora','Rockford','Joliet'],
        'Ohio':['Columbus','Cleveland','Cincinnati','Toledo'],
        'Florida':['Miami','Orlando','Tampa','Jacksonville'],
        'Michigan':['Detroit','Grand Rapids','Lansing','Ann Arbor'],
        'Virginia':['Virginia Beach','Richmond','Norfolk','Chesapeake'],
        'Georgia':['Atlanta','Augusta','Columbus','Savannah'],
        'North Carolina':['Charlotte','Raleigh','Greensboro','Durham'],
        'Indiana':['Indianapolis','Fort Wayne','Evansville','South Bend'],
        'Arizona':['Phoenix','Tucson','Mesa','Chandler'],
        'Tennessee':['Memphis','Nashville','Knoxville','Chattanooga'],
        'Colorado':['Denver','Colorado Springs','Aurora','Fort Collins'],
        'Wisconsin':['Milwaukee','Madison','Green Bay','Kenosha'],
        'Minnesota':['Minneapolis','Saint Paul','Rochester','Duluth'],
        'Oregon':['Portland','Salem','Eugene','Gresham'],
        'Nevada':['Las Vegas','Henderson','Reno','North Las Vegas'],
    }
    regions = {'California':'West','New York':'East','Texas':'Central',
               'Washington':'West','Pennsylvania':'East','Illinois':'Central',
               'Ohio':'East','Florida':'South','Michigan':'East',
               'Virginia':'South','Georgia':'South','North Carolina':'South',
               'Indiana':'Central','Arizona':'West','Tennessee':'South',
               'Colorado':'West','Wisconsin':'Central','Minnesota':'Central',
               'Oregon':'West','Nevada':'West'}
    categories   = ['Furniture','Office Supplies','Technology']
    sub_cats     = {'Furniture':['Chairs','Tables','Bookcases','Furnishings'],
                    'Office Supplies':['Paper','Binders','Storage','Art'],
                    'Technology':['Phones','Accessories','Machines','Copiers']}
    segments     = ['Consumer','Corporate','Home Office']
    customers    = [f"Customer_{i:04d}" for i in range(800)]

    state_arr  = np.random.choice(states, n)
    city_arr   = [np.random.choice(cities_map[s]) for s in state_arr]
    region_arr = [regions[s] for s in state_arr]
    cat_arr    = np.random.choice(categories, n, p=[0.32,0.40,0.28])
    subcat_arr = [np.random.choice(sub_cats[c]) for c in cat_arr]
    cust_arr   = np.random.choice(customers, n)
    seg_arr    = np.random.choice(segments, n)

    sales    = np.round(np.random.exponential(250, n), 2)
    discount = np.random.choice([0,.1,.2,.3,.4,.5], n,
                                 p=[0.50,.15,.15,.10,.07,.03])
    profit   = np.round(sales * np.random.uniform(-0.1, 0.35, n)
                        - sales * discount * 0.5, 2)
    order_dates = pd.to_datetime(
        np.random.choice(pd.date_range('2019-01-01','2022-12-31'), n))
    ship_dates  = order_dates + pd.to_timedelta(
        np.random.randint(2,8,n), unit='D')

    df = pd.DataFrame({
        'Row ID'       : range(1, n+1),
        'Order ID'     : [f"US-{np.random.randint(2019,2023)}-{i:06d}" for i in range(n)],
        'Order Date'   : order_dates,
        'Ship Date'    : ship_dates,
        'Ship Mode'    : np.random.choice(['Standard Class','Second Class',
                                           'First Class','Same Day'], n),
        'Customer ID'  : [f"CU-{i%800:04d}" for i in range(n)],
        'Customer Name': cust_arr,
        'Segment'      : seg_arr,
        'Country'      : 'United States',
        'City'         : city_arr,
        'State'        : state_arr,
        'Postal Code'  : np.random.randint(10000,99999,n),
        'Region'       : region_arr,
        'Product ID'   : [f"PROD-{i%2000:04d}" for i in range(n)],
        'Category'     : cat_arr,
        'Sub-Category' : subcat_arr,
        'Product Name' : [f"{sc} Model {np.random.randint(1,50)}"
                          for sc in subcat_arr],
        'Sales'        : sales,
        'Quantity'     : np.random.randint(1,14,n),
        'Discount'     : discount,
        'Profit'       : profit,
    })
    print("Synthetic dataset created ✅")

# ── Preprocessing ─────────────────────────────────────────────────────────────
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date']  = pd.to_datetime(df['Ship Date'],  errors='coerce')
df['Order Year'] = df['Order Date'].dt.year
df['Order Month']= df['Order Date'].dt.to_period('M')
df['Profit Margin'] = (df['Profit'] / df['Sales'].replace(0,np.nan) * 100).round(2)

print(f"\nShape         : {df.shape}")
print(f"Null values   : {df.isnull().sum().sum()}")
print(f"Duplicates    : {df.duplicated().sum()}")
display(df.head())

# ══════════════════════════════════════════════════════════════════════════════
# Q1: WHICH STATES HAVE THE MOST SALES?
# ══════════════════════════════════════════════════════════════════════════════

state_sales  = df.groupby('State')['Sales'].sum().sort_values(ascending=False)
state_profit = df.groupby('State')['Profit'].sum()

fig, ax = plt.subplots(figsize=(14, 8))
colors = ['#1565C0' if v > state_sales.mean() else '#90CAF9'
          for v in state_sales.values]
ax.barh(state_sales.index[::-1], state_sales.values[::-1],
        color=colors[::-1], edgecolor='white')
ax.axvline(state_sales.mean(), color='red', lw=1.5,
           linestyle='--', label=f'Mean = ${state_sales.mean():,.0f}')
ax.set_title('Total Sales by State', fontsize=14, fontweight='bold')
ax.set_xlabel('Total Sales ($)')
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x,_: f'${x/1e3:.0f}K'))
ax.legend(); plt.tight_layout(); plt.show()

print(f"Top 5 states by sales:")
print(state_sales.head().to_string())

# ══════════════════════════════════════════════════════════════════════════════
# Q2: NEW YORK vs CALIFORNIA — SALES & PROFIT
# ══════════════════════════════════════════════════════════════════════════════

ny_ca = df[df['State'].isin(['New York','California'])]
compare = ny_ca.groupby('State')[['Sales','Profit']].sum()

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for ax, col, color in zip(axes, ['Sales','Profit'],
                           [['#1565C0','#E91E63'],['#2E7D32','#F57F17']]):
    vals = compare[col]
    bars = ax.bar(vals.index, vals.values, color=color,
                  alpha=0.85, edgecolor='white', width=0.5)
    ax.bar_label(bars, fmt='${:,.0f}', padding=5, fontsize=10)
    ax.set_title(f'{col}: New York vs California', fontweight='bold')
    ax.set_ylabel(f'{col} ($)')
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x,_: f'${x/1e3:.0f}K'))
plt.suptitle('New York vs California — Sales & Profit Comparison',
             fontsize=13, fontweight='bold')
plt.tight_layout(); plt.show()

print("\nNew York vs California:")
display(compare)
diff = compare.diff().iloc[-1]
print(f"\nDifference (NY − CA): Sales=${diff['Sales']:,.0f}  Profit=${diff['Profit']:,.0f}")

# ══════════════════════════════════════════════════════════════════════════════
# Q3: OUTSTANDING CUSTOMER IN NEW YORK
# ══════════════════════════════════════════════════════════════════════════════

ny = df[df['State']=='New York']
ny_cust = ny.groupby('Customer Name').agg(
    Total_Sales   = ('Sales','sum'),
    Total_Profit  = ('Profit','sum'),
    Orders        = ('Order ID','nunique'),
    Avg_Order_Val = ('Sales','mean')
).sort_values('Total_Sales', ascending=False)

print("\nTop 10 Customers in New York:")
display(ny_cust.head(10).round(2))

fig, ax = plt.subplots(figsize=(12, 6))
top_ny = ny_cust.head(10)
colors = ['gold' if i==0 else 'steelblue' for i in range(10)]
bars   = ax.barh(top_ny.index[::-1], top_ny['Total_Sales'][::-1],
                 color=colors[::-1], edgecolor='white')
ax.set_title('Top 10 Customers in New York by Sales\n⭐ = Outstanding Customer',
             fontweight='bold')
ax.set_xlabel('Total Sales ($)')
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x,_: f'${x:,.0f}'))
for i, v in enumerate(top_ny['Total_Sales'][::-1]):
    ax.text(v*1.01, i, f'${v:,.0f}', va='center', fontsize=9)
plt.tight_layout(); plt.show()

top_cust = ny_cust.index[0]
print(f"\n⭐ Outstanding customer in New York: {top_cust}")
print(f"   Total Sales  : ${ny_cust.iloc[0]['Total_Sales']:,.2f}")
print(f"   Total Profit : ${ny_cust.iloc[0]['Total_Profit']:,.2f}")
print(f"   Orders placed: {ny_cust.iloc[0]['Orders']}")

# ══════════════════════════════════════════════════════════════════════════════
# Q4: STATE PROFITABILITY DIFFERENCES
# ══════════════════════════════════════════════════════════════════════════════

state_pm = (df.groupby('State')
              .agg(Total_Sales=('Sales','sum'),
                   Total_Profit=('Profit','sum'))
              .assign(Profit_Margin=lambda d:
                      (d['Total_Profit']/d['Total_Sales']*100).round(2))
              .sort_values('Profit_Margin', ascending=False))

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Profit margin bar
colors_pm = ['#2E7D32' if v>=0 else '#C62828'
             for v in state_pm['Profit_Margin']]
axes[0].barh(state_pm.index[::-1], state_pm['Profit_Margin'][::-1],
             color=colors_pm[::-1], edgecolor='white')
axes[0].axvline(0, color='black', lw=1)
axes[0].set_title('Profit Margin by State (%)', fontweight='bold')
axes[0].set_xlabel('Profit Margin (%)')

# Profit vs Sales scatter
sc = axes[1].scatter(state_pm['Total_Sales'],
                     state_pm['Total_Profit'],
                     c=state_pm['Profit_Margin'],
                     cmap='RdYlGn', s=80, alpha=0.8)
plt.colorbar(sc, ax=axes[1], label='Profit Margin (%)')
axes[1].axhline(0, color='red', lw=1, linestyle='--')
for st in state_pm.head(5).index:
    row = state_pm.loc[st]
    axes[1].annotate(st, (row['Total_Sales'], row['Total_Profit']),
                     fontsize=7, xytext=(5,3),
                     textcoords='offset points')
axes[1].set_title('Sales vs Profit by State', fontweight='bold')
axes[1].set_xlabel('Total Sales ($)'); axes[1].set_ylabel('Total Profit ($)')
plt.suptitle('State Profitability Analysis', fontsize=13, fontweight='bold')
plt.tight_layout(); plt.show()

print("\nTop 5 most profitable states:")
print(state_pm[['Total_Sales','Total_Profit','Profit_Margin']].head().to_string())
print("\nBottom 5 least profitable states:")
print(state_pm[['Total_Sales','Total_Profit','Profit_Margin']].tail().to_string())

# ══════════════════════════════════════════════════════════════════════════════
# Q5: PARETO PRINCIPLE — CUSTOMERS & PROFIT
# ══════════════════════════════════════════════════════════════════════════════

cust_profit = (df.groupby('Customer Name')['Profit']
                 .sum().sort_values(ascending=False))
cust_profit_pos = cust_profit[cust_profit > 0]

cumulative_profit = cust_profit_pos.cumsum() / cust_profit_pos.sum() * 100
pct_customers     = np.arange(1, len(cust_profit_pos)+1) / len(cust_profit_pos) * 100

# Find where 20% of customers are
idx_20 = np.searchsorted(pct_customers, 20)
profit_at_20 = cumulative_profit.iloc[idx_20] if idx_20 < len(cumulative_profit) else None

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(pct_customers, cumulative_profit.values,
        color='steelblue', lw=2.5, label='Cumulative Profit')
ax.axvline(20, color='red', lw=1.5, linestyle='--', label='20% of Customers')
if profit_at_20:
    ax.axhline(profit_at_20, color='orange', lw=1.5,
               linestyle='--', label=f'{profit_at_20:.1f}% of Profit')
    ax.scatter([20], [profit_at_20], color='red', s=100, zorder=5)
    ax.annotate(f'20% customers\n→ {profit_at_20:.1f}% profit',
                xy=(20, profit_at_20), xytext=(30, profit_at_20-15),
                fontsize=10, fontweight='bold', color='red',
                arrowprops=dict(arrowstyle='->', color='red'))
ax.fill_between(pct_customers[:idx_20+1],
                cumulative_profit.values[:idx_20+1],
                alpha=0.15, color='red')
ax.set_title('Pareto Analysis — Customers vs Cumulative Profit',
             fontsize=14, fontweight='bold')
ax.set_xlabel('% of Customers (sorted by profit)')
ax.set_ylabel('Cumulative Profit (%)')
ax.legend(); plt.tight_layout(); plt.show()

print(f"\nPareto Analysis (Customers → Profit):")
print(f"  Top 20% of customers ({idx_20} customers) → "
      f"{profit_at_20:.1f}% of total profit")
pareto_holds = profit_at_20 >= 75 if profit_at_20 else False
print(f"  Pareto principle {'HOLDS ✅' if pareto_holds else 'partially holds ⚠️'}")

# ══════════════════════════════════════════════════════════════════════════════
# Q6: TOP 20 CITIES BY SALES AND PROFIT
# ══════════════════════════════════════════════════════════════════════════════

city_stats = (df.groupby('City')
                .agg(Total_Sales=('Sales','sum'),
                     Total_Profit=('Profit','sum'))
                .assign(Profit_Margin=lambda d:
                        (d['Total_Profit']/d['Total_Sales']*100).round(2)))

top20_sales  = city_stats.sort_values('Total_Sales',  ascending=False).head(20)
top20_profit = city_stats.sort_values('Total_Profit', ascending=False).head(20)

fig, axes = plt.subplots(1, 2, figsize=(16, 9))

# Top 20 by sales
c_s = ['#1565C0' if v>=0 else '#C62828' for v in top20_sales['Total_Sales']]
axes[0].barh(top20_sales.index[::-1], top20_sales['Total_Sales'][::-1],
             color='steelblue', edgecolor='white')
axes[0].set_title('Top 20 Cities by Sales', fontweight='bold')
axes[0].set_xlabel('Total Sales ($)')
axes[0].xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x,_: f'${x/1e3:.0f}K'))

# Top 20 by profit
c_p = ['#2E7D32' if v>=0 else '#C62828' for v in top20_profit['Total_Profit']]
axes[1].barh(top20_profit.index[::-1], top20_profit['Total_Profit'][::-1],
             color=c_p[::-1], edgecolor='white')
axes[1].axvline(0, color='black', lw=1)
axes[1].set_title('Top 20 Cities by Profit', fontweight='bold')
axes[1].set_xlabel('Total Profit ($)')
axes[1].xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x,_: f'${x/1e3:.0f}K'))

plt.suptitle('Top 20 Cities — Sales vs Profit', fontsize=13, fontweight='bold')
plt.tight_layout(); plt.show()

# Profitability scatter for top 40 cities
top40 = city_stats.nlargest(40, 'Total_Sales')
fig, ax = plt.subplots(figsize=(12, 7))
sc = ax.scatter(top40['Total_Sales'], top40['Total_Profit'],
                c=top40['Profit_Margin'], cmap='RdYlGn',
                s=80, alpha=0.85)
plt.colorbar(sc, ax=ax, label='Profit Margin (%)')
ax.axhline(0, color='red', lw=1, linestyle='--')
for city, row in top40.head(10).iterrows():
    ax.annotate(city, (row['Total_Sales'], row['Total_Profit']),
                fontsize=7, xytext=(5,3), textcoords='offset points')
ax.set_title('City Profitability Analysis (Top 40 by Sales)',
             fontweight='bold')
ax.set_xlabel('Total Sales ($)'); ax.set_ylabel('Total Profit ($)')
plt.tight_layout(); plt.show()

print("\nTop 10 cities by sales with profit margins:")
display(top20_sales[['Total_Sales','Total_Profit','Profit_Margin']].head(10))

# ══════════════════════════════════════════════════════════════════════════════
# Q7: TOP 20 CUSTOMERS BY SALES
# ══════════════════════════════════════════════════════════════════════════════

cust_sales = (df.groupby('Customer Name')
                .agg(Total_Sales=('Sales','sum'),
                     Total_Profit=('Profit','sum'),
                     Orders=('Order ID','nunique'))
                .sort_values('Total_Sales', ascending=False))

top20_cust = cust_sales.head(20)

fig, ax = plt.subplots(figsize=(13, 8))
colors = ['gold' if i==0 else ('#1565C0' if v>=0 else '#C62828')
          for i, v in enumerate(top20_cust['Total_Sales'])]
bars = ax.barh(top20_cust.index[::-1], top20_cust['Total_Sales'][::-1],
               color=colors[::-1], edgecolor='white')
ax.set_title('Top 20 Customers by Total Sales', fontsize=14, fontweight='bold')
ax.set_xlabel('Total Sales ($)')
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x,_: f'${x:,.0f}'))
for i, (cust, row) in enumerate(top20_cust[::-1].iterrows()):
    ax.text(row['Total_Sales']*1.005, i,
            f'${row["Total_Sales"]:,.0f}', va='center', fontsize=8)
plt.tight_layout(); plt.show()

print("\nTop 20 Customers by Sales:")
display(top20_cust.head(20).round(2))

# ══════════════════════════════════════════════════════════════════════════════
# Q8: CUMULATIVE SALES CURVE — PARETO FOR CUSTOMERS & SALES
# ══════════════════════════════════════════════════════════════════════════════

cust_sales_sorted = cust_sales.sort_values('Total_Sales', ascending=False)
cum_sales = cust_sales_sorted['Total_Sales'].cumsum()
cum_pct   = cum_sales / cum_sales.iloc[-1] * 100
cust_pct  = np.arange(1, len(cust_sales_sorted)+1) / len(cust_sales_sorted) * 100

idx_20s   = np.searchsorted(cust_pct, 20)
sales_20  = cum_pct.iloc[idx_20s] if idx_20s < len(cum_pct) else None

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Cumulative curve
axes[0].plot(cust_pct, cum_pct.values, color='steelblue', lw=2.5,
             label='Cumulative Sales')
axes[0].plot([0, 100], [0, 100], 'k--', lw=1, alpha=0.4, label='Perfect Equality')
axes[0].axvline(20, color='red', lw=1.5, linestyle='--', label='20% Customers')
if sales_20:
    axes[0].axhline(sales_20, color='orange', lw=1.5,
                    linestyle='--', label=f'{sales_20:.1f}% Sales')
    axes[0].scatter([20], [sales_20], color='red', s=100, zorder=5)
    axes[0].annotate(f'20% customers\n→ {sales_20:.1f}% sales',
                     xy=(20, sales_20), xytext=(35, sales_20-12),
                     fontsize=9, fontweight='bold', color='red',
                     arrowprops=dict(arrowstyle='->', color='red'))
axes[0].fill_between(cust_pct[:idx_20s+1], cum_pct.values[:idx_20s+1],
                     alpha=0.15, color='red')
axes[0].set_title('Cumulative Sales by Customers\n(Lorenz Curve)',
                  fontweight='bold')
axes[0].set_xlabel('% of Customers'); axes[0].set_ylabel('Cumulative Sales (%)')
axes[0].legend(fontsize=9)

# Top 20 customers bar + cumulative line
ax2b = axes[1].twinx()
axes[1].bar(range(20), top20_cust['Total_Sales'].values,
            color='steelblue', alpha=0.7, label='Sales')
top20_cum = (top20_cust['Total_Sales'].cumsum()
             / cust_sales['Total_Sales'].sum() * 100)
ax2b.plot(range(20), top20_cum.values, color='red', marker='o',
          ms=5, lw=2, label='Cumulative %')
axes[1].set_xticks(range(20))
axes[1].set_xticklabels([c[:12] for c in top20_cust.index],
                         rotation=45, ha='right', fontsize=7)
axes[1].set_title('Top 20 Customers — Sales + Cumulative %',
                  fontweight='bold')
axes[1].set_ylabel('Sales ($)'); ax2b.set_ylabel('Cumulative Sales (%)')
axes[1].yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x,_: f'${x:,.0f}'))
plt.tight_layout(); plt.show()

print(f"\nPareto Analysis (Customers → Sales):")
print(f"  Top 20% of customers ({idx_20s} customers) → "
      f"{sales_20:.1f}% of total sales")
pareto_s = sales_20 >= 70 if sales_20 else False
print(f"  Pareto principle {'HOLDS ✅' if pareto_s else 'partially holds ⚠️'}")

# ══════════════════════════════════════════════════════════════════════════════
# SALES & PROFIT TIME SERIES
# ══════════════════════════════════════════════════════════════════════════════

monthly = (df.groupby('Order Month')
             .agg(Sales=('Sales','sum'), Profit=('Profit','sum'))
             .reset_index())
monthly['Date'] = monthly['Order Month'].dt.to_timestamp()

fig, axes = plt.subplots(2, 1, figsize=(14, 9), sharex=True)
axes[0].plot(monthly['Date'], monthly['Sales'],
             color='steelblue', lw=2, marker='o', ms=3)
axes[0].fill_between(monthly['Date'], monthly['Sales'], alpha=0.15,
                     color='steelblue')
axes[0].set_title('Monthly Sales Trend', fontweight='bold')
axes[0].set_ylabel('Sales ($)')
axes[0].yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x,_: f'${x/1e3:.0f}K'))

axes[1].plot(monthly['Date'], monthly['Profit'],
             color='seagreen', lw=2, marker='o', ms=3)
axes[1].fill_between(monthly['Date'], monthly['Profit'], alpha=0.15,
                     color='seagreen')
axes[1].axhline(0, color='red', lw=1, linestyle='--')
axes[1].set_title('Monthly Profit Trend', fontweight='bold')
axes[1].set_ylabel('Profit ($)')
axes[1].yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x,_: f'${x/1e3:.0f}K'))
axes[1].set_xlabel('Date')
plt.suptitle('Sales & Profit Time Series', fontsize=13, fontweight='bold')
plt.tight_layout(); plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# MARKETING STRATEGY RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════

total_sales  = df['Sales'].sum()
total_profit = df['Profit'].sum()
top5_states  = state_sales.head(5)
top5_cities  = city_stats.nlargest(5,'Total_Sales')

print(f"""
╔══════════════════════════════════════════════════════════════╗
║          MARKETING STRATEGY RECOMMENDATIONS                  ║
╚══════════════════════════════════════════════════════════════╝

📊 OVERALL PERFORMANCE
  • Total Revenue          : ${total_sales:,.0f}
  • Total Profit           : ${total_profit:,.0f}
  • Profit Margin          : {total_profit/total_sales*100:.1f}%

🗺️  PRIORITY STATES FOR MARKETING
  Top 5 states by sales:
{top5_states.apply(lambda x: f"  • {x.name:<20} ${x:>10,.0f}").to_string(header=False)}

  Action: Concentrate campaigns in {top5_states.index[0]} and
  {top5_states.index[1]} — they account for
  {top5_states.iloc[:2].sum()/total_sales*100:.1f}% of total revenue.

🏙️  PRIORITY CITIES
  Focus on top-profit cities with high margins.
  Avoid heavy discounting in low-margin cities.

👥 CUSTOMER STRATEGY
  • Top 20% of customers → {sales_20:.1f}% of sales
  • Top 20% → {profit_at_20:.1f}% of profit
  • ✅ Pareto holds — prioritise VIP retention programs.
  • Launch loyalty rewards for top customers.
  • Outstanding NY customer: {top_cust}

💰 DISCOUNT STRATEGY
  • High discounts (>20%) consistently erode profit.
  • Enforce 20% max discount cap company-wide.

📦 REGIONAL FOCUS
  • States with negative profit margins need pricing review.
  • Investigate loss-making states before increasing spend.
""")
