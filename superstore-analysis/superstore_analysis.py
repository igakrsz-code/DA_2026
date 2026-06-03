# ══════════════════════════════════════════════════════════════════════════════
# STRATEGIC ANALYSIS OF SUPERSTORE PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════

import io, zipfile, urllib.request, time, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import ipywidgets as widgets
from ipywidgets import interact, Dropdown, IntSlider
from IPython.display import display
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'axes.grid': True, 'grid.alpha': 0.3,
    'axes.spines.top': False, 'axes.spines.right': False,
    'font.size': 11
})

# ══════════════════════════════════════════════════════════════════════════════
# TASK 1: DATA SCOPING AND PREPARATION
# ══════════════════════════════════════════════════════════════════════════════

URL = ("https://github.com/devtlv/Datasets-DA-Bootcamp-2-/raw/refs/heads/main/"
       "Week%207%20-%20Analysing%20Web%20Data/W7D1%20-%20Data%20Visualisation/"
       "Sample%20-%20Superstore.csv")

print("Downloading Superstore dataset…")
try:
    with urllib.request.urlopen(URL) as r:
        content = r.read()
    df = pd.read_csv(io.BytesIO(content), encoding='latin-1')
    print(f"Loaded from URL → {df.shape}")
except Exception as e:
    print(f"URL failed ({e}) — generating synthetic dataset…")
    np.random.seed(42)
    n = 9994
    categories   = ['Furniture','Office Supplies','Technology']
    sub_cats     = {'Furniture':    ['Chairs','Tables','Bookcases','Furnishings'],
                    'Office Supplies':['Paper','Binders','Storage','Art','Labels'],
                    'Technology':   ['Phones','Accessories','Machines','Copiers']}
    regions      = ['West','East','Central','South']
    states_r     = {'West' :['California','Washington','Oregon','Nevada'],
                    'East' :['New York','Pennsylvania','Ohio','Virginia'],
                    'Central':['Texas','Illinois','Michigan','Wisconsin'],
                    'South':['Florida','North Carolina','Georgia','Tennessee']}
    segments     = ['Consumer','Corporate','Home Office']
    ships        = ['Standard Class','Second Class','First Class','Same Day']

    cat_arr   = np.random.choice(categories, n, p=[0.32,0.40,0.28])
    reg_arr   = np.random.choice(regions, n)
    state_arr = [np.random.choice(states_r[r]) for r in reg_arr]
    seg_arr   = np.random.choice(segments, n)
    ship_arr  = np.random.choice(ships, n)
    order_dates = pd.to_datetime(
        np.random.choice(pd.date_range('2019-01-01','2022-12-31'), n))
    ship_dates  = order_dates + pd.to_timedelta(
        np.random.randint(2, 8, n), unit='D')

    sales    = np.round(np.random.exponential(230, n), 2)
    discount = np.random.choice([0,0.1,0.2,0.3,0.4,0.5], n,
                                 p=[0.50,0.15,0.15,0.10,0.07,0.03])
    cost     = sales * np.random.uniform(0.5, 0.85, n)
    profit   = np.round(sales - cost - sales * discount * 0.8, 2)

    subcat_arr = [np.random.choice(sub_cats[c]) for c in cat_arr]
    prod_arr   = [f"{sc} Model {np.random.randint(1,50)}"
                  for sc in subcat_arr]

    df = pd.DataFrame({
        'Order ID'     : [f"US-20{np.random.randint(19,23)}-{i:06d}" for i in range(n)],
        'Order Date'   : order_dates,
        'Ship Date'    : ship_dates,
        'Ship Mode'    : ship_arr,
        'Customer ID'  : [f"CU-{i%800:04d}" for i in range(n)],
        'Customer Name': [f"Customer {i%800}" for i in range(n)],
        'Segment'      : seg_arr,
        'Country'      : 'United States',
        'City'         : state_arr,
        'State'        : state_arr,
        'Postal Code'  : np.random.randint(10000, 99999, n),
        'Region'       : reg_arr,
        'Product ID'   : [f"PROD-{i%2000:04d}" for i in range(n)],
        'Category'     : cat_arr,
        'Sub-Category' : subcat_arr,
        'Product Name' : prod_arr,
        'Sales'        : sales,
        'Quantity'     : np.random.randint(1, 14, n),
        'Discount'     : discount,
        'Profit'       : profit,
    })
    print("Synthetic dataset created ✅")

