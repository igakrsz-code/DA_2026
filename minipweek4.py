import os, zipfile, io, urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Patch
from scipy import stats
from scipy.signal import butter, filtfilt

plt.rcParams.update({
    'figure.figsize': (14, 5), 'axes.grid': True, 'grid.alpha': 0.3,
    'axes.spines.top': False, 'axes.spines.right': False, 'font.size': 11,
})

# ── 1. LOAD DATA ──────────────────────────────────────────────────────────────
URL = (
    'https://github.com/devtlv/Datasets-GEN-AI-Bootcamp/raw/refs/heads/main/'
    'Week%203/W3D4%20-%20Mini%20Project/Apple%20Stock%20Prices%20From%201981%20to%202023.zip'
)
print('Downloading dataset…')
with urllib.request.urlopen(URL) as resp:
    zip_bytes = resp.read()
with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
    csv_name = [n for n in zf.namelist() if n.lower().endswith('.csv')][0]
    with zf.open(csv_name) as f:
        df = pd.read_csv(f)

df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df['date'] = pd.to_datetime(df['date'])
df.sort_values('date', inplace=True)
df.set_index('date', inplace=True)
df['daily_return'] = df['close'].pct_change()
df['year'] = df.index.year
df['decade'] = (df['year'] // 10) * 10

print(df.shape, '\n', df.dtypes)
print('\nNull values:\n', df.isnull().sum())
print(df.describe().round(2))

# ── 2. VISUALIZATION ──────────────────────────────────────────────────────────
# 2.1 Closing price
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(df.index, df['close'], color='steelblue', lw=0.8)
ax.set_title('AAPL Closing Price (1981–2023)', fontsize=14, fontweight='bold')
ax.set_xlabel('Date'); ax.set_ylabel('Price (USD)')
plt.tight_layout(); plt.show()

# 2.2 Volume
fig, ax = plt.subplots(figsize=(15, 4))
ax.bar(df.index, df['volume'], color='coral', alpha=0.6, width=1)
ax.set_title('AAPL Trading Volume (1981–2023)', fontsize=14, fontweight='bold')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e9:.1f}B'))
ax.set_xlabel('Date'); ax.set_ylabel('Shares Traded')
plt.tight_layout(); plt.show()

# 2.3 Candlestick (last 3 months)
recent = df.tail(63).copy()
fig, ax = plt.subplots(figsize=(15, 6))
for i, (date, row) in enumerate(recent.iterrows()):
    color = 'green' if row['close'] >= row['open'] else 'red'
    ax.plot([i, i], [row['low'], row['high']], color=color, lw=0.8)
    body_bot, body_top = min(row['open'], row['close']), max(row['open'], row['close'])
    ax.add_patch(plt.Rectangle((i - 0.3, body_bot), 0.6, body_top - body_bot, color=color, alpha=0.8))
ticks = range(0, len(recent), 10)
ax.set_xticks(list(ticks))
ax.set_xticklabels([recent.index[i].strftime('%b %d\n%Y') for i in ticks], fontsize=8)
ax.set_title('AAPL Candlestick – Last ~3 Trading Months', fontsize=14, fontweight='bold')
ax.legend(handles=[Patch(facecolor='green', label='Bullish'), Patch(facecolor='red', label='Bearish')])
plt.tight_layout(); plt.show()

# ── 3. STATISTICAL ANALYSIS ───────────────────────────────────────────────────
# 3.1 Summary stats
print(df[['open','high','low','close','volume']].agg(['mean','median','std','min','max']).round(2))

# 3.2 Moving averages
df['MA50']  = df['close'].rolling(50).mean()
df['MA200'] = df['close'].rolling(200).mean()
df_r = df['2018':]
fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(df_r.index, df_r['close'], color='steelblue', lw=1, label='Close')
ax.plot(df_r.index, df_r['MA50'],  color='orange', lw=1.5, label='50-day MA')
ax.plot(df_r.index, df_r['MA200'], color='red', lw=1.5, linestyle='--', label='200-day MA')
ax.set_title('Closing Price with Moving Averages (2018–2023)', fontsize=13, fontweight='bold')
ax.legend(); plt.tight_layout(); plt.show()

# 3.3 Daily returns distribution
returns = df['daily_return'].dropna()
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(returns, bins=150, color='steelblue', alpha=0.7, density=True)
xr = np.linspace(returns.min(), returns.max(), 500)
axes[0].plot(xr, stats.norm.pdf(xr, returns.mean(), returns.std()), color='red', lw=2, label='Normal PDF')
axes[0].set_xlim(-0.3, 0.3); axes[0].set_title('Daily Return Distribution'); axes[0].legend()
stats.probplot(returns, dist='norm', plot=axes[1]); axes[1].set_title('Q-Q Plot of Daily Returns')
plt.tight_layout(); plt.show()
print(f'Skewness: {returns.skew():.4f} | Excess Kurtosis: {returns.kurtosis():.4f}')

