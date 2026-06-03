# ══════════════════════════════════════════════════════════════════════════════
# SCIPY STATISTICAL ANALYSIS — Exercises 1–8
# ══════════════════════════════════════════════════════════════════════════════

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy

plt.rcParams.update({'axes.grid': True, 'grid.alpha': 0.3,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'font.size': 11})

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 1: Basic Usage of SciPy
# ══════════════════════════════════════════════════════════════════════════════

print("═"*55)
print("EXERCISE 1: SciPy Version")
print("═"*55)

print(f"SciPy version  : {scipy.__version__}")
print(f"NumPy version  : {np.__version__}")
print(f"Pandas version : {pd.__version__}")

# Explore top-level SciPy submodules
import scipy.stats, scipy.optimize, scipy.linalg, scipy.signal
print("\nKey SciPy submodules:")
for mod in ["stats","optimize","linalg","signal","integrate","interpolate"]:
    print(f"  scipy.{mod}")

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 2: Descriptive Statistics
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*55)
print("EXERCISE 2: Descriptive Statistics")
print("═"*55)

from scipy import stats

data = [12, 15, 13, 12, 18, 20, 22, 21]

mean     = np.mean(data)
median   = np.median(data)
variance = np.var(data, ddof=1)          # sample variance
std_dev  = np.std(data, ddof=1)          # sample std dev
mode_res = stats.mode(data, keepdims=True)
skewness = stats.skew(data)
kurtosis = stats.kurtosis(data)

print(f"\nDataset  : {data}")
print(f"\nMean     : {mean:.4f}")
print(f"Median   : {median:.4f}")
print(f"Variance : {variance:.4f}")
print(f"Std Dev  : {std_dev:.4f}")
print(f"Mode     : {mode_res.mode[0]}  (appears {mode_res.count[0]} times)")
print(f"Skewness : {skewness:.4f}  ({'right-skewed' if skewness > 0 else 'left-skewed'})")
print(f"Kurtosis : {kurtosis:.4f}")

# Using scipy.stats.describe for a full summary
desc = stats.describe(data)
print(f"\nscipy.stats.describe output:")
print(f"  n        : {desc.nobs}")
print(f"  min/max  : {desc.minmax}")
print(f"  mean     : {desc.mean:.4f}")
print(f"  variance : {desc.variance:.4f}")
print(f"  skewness : {desc.skewness:.4f}")
print(f"  kurtosis : {desc.kurtosis:.4f}")

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 3: Normal Distribution
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*55)
print("EXERCISE 3: Normal Distribution")
print("═"*55)

from scipy.stats import norm

mu    = 50
sigma = 10
x     = np.linspace(mu - 4*sigma, mu + 4*sigma, 300)
pdf   = norm.pdf(x, mu, sigma)
cdf   = norm.cdf(x, mu, sigma)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# PDF
axes[0].plot(x, pdf, color="steelblue", lw=2, label="PDF")
axes[0].fill_between(x, pdf, alpha=0.2, color="steelblue")
axes[0].axvline(mu,         color="red",    lw=1.5, linestyle="--", label=f"Mean = {mu}")
axes[0].axvline(mu + sigma, color="orange", lw=1,   linestyle=":",  label=f"±1σ = {sigma}")
axes[0].axvline(mu - sigma, color="orange", lw=1,   linestyle=":")
axes[0].set_title(f"Normal Distribution PDF  (μ={mu}, σ={sigma})", fontweight="bold")
axes[0].set_xlabel("x"); axes[0].set_ylabel("Probability Density")
axes[0].legend()

# CDF
axes[1].plot(x, cdf, color="darkorange", lw=2)
axes[1].axhline(0.5, color="red", lw=1, linestyle="--", label="50th percentile")
axes[1].set_title("Normal Distribution CDF", fontweight="bold")
axes[1].set_xlabel("x"); axes[1].set_ylabel("Cumulative Probability")
axes[1].legend()

plt.tight_layout(); plt.show()

print(f"P(X < 50)  = {norm.cdf(50, mu, sigma):.4f}")
print(f"P(X < 60)  = {norm.cdf(60, mu, sigma):.4f}")
print(f"P(40<X<60) = {norm.cdf(60,mu,sigma) - norm.cdf(40,mu,sigma):.4f}  (≈68% within 1σ)")
print(f"95th pctile = {norm.ppf(0.95, mu, sigma):.2f}")

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 4: T-Test
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*55)
print("EXERCISE 4: T-Test Application")
print("═"*55)

np.random.seed(42)
data1 = np.random.normal(50, 10, 100)
data2 = np.random.normal(60, 10, 100)

# Independent two-sample t-test
t_stat, p_value = stats.ttest_ind(data1, data2)