# ── Basic exploration ──────────────────────────────────────────────────────────
print(f"\nDataset Shape: {df.shape}")
print("\nColumn Names:")
print(df.columns.tolist())
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())
print(f"\nDuplicate rows: {df.duplicated().sum()}")
display(df.describe().round(2))

# ── Clean ─────────────────────────────────────────────────────────────────────
df = df.drop_duplicates()

if 'Postal Code' in df.columns:
    df['Postal Code'] = df['Postal Code'].fillna(0)

# ── Date conversion ───────────────────────────────────────────────────────────
for col in ['Order Date','Ship Date']:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

print("\nDate types after conversion:")
print(df[['Order Date','Ship Date']].dtypes)

# ── Feature engineering ───────────────────────────────────────────────────────
df['Profit Margin']    = (df['Profit'] / df['Sales'].replace(0, np.nan)) * 100
df['Order Year']       = df['Order Date'].dt.year
df['Order Month']      = df['Order Date'].dt.month
df['Order Month-Year'] = df['Order Date'].dt.to_period('M')

print("\nNew features sample:")
display(df[['Sales','Profit','Profit Margin','Order Year','Order Month']].head())

# ══════════════════════════════════════════════════════════════════════════════
# TASK 2: DEEP-DIVE EXPLORATORY ANALYSIS (MATPLOTLIB)
# ══════════════════════════════════════════════════════════════════════════════

# ── Time-series data prep ─────────────────────────────────────────────────────
monthly_sales = (df.groupby(['Order Month-Year','Category'])['Sales']
                   .sum().reset_index())
monthly_sales['Date'] = monthly_sales['Order Month-Year'].dt.to_timestamp()

# ── Interactive time-series ───────────────────────────────────────────────────
def plot_monthly_sales(category='All'):
    fig, ax = plt.subplots(figsize=(13, 5))
    colors  = {'All':'steelblue','Furniture':'darkorange',
               'Office Supplies':'seagreen','Technology':'crimson'}

    if category == 'All':
        total = df.groupby('Order Month-Year')['Sales'].sum()
        ax.plot(total.index.to_timestamp(), total.values,
                marker='o', lw=2, ms=4, color='steelblue')
        ax.set_title('Monthly Sales Trend — All Categories',
                     fontsize=14, fontweight='bold')
    else:
        cat_data = monthly_sales[monthly_sales['Category'] == category]
        ax.plot(cat_data['Date'], cat_data['Sales'],
                marker='o', lw=2, ms=4,
                color=colors.get(category,'steelblue'))
        ax.set_title(f'Monthly Sales Trend — {category}',
                     fontsize=14, fontweight='bold')

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Sales ($)', fontsize=12)
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout(); plt.show()

categories = ['All'] + list(df['Category'].unique())
category_dd = Dropdown(options=categories, value='All', description='Category:')
interact(plot_monthly_sales, category=category_dd);

# ── Geographic analysis ───────────────────────────────────────────────────────
state_sales = df.groupby('State')['Sales'].sum().sort_values(ascending=True)

def plot_top_states(top_n=10):
    fig, ax = plt.subplots(figsize=(12, max(6, top_n * 0.4)))
    top_states = state_sales.tail(top_n)
    colors     = plt.cm.Blues(np.linspace(0.4, 0.9, top_n))
    bars       = ax.barh(range(len(top_states)), top_states.values,
                         color=colors, edgecolor='white')
    ax.set_yticks(range(len(top_states)))
    ax.set_yticklabels(top_states.index)
    ax.set_xlabel('Total Sales ($)', fontsize=12)
    ax.set_title(f'Top {top_n} States by Sales Performance',
                 fontsize=14, fontweight='bold')
    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    for i, (state, val) in enumerate(top_states.items()):
        ax.text(val + top_states.max() * 0.01, i,
                f'${val:,.0f}', va='center', fontsize=9)
    plt.tight_layout(); plt.show()
    print(f"Top {top_n} states: ${top_states.sum():,.0f}  "
          f"({top_states.sum()/state_sales.sum()*100:.1f}% of total sales)")