# ── 4. HYPOTHESIS TESTING ─────────────────────────────────────────────────────
# 4.1 Welch t-test: 2000s vs 2010s
g_a = df.loc[df['year'].between(2000, 2009), 'close'].dropna()
g_b = df.loc[df['year'].between(2010, 2019), 'close'].dropna()
t, p = stats.ttest_ind(g_a, g_b, equal_var=False)
print(f'\nWelch t-test: t={t:.4f}, p={p:.2e}')
print('Reject H₀' if p < 0.05 else 'Fail to reject H₀')

# 4.2 Normality tests
sw_stat, sw_p = stats.shapiro(returns.sample(3000, random_state=42))
jb_stat, jb_p = stats.jarque_bera(returns)
print(f'Shapiro-Wilk: stat={sw_stat:.6f}, p={sw_p:.2e}')
print(f'Jarque-Bera:  stat={jb_stat:.2f}, p={jb_p:.2e}')

# 4.3 Mean close by decade
decade_means = df.groupby('decade')['close'].mean()
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(decade_means.index.astype(str) + 's', decade_means.values, color='steelblue', alpha=0.8, width=0.5)
ax.bar_label(bars, fmt='$%.2f', padding=4)
ax.set_title('Mean AAPL Closing Price by Decade', fontsize=13, fontweight='bold')
plt.tight_layout(); plt.show()

# ── 5. ADVANCED STATISTICAL TECHNIQUES ───────────────────────────────────────
# 5a. Butterworth low-pass filter
close_vals = df['close'].dropna().values
valid_idx  = df.index[~df['close'].isna()]

def butter_lowpass(data, cutoff=0.03, fs=1.0, order=4):
    b, a = butter(order, cutoff / (0.5 * fs), btype='low', analog=False)
    return filtfilt(b, a, data)

s_strict = butter_lowpass(close_vals, cutoff=0.02)
s_loose  = butter_lowpass(close_vals, cutoff=0.08)

fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(valid_idx, close_vals, color='lightsteelblue', lw=0.5, alpha=0.7, label='Original')
ax.plot(valid_idx, s_loose,   color='orange', lw=1.5, label='Low-pass (0.08)')
ax.plot(valid_idx, s_strict,  color='red',    lw=2,   linestyle='--', label='Low-pass (0.02)')
ax.set_title('Butterworth Low-Pass Filtered Signals', fontsize=13, fontweight='bold')
ax.legend(); plt.tight_layout(); plt.show()

# 5b-1. np.convolve moving average
window = 30
conv_ma    = np.convolve(close_vals, np.ones(window) / window, mode='valid')
conv_index = valid_idx[window - 1:]
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(valid_idx,  close_vals, color='lightsteelblue', lw=0.6, alpha=0.8, label='Close')
ax.plot(conv_index, conv_ma,    color='darkgreen',      lw=1.8, label=f'np.convolve {window}-day MA')
ax.set_title(f'{window}-Day Moving Average via np.convolve', fontsize=13, fontweight='bold')
ax.legend(); plt.tight_layout(); plt.show()

# 5b-2. np.corrcoef heatmap
metrics = [m for m in ['open','high','low','close','volume'] if m in df.columns]
corr = np.corrcoef(df[metrics].dropna().values.T)
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(corr, cmap='RdYlGn', vmin=-1, vmax=1)
plt.colorbar(im, ax=ax, label='Pearson r')
ax.set_xticks(range(len(metrics))); ax.set_yticks(range(len(metrics)))
ax.set_xticklabels([m.upper() for m in metrics], rotation=30, ha='right')
ax.set_yticklabels([m.upper() for m in metrics])
for i in range(len(metrics)):
    for j in range(len(metrics)):
        ax.text(j, i, f'{corr[i,j]:.2f}', ha='center', va='center', fontsize=10)
ax.set_title('Correlation Matrix (np.corrcoef)', fontsize=13, fontweight='bold')
plt.tight_layout(); plt.show()

# 5b-3. Rolling 1-year correlation: close vs volume
roll_corr = df['close'].rolling(252).corr(df['volume'])
df['vol_MA50'] = df['volume'].rolling(50).mean()
roll_ma_corr   = df['MA50'].rolling(252).corr(df['vol_MA50'])

fig, axes = plt.subplots(2, 1, figsize=(15, 8), sharex=True)
axes[0].plot(df.index, df['close'], color='steelblue', lw=0.8)
axes[0].set_title('AAPL Close Price'); axes[0].set_ylabel('USD')

axes[1].plot(df.index, roll_corr, color='purple', lw=1)
axes[1].axhline(0, color='black', lw=0.8, linestyle='--')
axes[1].fill_between(df.index, roll_corr, 0, where=roll_corr > 0, alpha=0.3, color='green', label='Positive')
axes[1].fill_between(df.index, roll_corr, 0, where=roll_corr < 0, alpha=0.3, color='red',   label='Negative')
axes[1].set_title('1-Year Rolling Correlation: Close vs Volume')
axes[1].set_ylim(-1, 1); axes[1].legend()
plt.tight_layout(); plt.show()

print('\n✅ All analysis complete.')
