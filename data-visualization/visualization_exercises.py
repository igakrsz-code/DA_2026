# ══════════════════════════════════════════════════════════════════════════════
# DATA VISUALIZATION EXERCISES 1–6
# ══════════════════════════════════════════════════════════════════════════════

import io, zipfile, urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({
    'axes.grid': True, 'grid.alpha': 0.3,
    'axes.spines.top': False, 'axes.spines.right': False,
    'font.size': 11
})

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 1: Understanding Data Visualization
# ══════════════════════════════════════════════════════════════════════════════

print("═"*60)
print("EXERCISE 1: Understanding Data Visualization")
print("═"*60)
print("""
WHY DATA VISUALIZATION IS IMPORTANT
─────────────────────────────────────
1. Pattern recognition: Humans process visual information far faster
   than tables of numbers. Charts reveal trends, clusters, and outliers
   that would be invisible in raw data.

2. Communication: Visuals convey complex findings to both technical
   and non-technical audiences quickly and clearly.

3. Decision-making: Stakeholders can act on insights they can see and
   understand — a well-chosen chart reduces ambiguity.

4. Data quality: Plotting data often exposes errors, missing values,
   or unexpected distributions that summary statistics miss.

5. Hypothesis generation: Visual exploration sparks questions and
   guides deeper statistical analysis.

PURPOSE OF A LINE GRAPH
─────────────────────────
A line graph connects data points with a continuous line, making it
ideal for showing change over time (time-series data). Key uses:
  • Tracking trends — rising, falling, or cyclical patterns.
  • Comparing multiple series on the same time axis.
  • Highlighting rate of change (steeper = faster change).
  • Examples: temperature over days, stock prices, monthly sales.
""")

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 2: Line Plot — Temperature Variation
# ══════════════════════════════════════════════════════════════════════════════

print("═"*60)
print("EXERCISE 2: Line Plot — Weekly Temperature")
print("═"*60)

days         = ["Monday","Tuesday","Wednesday","Thursday",
                "Friday","Saturday","Sunday"]
temperatures = [72, 74, 76, 80, 82, 78, 75]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(days, temperatures,
        marker='o', color='steelblue', lw=2.5,
        markersize=8, markerfacecolor='white',
        markeredgewidth=2, label='Temperature')
ax.fill_between(days, temperatures, min(temperatures),
                alpha=0.1, color='steelblue')

# Annotate each point
for i, (day, temp) in enumerate(zip(days, temperatures)):
    ax.annotate(f"{temp}°F",
                xy=(i, temp),
                xytext=(0, 10),
                textcoords='offset points',
                ha='center', fontsize=9, color='steelblue')

ax.set_xlabel("Day",             fontsize=12)
ax.set_ylabel("Temperature (°F)", fontsize=12)
ax.set_title("Temperature Variation Over a Week",
             fontsize=14, fontweight='bold')
ax.set_ylim(68, 86)
ax.legend()
plt.tight_layout()
plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 3: Bar Chart — Monthly Sales
# ══════════════════════════════════════════════════════════════════════════════

print("═"*60)
print("EXERCISE 3: Bar Chart — Monthly Sales")
print("═"*60)

months = ["January","February","March","April","May"]
sales  = [5000, 5500, 6200, 7000, 7500]
colors = ['#2196F3','#42A5F5','#64B5F6','#1565C0','#0D47A1']

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(months, sales, color=colors, alpha=0.88,
              edgecolor='white', linewidth=1.2)
ax.bar_label(bars, fmt='$%,.0f', padding=5, fontsize=10)

ax.set_xlabel("Month",          fontsize=12)
ax.set_ylabel("Sales Amount ($)", fontsize=12)
ax.set_title("Monthly Sales Data — Retail Store",
             fontsize=14, fontweight='bold')
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f'${x:,.0f}')
    if False else
    plt.matplotlib.ticker.FuncFormatter(lambda x, _: f'${x:,.0f}')
)
ax.set_ylim(0, max(sales) * 1.2)
plt.tight_layout()
plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# LOAD STUDENT MENTAL HEALTH DATASET
# ══════════════════════════════════════════════════════════════════════════════

URL = ("https://github.com/devtlv/Datasets-GEN-AI-Bootcamp/raw/refs/heads/main/"
       "Week%203/W3D1%20-%20Data%20Visualization/Student%20Mental%20health.zip")

