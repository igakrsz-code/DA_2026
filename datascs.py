# Import necessary libraries
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

# Step 1: Load the dataset
# Replace 'data_science_salaries.csv' with the path to your dataset
df = pd.read_csv('data_science_salaries.csv')

# Step 2: Normalize the 'salary' column using Min-Max scaling
scaler = MinMaxScaler()
df['salary_normalized'] = scaler.fit_transform(df[['salary']])

# Step 3: Dimensionality Reduction
# Drop non-numeric columns first for PCA
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
# Optional: drop the normalized salary to not include in PCA
numeric_cols = numeric_cols.drop('salary_normalized', errors='ignore')

# Apply PCA
pca = PCA(n_components=2)  # Reduce to 2 principal components for visualization
pca_result = pca.fit_transform(df[numeric_cols])
df['PCA1'] = pca_result[:, 0]
df['PCA2'] = pca_result[:, 1]

# Step 4: Aggregation by experience level
# Calculate average and median salary per experience level
salary_stats = df.groupby('experience_level')['salary'].agg(['mean', 'median']).reset_index()

# Optional: show normalized salary stats as well
normalized_stats = df.groupby('experience_level')['salary_normalized'].agg(['mean', 'median']).reset_index()

# Step 5: Output results
print("Salary stats by experience level:")
print(salary_stats)
print("\nNormalized salary stats by experience level:")
print(normalized_stats)

# Step 6: Optional - save results to CSV
salary_stats.to_csv('salary_stats_by_experience.csv', index=False)