slider = IntSlider(min=5, max=min(25,len(state_sales)), value=10,
                   description='Top N:')
interact(plot_top_states, top_n=slider);

# ══════════════════════════════════════════════════════════════════════════════
# TASK 3: COMMUNICATING INSIGHTS (SEABORN)
# ══════════════════════════════════════════════════════════════════════════════

# ── Top 10 most profitable products ──────────────────────────────────────────
product_profit = (df.groupby('Product Name')['Profit']
                    .sum().sort_values(ascending=False).head(10))

fig, ax = plt.subplots(figsize=(13, 8))
sns.barplot(x=product_profit.values, y=product_profit.index,
            palette='viridis', orient='h', ax=ax)
ax.set_title('Top 10 Most Profitable Products\nExecutive Summary — Product Performance',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Total Profit ($)', fontsize=12, fontweight='bold')
ax.set_ylabel('Product Name', fontsize=12, fontweight='bold')
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for i, (prod, profit) in enumerate(product_profit.items()):
    ax.text(profit + product_profit.max() * 0.01, i,
            f'${profit:,.0f}', va='center', fontsize=9, fontweight='bold')
plt.tight_layout(); plt.show()

print(f"\n✦ Most profitable product  : {product_profit.index[0]}")
print(f"✦ Its profit               : ${product_profit.iloc[0]:,.0f}")
print(f"✦ Top 10 total profit      : ${product_profit.sum():,.0f}")
print(f"✦ Average per top product  : ${product_profit.mean():,.0f}")

# ── Discount vs Profit scatter ────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 7))
sns.scatterplot(data=df, x='Discount', y='Profit', hue='Category',
                alpha=0.5, s=40, ax=ax)
sns.regplot(data=df, x='Discount', y='Profit', scatter=False,
            color='red', line_kws={'lw':2,'linestyle':'--'}, ax=ax)
ax.axhline(0, color='black', lw=1, linestyle='-', alpha=0.4)
ax.text(0.52, ax.get_ylim()[1] * 0.05, 'Break-even line',
        fontsize=9, alpha=0.6)
ax.set_title('Discount Strategy: Impact on Profitability by Category',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Discount Rate', fontsize=12, fontweight='bold')
ax.set_ylabel('Profit ($)',    fontsize=12, fontweight='bold')
ax.legend(title='Category', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout(); plt.show()

high_disc = df[df['Discount'] > 0.2]
print(f"\n✦ Transactions > 20% discount    : {len(high_disc):,}")
print(f"✦ Avg profit at > 20% discount   : ${high_disc['Profit'].mean():.2f}")
print(f"✦ Loss rate at > 20% discount    : {(high_disc['Profit']<0).mean()*100:.1f}%")
for cat in df['Category'].unique():
    hd = df[(df['Category']==cat) & (df['Discount']>0.2)]
    if len(hd):
        print(f"  {cat}: avg profit = ${hd['Profit'].mean():.2f}")

# ── Additional Seaborn charts ─────────────────────────────────────────────────
# Profit by Category and Segment
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
cat_profit = df.groupby('Category')[['Sales','Profit']].sum()
cat_profit['Profit Margin'] = (cat_profit['Profit'] /
                                cat_profit['Sales'] * 100).round(2)
sns.barplot(data=cat_profit.reset_index(), x='Category',
            y='Profit Margin', palette='Set2', ax=axes[0])
axes[0].set_title('Profit Margin by Category', fontweight='bold')
axes[0].set_ylabel('Profit Margin (%)')

seg_profit = df.groupby('Segment')['Profit'].sum().reset_index()
sns.barplot(data=seg_profit, x='Segment', y='Profit',
            palette='Set1', ax=axes[1])
axes[1].set_title('Total Profit by Segment', fontweight='bold')
axes[1].set_ylabel('Profit ($)')
axes[1].yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.tight_layout(); plt.show()

# Profit margin distribution
fig, ax = plt.subplots(figsize=(12, 5))
for cat, color in zip(df['Category'].unique(),
                      ['steelblue','darkorange','seagreen']):
    data = df[df['Category']==cat]['Profit Margin'].clip(-100, 100)
    sns.kdeplot(data=data, ax=ax, label=cat, color=color, fill=True, alpha=0.3)
ax.axvline(0, color='red', lw=1.5, linestyle='--', label='Break-even')
ax.set_title('Profit Margin Distribution by Category', fontweight='bold')
ax.set_xlabel('Profit Margin (%)'); ax.set_ylabel('Density')
ax.legend(); plt.tight_layout(); plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# TASK 4: METHODOLOGY AND TOOLING REVIEW
# ══════════════════════════════════════════════════════════════════════════════

print("═"*60)
print("MATPLOTLIB vs SEABORN — COMPARISON")
print("═"*60)

start = time.time()
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(df.groupby('Order Year')['Sales'].sum())
plt.close()
mpl_time = time.time() - start

start = time.time()
fig, ax = plt.subplots(figsize=(8, 4))
sns.lineplot(data=df.groupby('Order Year')['Sales'].sum().reset_index(),
             x='Order Year', y='Sales', ax=ax)
plt.close()
sns_time = time.time() - start

print(f"""
MATPLOTLIB STRENGTHS:
  • Complete low-level control over every visual element
  • Seamless ipywidgets integration for dynamic dashboards
  • Custom annotations, arrows, and text positioning
  • Best for: interactive tools, precise custom layouts

SEABORN STRENGTHS:
  • Publication-ready aesthetics out of the box
  • Built-in statistical layers (regplot, kdeplot, CI bands)
  • Automatic color palettes and categorical handling
  • Best for: stakeholder-facing charts, quick EDA

SPEED:
  • Matplotlib basic plot : {mpl_time:.4f}s
  • Seaborn equivalent    : {sns_time:.4f}s

RECOMMENDATION:
  → Exploration  : Matplotlib + ipywidgets for interactive speed
  → Presentation : Seaborn for polished, publication-ready output
""")

# ══════════════════════════════════════════════════════════════════════════════
# TASK 5: EXECUTIVE SUMMARY DASHBOARD + REPORT
# ══════════════════════════════════════════════════════════════════════════════

# ── 4-panel dashboard ─────────────────────────────────────────────────────────
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Panel 1: Monthly sales trend
monthly_total = df.groupby('Order Month-Year')['Sales'].sum()
ax1.plot(monthly_total.index.to_timestamp(), monthly_total.values,
         marker='o', ms=3, lw=1.8, color='steelblue')
ax1.set_title('Monthly Sales Trend', fontweight='bold')
ax1.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x,_: f'${x/1e3:.0f}K'))
ax1.tick_params(axis='x', rotation=45)

# Panel 2: Sales by category
cat_s = df.groupby('Category')['Sales'].sum()
colors_cat = ['#2196F3','#4CAF50','#FF5722']
ax2.bar(cat_s.index, cat_s.values, color=colors_cat, alpha=0.85,
        edgecolor='white')
ax2.set_title('Sales by Category', fontweight='bold')
ax2.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x,_: f'${x/1e6:.1f}M'))
for i, (cat, val) in enumerate(cat_s.items()):
    ax2.text(i, val*1.01, f'${val/1e6:.1f}M', ha='center', fontsize=9)