print("Downloading Student Mental Health dataset…")
try:
    with urllib.request.urlopen(URL) as r:
        zip_bytes = r.read()
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        print("Files:", zf.namelist())
        csv_name = [n for n in zf.namelist() if n.endswith('.csv')][0]
        with zf.open(csv_name) as f:
            df = pd.read_csv(f)
    print(f"Loaded: {csv_name}  →  {df.shape}")
except Exception as e:
    print(f"Download failed ({e}) — generating synthetic dataset…")
    np.random.seed(42)
    n = 300
    df = pd.DataFrame({
        'Timestamp'                     : pd.date_range('2022-01-01', periods=n, freq='D'),
        'Choose your gender'            : np.random.choice(['Male','Female'], n, p=[0.45,0.55]),
        'Age'                           : np.random.randint(17, 25, n),
        'What is your course?'          : np.random.choice(['Engineering','BCS','Law','Accounting'], n),
        'Your current year of Study'    : np.random.choice(['Year 1','Year 2','Year 3','Year 4'], n),
        'What is your CGPA?'            : np.random.choice(
                                              ['3.50 - 4.00','3.00 - 3.49',
                                               '2.50 - 2.99','2.00 - 2.49'], n,
                                              p=[0.35,0.35,0.20,0.10]),
        'Marital status'                : np.random.choice(['No','Yes'], n, p=[0.85,0.15]),
        'Do you have Depression?'       : np.random.choice(['Yes','No'], n, p=[0.35,0.65]),
        'Do you have Anxiety?'          : np.random.choice(['Yes','No'], n, p=[0.40,0.60]),
        'Do you have Panic Attacks?'    : np.random.choice(['Yes','No'], n, p=[0.30,0.70]),
        'Did you seek any specialist?'  : np.random.choice(['Yes','No'], n, p=[0.20,0.80]),
    })
    print("Synthetic dataset created ✅")

print("\nColumn names:", df.columns.tolist())
print("\nFirst 5 rows:")
display(df.head())

# Standardise column names (strip whitespace)
df.columns = df.columns.str.strip()

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 4: Histogram — CGPA Distribution
# ══════════════════════════════════════════════════════════════════════════════

print("═"*60)
print("EXERCISE 4: Histogram — CGPA Distribution")
print("═"*60)

cgpa_col = [c for c in df.columns if 'CGPA' in c or 'cgpa' in c.lower()][0]
print(f"CGPA column: '{cgpa_col}'")
print(df[cgpa_col].value_counts())

fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(
    data    = df,
    x       = cgpa_col,
    color   = 'steelblue',
    edgecolor = 'white',
    shrink  = 0.8,
    ax      = ax
)
ax.set_title("Distribution of Students' CGPA",
             fontsize=14, fontweight='bold')
ax.set_xlabel("CGPA Range",   fontsize=12)
ax.set_ylabel("Number of Students", fontsize=12)
ax.tick_params(axis='x', rotation=20)
plt.tight_layout()
plt.show()

print(f"\nMost common CGPA range: {df[cgpa_col].mode()[0]}")
print(f"CGPA distribution:\n{df[cgpa_col].value_counts()}")

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 5: Bar Plot — Anxiety Levels by Gender
# ══════════════════════════════════════════════════════════════════════════════

print("═"*60)
print("EXERCISE 5: Bar Plot — Anxiety by Gender")
print("═"*60)

anxiety_col = [c for c in df.columns if 'Anxiety' in c][0]
gender_col  = [c for c in df.columns if 'gender' in c.lower()][0]

# Calculate proportion with anxiety per gender
anxiety_by_gender = (
    df.groupby([gender_col, anxiety_col])
    .size()
    .reset_index(name='count')
)
total_by_gender = df.groupby(gender_col).size().reset_index(name='total')
anxiety_by_gender = anxiety_by_gender.merge(total_by_gender, on=gender_col)
anxiety_by_gender['proportion'] = (
    anxiety_by_gender['count'] / anxiety_by_gender['total'] * 100
).round(2)