print(f"\nGroup 1 — mean: {data1.mean():.2f}, std: {data1.std():.2f}, n: {len(data1)}")
print(f"Group 2 — mean: {data2.mean():.2f}, std: {data2.std():.2f}, n: {len(data2)}")
print(f"\nT-statistic : {t_stat:.4f}")
print(f"P-value     : {p_value:.6f}")
print(f"\nConclusion  : {'Reject H₀ — significant difference (p < 0.05)' if p_value < 0.05 else 'Fail to reject H₀'}")

# One-sample t-test (vs known mean)
t1, p1 = stats.ttest_1samp(data1, popmean=50)
print(f"\nOne-sample t-test (data1 vs μ=50): t={t1:.4f}, p={p1:.4f}")

# Welch's t-test (unequal variances)
t_w, p_w = stats.ttest_ind(data1, data2, equal_var=False)
print(f"Welch's t-test                    : t={t_w:.4f}, p={p_w:.6f}")

# Visualise
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(data1, bins=20, alpha=0.6, color="steelblue",  label=f"Group 1 (μ=50)")
ax.hist(data2, bins=20, alpha=0.6, color="darkorange", label=f"Group 2 (μ=60)")
ax.axvline(data1.mean(), color="steelblue",  lw=2, linestyle="--")
ax.axvline(data2.mean(), color="darkorange", lw=2, linestyle="--")
ax.set_title(f"T-Test: Two Groups  (t={t_stat:.2f}, p={p_value:.4f})", fontweight="bold")
ax.set_xlabel("Value"); ax.set_ylabel("Frequency")
ax.legend(); plt.tight_layout(); plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 5: Linear Regression
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*55)
print("EXERCISE 5: Linear Regression — Housing Prices")
print("═"*55)

from scipy.stats import linregress

house_sizes  = [50,  70,  80,  100, 120]
house_prices = [150000, 200000, 210000, 250000, 280000]

slope, intercept, r_value, p_value, std_err = linregress(house_sizes, house_prices)

print(f"\nSlope     : {slope:.2f}  → each extra m² adds £{slope:,.2f} to price")
print(f"Intercept : {intercept:.2f}")
print(f"R²        : {r_value**2:.4f}  ({r_value**2*100:.1f}% of variance explained)")
print(f"P-value   : {p_value:.6f}")
print(f"Std error : {std_err:.4f}")

# Prediction
size_to_predict = 90
predicted_price = slope * size_to_predict + intercept
print(f"\nPredicted price for {size_to_predict}m²: £{predicted_price:,.2f}")

# Regression line
x_line = np.linspace(40, 130, 200)
y_line = slope * x_line + intercept

fig, ax = plt.subplots(figsize=(9, 6))
ax.scatter(house_sizes, house_prices, color="steelblue",
           s=100, zorder=5, label="Actual data")
ax.plot(x_line, y_line, color="red", lw=2, label=f"Regression line (R²={r_value**2:.3f})")
ax.scatter(size_to_predict, predicted_price, color="green",
           s=150, marker="*", zorder=6, label=f"Prediction: {size_to_predict}m² → £{predicted_price:,.0f}")
ax.set_title("Housing Price Linear Regression", fontweight="bold")
ax.set_xlabel("House Size (m²)"); ax.set_ylabel("Price (£)")
ax.legend(); plt.tight_layout(); plt.show()

print(f"""
Interpretation:
  Slope = {slope:.2f}
    → For every additional square metre, the house price increases
      by approximately £{slope:,.0f}.

  Intercept = {intercept:.2f}
    → Theoretical price of a 0m² house (not meaningful practically,
      but required for the regression equation).

  R² = {r_value**2:.4f}
    → {r_value**2*100:.1f}% of the variation in price is explained by size alone.
    → Very strong linear relationship in this small dataset.
""")

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 6: ANOVA
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*55)
print("EXERCISE 6: One-Way ANOVA — Fertilizer Effects")
print("═"*55)

from scipy.stats import f_oneway

fertilizer_1 = [5, 6, 7, 6, 5]
fertilizer_2 = [7, 8, 7, 9, 8]
fertilizer_3 = [4, 5, 4, 3, 4]

f_stat, p_value = f_oneway(fertilizer_1, fertilizer_2, fertilizer_3)

print(f"\nGroup means:")
print(f"  Fertilizer 1 : {np.mean(fertilizer_1):.2f} cm")
print(f"  Fertilizer 2 : {np.mean(fertilizer_2):.2f} cm")
print(f"  Fertilizer 3 : {np.mean(fertilizer_3):.2f} cm")
print(f"\nF-value  : {f_stat:.4f}")
print(f"P-value  : {p_value:.6f}")
print(f"\nConclusion: {'Reject H₀ — fertilizers have significantly different effects (p < 0.05)' if p_value < 0.05 else 'Fail to reject H₀'}")

