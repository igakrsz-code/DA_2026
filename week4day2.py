import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Exercise 1 : Matrix Operations
# -----------------------------

np.random.seed(42)

matrix = np.random.randint(1, 10, (3, 3))

det = np.linalg.det(matrix)
inv = np.linalg.inv(matrix)

print("Matrix:\n", matrix)
print("Determinant:", det)
print("Inverse:\n", inv)

# -----------------------------
# Exercise 2 : Statistical Analysis
# -----------------------------

data = np.random.randn(50)

mean_val = np.mean(data)
median_val = np.median(data)
std_val = np.std(data)

print("\nMean:", mean_val)
print("Median:", median_val)
print("Std:", std_val)

# -----------------------------
# Exercise 3 : Date Manipulation
# -----------------------------

dates = pd.date_range(start="2023-01-01", end="2023-01-31")
formatted_dates = dates.strftime("%Y/%m/%d")

print("\nFormatted Dates Example:", formatted_dates[:5])

# -----------------------------
# Exercise 4 : Data Manipulation with NumPy and Pandas
# -----------------------------

df = pd.DataFrame(np.random.randint(1, 100, (5, 5)),
                  columns=list("ABCDE"))

print("\nDataFrame:\n", df)

# Conditional selection
filtered = df[df > 50]

# Aggregations
print("\nSum:\n", df.sum().sum())
print("Mean:\n", df.mean().mean())

# -----------------------------
# Exercise 5 : Image Representation
# -----------------------------

image = np.random.randint(0, 256, (5, 5))
print("\nGrayscale Image (5x5):\n", image)

# -----------------------------
# Exercise 6 : Basic Hypothesis Testing
# -----------------------------

productivity_before = np.random.normal(loc=50, scale=10, size=30)
productivity_after = productivity_before + np.random.normal(loc=5, scale=3, size=30)

# Hypothesis: training improves productivity (after > before)

mean_before = np.mean(productivity_before)
mean_after = np.mean(productivity_after)

print("\nBefore mean:", mean_before)
print("After mean:", mean_after)
print("Improvement:", mean_after - mean_before)

# -----------------------------
# Exercise 7 : Complex Array Comparison
# -----------------------------

a = np.random.randint(1, 20, 10)
b = np.random.randint(1, 20, 10)

comparison = a > b

print("\nArray A:", a)
print("Array B:", b)
print("A > B:", comparison)

# -----------------------------
# Exercise 8 : Time Series Data Manipulation
# -----------------------------

time_index = pd.date_range("2023-01-01", "2023-12-31")
ts_data = pd.Series(np.random.randn(len(time_index)), index=time_index)

print("\nJan-Mar:\n", ts_data["2023-01":"2023-03"].head())
print("\nApr-Jun:\n", ts_data["2023-04":"2023-06"].head())
print("\nJul-Sep:\n", ts_data["2023-07":"2023-09"].head())
print("\nOct-Dec:\n", ts_data["2023-10":"2023-12"].head())

# -----------------------------
# Exercise 9 : Data Conversion
# -----------------------------

arr = np.array([[1, 2], [3, 4]])

df_conv = pd.DataFrame(arr)
arr_back = df_conv.to_numpy()

print("\nDataFrame:\n", df_conv)
print("Back to array:\n", arr_back)

# -----------------------------
# Exercise 10 : Basic Visualization
# -----------------------------

plt.figure()

random_line = np.random.randn(100)
plt.plot(random_line)

plt.title("Random Line Plot")
plt.xlabel("Index")
plt.ylabel("Value")

plt.show()