print(anxiety_by_gender)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Count plot
sns.countplot(
    data     = df,
    x        = gender_col,
    hue      = anxiety_col,
    palette  = {'Yes': '#e74c3c', 'No': '#2ecc71'},
    edgecolor= 'white',
    ax       = axes[0]
)
axes[0].set_title("Anxiety Count by Gender", fontweight='bold')
axes[0].set_xlabel("Gender"); axes[0].set_ylabel("Count")
axes[0].legend(title='Has Anxiety?')

# Proportion bar plot
anxiety_yes = anxiety_by_gender[anxiety_by_gender[anxiety_col] == 'Yes']
axes[1].bar(anxiety_yes[gender_col], anxiety_yes['proportion'],
            color=['#3498db','#e91e63'], alpha=0.85, edgecolor='white')
for i, (_, row) in enumerate(anxiety_yes.iterrows()):
    axes[1].text(i, row['proportion'] + 1,
                 f"{row['proportion']:.1f}%",
                 ha='center', fontweight='bold')
axes[1].set_title("% of Students with Anxiety by Gender", fontweight='bold')
axes[1].set_xlabel("Gender"); axes[1].set_ylabel("Proportion (%)")
axes[1].set_ylim(0, 100)

plt.suptitle("Anxiety Levels Across Different Genders",
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 6: Scatter Plot — Age vs Panic Attacks
# ══════════════════════════════════════════════════════════════════════════════

print("═"*60)
print("EXERCISE 6: Scatter Plot — Age vs Panic Attacks")
print("═"*60)

age_col    = [c for c in df.columns if 'Age' in c or 'age' in c.lower()][0]
panic_col  = [c for c in df.columns if 'Panic' in c][0]

# Convert Yes/No to numeric
df['Panic_Numeric'] = df[panic_col].map({'Yes': 1, 'No': 0})
print(f"\nPanic attack mapping:\n{df[[panic_col,'Panic_Numeric']].value_counts()}")

# Add jitter so points don't overlap on y=0 and y=1
np.random.seed(42)
jitter = np.random.uniform(-0.05, 0.05, len(df))

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: basic scatter with jitter
colors_map = {1: '#e74c3c', 0: '#2ecc71'}
for val, label, color in [(1,'Yes — Panic','#e74c3c'),(0,'No — No Panic','#2ecc71')]:
    subset = df[df['Panic_Numeric'] == val]
    axes[0].scatter(
        subset[age_col],
        subset['Panic_Numeric'] + jitter[:len(subset)],
        alpha=0.5, s=50, color=color, label=label, edgecolors='white'
    )
axes[0].set_yticks([0, 1])
axes[0].set_yticklabels(['No (0)', 'Yes (1)'])
axes[0].set_xlabel("Age", fontsize=12)
axes[0].set_ylabel("Panic Attacks", fontsize=12)
axes[0].set_title("Age vs Panic Attacks (jittered)", fontweight='bold')
axes[0].legend()

# Plot 2: proportion of panic attacks per age
panic_by_age = df.groupby(age_col)['Panic_Numeric'].mean() * 100
axes[1].bar(panic_by_age.index, panic_by_age.values,
            color='#9b59b6', alpha=0.8, edgecolor='white')
axes[1].set_xlabel("Age", fontsize=12)
axes[1].set_ylabel("% with Panic Attacks", fontsize=12)
axes[1].set_title("Panic Attack Rate by Age", fontweight='bold')

plt.suptitle("Relationship Between Age and Panic Attacks",
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# Stats summary
print(f"\nOverall panic attack rate : {df['Panic_Numeric'].mean()*100:.1f}%")
print(f"\nPanic attack rate by gender:")
print(df.groupby(gender_col)['Panic_Numeric'].mean().mul(100).round(1))
print(f"\nMean age with panic    : {df[df['Panic_Numeric']==1][age_col].mean():.1f}")
print(f"Mean age without panic : {df[df['Panic_Numeric']==0][age_col].mean():.1f}")

# T-test: age difference between panic vs no panic
from scipy.stats import ttest_ind
t, p = ttest_ind(
    df[df['Panic_Numeric']==1][age_col].dropna(),
    df[df['Panic_Numeric']==0][age_col].dropna()
)
print(f"\nT-test (age vs panic): t={t:.4f}, p={p:.4f}")
print("Age is significantly related to panic attacks:"
      if p < 0.05 else "No significant age difference.")