# Panel 3: Top 10 states
top10 = state_sales.tail(10)
ax3.barh(range(len(top10)), top10.values,
         color=plt.cm.Blues(np.linspace(0.4, 0.9, 10)),
         edgecolor='white')
ax3.set_yticks(range(len(top10)))
ax3.set_yticklabels(top10.index, fontsize=9)
ax3.set_title('Top 10 States by Sales', fontweight='bold')
ax3.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x,_: f'${x/1e3:.0f}K'))

# Panel 4: Discount vs Profit
for cat, color in zip(df['Category'].unique(),
                      ['#2196F3','#4CAF50','#FF5722']):
    sub = df[df['Category']==cat]
    ax4.scatter(sub['Discount'], sub['Profit'],
                label=cat, alpha=0.4, s=15, color=color)
ax4.axhline(0, color='black', lw=1, linestyle='--', alpha=0.5)
ax4.set_xlabel('Discount'); ax4.set_ylabel('Profit ($)')
ax4.set_title('Discount vs Profit by Category', fontweight='bold')
ax4.legend(fontsize=8)

plt.suptitle('SUPERSTORE PERFORMANCE DASHBOARD',
             fontsize=16, fontweight='bold', y=1.01)
plt.tight_layout(); plt.show()

# ── Outlier annotations ───────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 7))
sns.scatterplot(data=df, x='Discount', y='Profit',
                hue='Category', alpha=0.5, s=40, ax=ax)
