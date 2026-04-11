import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

# Check number of rows before removing duplicates
rows_before = df.shape[0]
print("Rows before removing duplicates:", rows_before)

# Identify duplicate rows
duplicates = df.duplicated()
print("Number of duplicate rows:", duplicates.sum())

# Remove duplicate rows
df_cleaned = df.drop_duplicates()

# Check number of rows after removing duplicates
rows_after = df_cleaned.shape[0]
print("Rows after removing duplicates:", rows_after)

# Verify duplicates removed
print("Duplicates remaining:", df_cleaned.duplicated().sum())

# 1. Identify columns with missing values
print("Missing values in each column:")
print(df.isnull().sum())

# 2. Strategy 1: Remove rows with missing values
df_drop = df.dropna()
print("\nShape after dropping rows with missing values:", df_drop.shape)

# 3. Strategy 2: Fill missing categorical values with a constant
df["Embarked"] = df["Embarked"].fillna("Unknown")

# 4. Strategy 3: Impute missing numerical values with the mean
imputer = SimpleImputer(strategy="mean")
df["Age"] = imputer.fit_transform(df[["Age"]])

# 5. Check if missing values remain
print("\nMissing values after handling:")
print(df.isnull().sum())

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler

# Load dataset (if not already loaded)
df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

# =========================
# 🌟 Exercise 3: Feature Engineering
# =========================

# Create FamilySize from SibSp + Parch + 1 (self)
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

# Extract Title from Name
df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)

# Simplify titles (group rare ones)
df['Title'] = df['Title'].replace(['Lady','Countess','Capt','Col','Don','Dr','Major','Rev','Sir','Jonkheer','Dona'], 'Rare')
df['Title'] = df['Title'].replace(['Mlle','Ms'], 'Miss')
df['Title'] = df['Title'].replace('Mme', 'Mrs')

# Encode Title using LabelEncoder
le_title = LabelEncoder()
df['Title_encoded'] = le_title.fit_transform(df['Title'])

# =========================
# 🌟 Exercise 4: Outlier Detection and Handling
# =========================

# Example: Visualize Fare and Age
# (optional in Colab: df.boxplot(column=['Fare','Age']))

# Using IQR method for Fare
Q1 = df['Fare'].quantile(0.25)
Q3 = df['Fare'].quantile(0.75)
IQR = Q3 - Q1
fare_upper = df['Fare'].quantile(0.98)  # 98th percentile cap
df['Fare'] = np.where(df['Fare'] > fare_upper, fare_upper, df['Fare'])

# Age: cap using 98th percentile
age_upper = df['Age'].quantile(0.98)
df['Age'] = np.where(df['Age'] > age_upper, age_upper, df['Age'])

# =========================
# 🌟 Exercise 5: Data Standardization and Normalization
# =========================

# StandardScaler for Age (assume roughly normal)
scaler_age = StandardScaler()
df['Age_scaled'] = scaler_age.fit_transform(df[['Age']])

# MinMaxScaler for Fare (skewed)
scaler_fare = MinMaxScaler()
df['Fare_scaled'] = scaler_fare.fit_transform(df[['Fare']])

# =========================
# 🌟 Exercise 6: Feature Encoding
# =========================

# Encode categorical columns: Sex, Embarked, Title (already encoded Title above)
# One-Hot Encoding for Sex and Embarked
df = pd.get_dummies(df, columns=['Sex','Embarked'], drop_first=True)

# =========================
# 🌟 Exercise 7: Data Transformation for Age Feature
# =========================

# Create age bins
bins = [0, 12, 18, 60, 100]
labels = ['Child','Teen','Adult','Senior']
df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)

# One-hot encode AgeGroup
df = pd.get_dummies(df, columns=['AgeGroup'], drop_first=True)

# =========================
# Final dataset preview
# =========================
print(df.head())
print("\nColumns after transformations:")
print(df.columns)