# Visualise
fig, ax = plt.subplots(figsize=(9, 6))
ax.boxplot([fertilizer_1, fertilizer_2, fertilizer_3],
           labels=["Fertilizer 1","Fertilizer 2","Fertilizer 3"],
           patch_artist=True,
           boxprops=dict(facecolor="lightblue", alpha=0.7))
ax.set_title(f"ANOVA: Plant Growth by Fertilizer\n(F={f_stat:.2f}, p={p_value:.4f})",
             fontweight="bold")
ax.set_ylabel("Growth (cm)")
plt.tight_layout(); plt.show()

print(f"""
Answers:
  F-value = {f_stat:.4f},  P-value = {p_value:.6f}

  Q1: The F-value measures the ratio of between-group variance to
      within-group variance. A high F ({f_stat:.2f}) means groups differ
      more than expected by chance.

  Q2: P = {p_value:.6f} < 0.05 → Yes, the fertilizers have
      significantly different effects on plant growth.
      Fertilizer 2 produces the most growth on average.

  Q3: If p > 0.05 we would fail to reject H₀, concluding there is
      insufficient evidence that the fertilizers differ — any observed
      differences could be due to random variation alone.
""")

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 7 (Optional): Binomial Distribution
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*55)
print("EXERCISE 7 (Optional): Binomial Distribution")
print("═"*55)

from scipy.stats import binom

n = 10    # number of flips
p = 0.5   # probability of heads

# P(exactly 5 heads)
p_exactly_5 = binom.pmf(5, n, p)
print(f"P(exactly 5 heads in 10 flips) = {p_exactly_5:.4f} ({p_exactly_5*100:.2f}%)")

# Full distribution
k_values = np.arange(0, n+1)
pmf      = binom.pmf(k_values, n, p)
cdf      = binom.cdf(k_values, n, p)

print(f"\nP(X ≤ 5) = {binom.cdf(5, n, p):.4f}")
print(f"P(X ≥ 7) = {1 - binom.cdf(6, n, p):.4f}")

for k, prob in zip(k_values, pmf):
    bar = "█" * int(prob * 100)
    print(f"  P(X={k:2d}) = {prob:.4f}  {bar}")

# Plot
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].bar(k_values, pmf, color="steelblue", alpha=0.85, edgecolor="white")
axes[0].bar(5, binom.pmf(5, n, p), color="red", alpha=0.9, label="P(X=5)")
axes[0].set_title("Binomial PMF (n=10, p=0.5)", fontweight="bold")
axes[0].set_xlabel("Number of Heads"); axes[0].set_ylabel("Probability")
axes[0].legend()

axes[1].step(k_values, cdf, color="darkorange", lw=2, where="post")
axes[1].set_title("Binomial CDF (n=10, p=0.5)", fontweight="bold")
axes[1].set_xlabel("Number of Heads"); axes[1].set_ylabel("Cumulative Probability")
plt.tight_layout(); plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE 8 (Optional): Correlation Coefficients
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*55)
print("EXERCISE 8 (Optional): Correlation Coefficients")
print("═"*55)

from scipy.stats import pearsonr, spearmanr

data = pd.DataFrame({
    'age'   : [23, 25, 30, 35, 40],
    'income': [35000, 40000, 50000, 60000, 70000]
})

pearson_r,  pearson_p  = pearsonr(data['age'],  data['income'])
spearman_r, spearman_p = spearmanr(data['age'], data['income'])

print(f"\nDataset:\n{data.to_string(index=False)}")
print(f"\nPearson  r = {pearson_r:.4f},  p = {pearson_p:.6f}")
print(f"Spearman r = {spearman_r:.4f},  p = {spearman_p:.6f}")
print(f"\nBoth correlations are significant (p < 0.05): "
      f"{'Yes' if pearson_p < 0.05 else 'No'}")

# Visualise
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(data['age'], data['income'], color="steelblue", s=100, zorder=5)
for _, row in data.iterrows():
    ax.annotate(f"({int(row.age)}, {int(row.income):,})",
                (row.age, row.income),
                textcoords="offset points", xytext=(8, 4), fontsize=9)
m, b = np.polyfit(data['age'], data['income'], 1)
x_fit = np.linspace(20, 45, 100)
ax.plot(x_fit, m*x_fit + b, color="red", lw=2, linestyle="--",
        label=f"Pearson r={pearson_r:.3f}")
ax.set_title("Age vs Income Correlation", fontweight="bold")
ax.set_xlabel("Age"); ax.set_ylabel("Income (£)")
ax.legend(); plt.tight_layout(); plt.show()

print(f"""
Interpretation:
  Pearson r  = {pearson_r:.4f} → perfect positive LINEAR correlation.
    Age and income increase together in a straight line.

  Spearman r = {spearman_r:.4f} → perfect positive RANK correlation.
    The rank order of ages matches the rank order of incomes exactly.

  When Pearson ≈ Spearman, the relationship is both linear and monotonic.
  If data had outliers or a non-linear pattern, Spearman would be more robust.
""")