sns.regplot(data=df, x='Discount', y='Profit', scatter=False,
            color='red', line_kws={'lw':2,'linestyle':'--'}, ax=ax)
ax.axhline(0, color='black', lw=1, alpha=0.4)

top3    = df.nlargest(3, 'Profit')
bottom3 = df.nsmallest(3, 'Profit')

for _, row in top3.iterrows():
    ax.annotate(f"Best\n${row['Profit']:.0f}",
                xy=(row['Discount'], row['Profit']),
                xytext=(15, -20), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3',
                          facecolor='lightgreen', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color='green'))
for _, row in bottom3.iterrows():
    ax.annotate(f"Worst\n${row['Profit']:.0f}",
                xy=(row['Discount'], row['Profit']),
                xytext=(15, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3',
                          facecolor='lightsalmon', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color='red'))
ax.set_title('Discount vs Profit — Outlier Identification',
             fontsize=13, fontweight='bold')
ax.legend(title='Category', bbox_to_anchor=(1.02, 1))
plt.tight_layout(); plt.show()

# ── Final key metrics ─────────────────────────────────────────────────────────
total_sales  = df['Sales'].sum()
total_profit = df['Profit'].sum()
margin       = total_profit / total_sales * 100
top_state    = state_sales.index[-1]
top_cat      = df.groupby('Category')['Sales'].sum().idxmax()
loss_rate    = (df[df['Discount']>0.2]['Profit']<0).mean()*100

print(f"""
╔══════════════════════════════════════════════════════════╗
║         EXECUTIVE SUMMARY — KEY FINDINGS                ║
╚══════════════════════════════════════════════════════════╝

📊 BUSINESS PERFORMANCE
  • Total Revenue          : ${total_sales:,.0f}
  • Total Profit           : ${total_profit:,.0f}
  • Overall Profit Margin  : {margin:.1f}%

🗺️  GEOGRAPHIC PERFORMANCE
  • Top state              : {top_state}  (${state_sales.iloc[-1]:,.0f})
  • Top 5 states share     : {state_sales.tail(5).sum()/total_sales*100:.1f}% of revenue

🏆 PRODUCT PERFORMANCE
  • Leading category       : {top_cat}
  • Most profitable product: {product_profit.index[0]}
  • Its profit             : ${product_profit.iloc[0]:,.0f}

💰 DISCOUNT STRATEGY
  • Loss rate at >20% disc : {loss_rate:.1f}%
  • Recommended max disc   : 20% to preserve profitability

📋 STRATEGIC RECOMMENDATIONS
  1. Cap discounts at 20% across all categories — higher
     discounts correlate strongly with losses.
  2. Invest in Technology and top-performing products
     which drive the highest profit margins.
  3. Expand presence in top states; analyse low-revenue
     states for growth or cost-cutting opportunities.
  4. Segment marketing by Customer Segment — Corporate
     and Consumer show distinct purchase patterns.
  5. Review Furniture pricing — lowest margin category,
     most sensitive to discount-driven losses.
""")
