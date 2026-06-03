import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. Data Preparation
# -----------------------------

np.random.seed(42)

cities = [
    "Tel Aviv", "New York", "London", "Paris", "Tokyo",
    "Berlin", "Sydney", "Toronto", "Madrid", "Rome"
]

months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# Generate synthetic temperature data (-5 to 35 degrees)
data = np.random.uniform(-5, 35, (10, 12))

df = pd.DataFrame(data, index=cities, columns=months)

# -----------------------------
# 2. Data Analysis
# -----------------------------

# Annual average temperature per city
df["Annual_Avg"] = df.mean(axis=1)

# City with highest and lowest average temperature
hottest_city = df["Annual_Avg"].idxmax()
coldest_city = df["Annual_Avg"].idxmin()

print("Hottest city:", hottest_city)
print("Coldest city:", coldest_city)

# -----------------------------
# 3. Data Visualization
# -----------------------------

plt.figure(figsize=(12, 6))

for city in cities:
    plt.plot(months, df.loc[city, months], label=city)

plt.title("Monthly Temperature Trends Across Cities")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

plt.show()

# Optional: Bar plot of annual averages
plt.figure(figsize=(10, 5))
df["Annual_Avg"].sort_values().plot(kind="bar")
plt.title("Annual Average Temperature by City")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.show()
