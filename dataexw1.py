# 📊 Data Analysis Exercises — Solutions Guide

> **Exercises 1–10 | Python · Pandas · Matplotlib · Seaborn · Google Colab**

---

## 📋 Table of Contents

| # | Exercise | Topic |
|---|----------|-------|
| 1 | [Exercise 1](#-exercise-1--introduction-to-data-analysis) | Introduction to Data Analysis |
| 2 | [Exercise 2](#-exercise-2--dataset-loading-and-initial-analysis) | Dataset Loading & Initial Analysis |
| 3 | [Exercise 3](#-exercise-3--identifying-data-types) | Identifying Data Types |
| 4 | [Exercise 4](#-exercise-4--exploring-data-types--iris-dataset) | Exploring Data Types — Iris Dataset |
| 5 | [Exercise 5](#-exercise-5--basic-observation-skills) | Basic Observation Skills |
| 6 | [Exercise 6](#-exercise-6--structured-vs-unstructured-data) | Structured vs Unstructured Data |
| 7 | [Exercise 7](#-exercise-7--transformation-exercise) | Transformation Exercise |
| 8 | [Exercise 8](#-exercise-8--import-a-file-from-kaggle) | Import a File from Kaggle |
| 9 | [Exercise 9](#-exercise-9--export-dataframe-to-excel--json) | Export DataFrame to Excel & JSON |
| 10 | [Exercise 10](#-exercise-10--reading-json-data-from-a-url) | Reading JSON Data from a URL |

---

## 🌟 Exercise 1 — Introduction to Data Analysis

### What is Data Analysis?

**Data analysis** is the systematic process of **inspecting, cleansing, transforming, and modelling data** with the goal of discovering useful information, drawing conclusions, and supporting decision-making.

It combines statistical methods, programming, and domain expertise to turn raw numbers and text into actionable insights.

---

### Why is Data Analysis Important?

In the modern world, data is generated at an unprecedented scale. Data analysis allows us to:

- ✅ Make **evidence-based decisions** rather than relying on intuition
- ✅ Identify **patterns, trends, and anomalies** hidden in large datasets
- ✅ **Optimise processes**, reduce costs, and improve efficiency
- ✅ **Predict future outcomes** and mitigate risks proactively
- ✅ Understand **customer behaviour** and personalise experiences

---

### Three Areas Where Data Analysis is Applied Today

#### 1. 🏥 Healthcare & Medicine
Data analysis is used to predict disease outbreaks, personalise treatment plans, and analyse patient outcomes. Electronic health records and genomic data are mined to discover correlations that lead to medical breakthroughs. Machine learning models now detect cancer in medical images with accuracy matching specialist doctors.

#### 2. 💰 Finance & Banking
Banks and financial institutions use data analysis for credit scoring, fraud detection, algorithmic trading, and risk management. Real-time transaction analysis helps flag suspicious activity within milliseconds. Credit card companies analyse thousands of variables to approve or deny applications instantly.

#### 3. 🛒 Marketing & E-Commerce
Companies like Amazon and Netflix analyse customer behaviour, purchase history, and browsing patterns to personalise recommendations and increase conversion rates. A/B testing and cohort analysis are standard tools used daily to optimise user experience and maximise revenue.

---

## 🌟 Exercise 2 — Dataset Loading and Initial Analysis

**Datasets:** How Much Sleep Do Americans Really Get? | Global Trends in Mental Health Disorder | Credit Card Approvals

### Step 1 — Install & Authenticate Kaggle API

```python
!pip install kaggle -q

# Upload your kaggle.json (from kaggle.com → Account → Create API Token)
from google.colab import files
uploaded = files.upload()

import os
os.makedirs(os.path.expanduser('~/.kaggle'), exist_ok=True)
os.rename('kaggle.json', os.path.expanduser('~/.kaggle/kaggle.json'))
os.chmod(os.path.expanduser('~/.kaggle/kaggle.json'), 0o600)
print('✅ Kaggle authenticated!')
```

### Step 2 — Download the Datasets

```python
!kaggle datasets download -d mlomuscio/sleepstudypilot --unzip -q
!kaggle datasets download -d thedevastator/uncover-global-trends-in-mental-health-disorder --unzip -q
!kaggle datasets download -d rikdifos/credit-card-approval-prediction --unzip -q
print('✅ All datasets downloaded!')
```

### Step 3 — Load and Inspect

```python
import pandas as pd

sleep_df  = pd.read_csv('SleepStudyData.csv')
mental_df = pd.read_csv('Mental health Depression disorder Data.csv')
credit_df = pd.read_csv('application_record.csv')

print('=== SLEEP DATASET ===')
print(f'Shape: {sleep_df.shape}')
display(sleep_df.head())

print('\n=== MENTAL HEALTH DATASET ===')
print(f'Shape: {mental_df.shape}')
display(mental_df.head())

print('\n=== CREDIT CARD DATASET ===')
print(f'Shape: {credit_df.shape}')
display(credit_df.head())
```

### Brief Dataset Descriptions

| Dataset | Description |
|---------|-------------|
| **Sleep Study** | Self-reported sleep hours, quality ratings, and lifestyle factors for American participants. Useful for trend and correlation analysis. |
| **Mental Health** | Global prevalence rates of depression, anxiety, and bipolar disorder across countries and years. Useful for geographic and temporal trend analysis. |
| **Credit Cards** | Applicant demographic and financial attributes alongside approval status. Useful for classification and predictive modelling. |

---

## 🌟 Exercise 3 — Identifying Data Types

### Automated Column Type Detection

```python
import pandas as pd

datasets = {
    'Sleep Study':   sleep_df,
    'Mental Health': mental_df,
    'Credit Cards':  credit_df
}

for name, df in datasets.items():
    print('=' * 50)
    print(f'📊 {name}')
    print('=' * 50)
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    object_cols  = df.select_dtypes(include='object').columns.tolist()
    print(f'  ➡ Quantitative : {numeric_cols}')
    print(f'  ➡ Qualitative  : {object_cols}\n')
```

### Manual Classification — Sleep Dataset

| Column | Type | Reason |
|--------|------|--------|
| Hours of Sleep | Quantitative (continuous) | Numeric — measurable hours of duration |
| Sleep Quality | Quantitative (ordinal) | Numeric rating on a scale (1–10) |
| Gender | Qualitative (nominal) | Categorical label with no numeric order |
| Occupation | Qualitative (nominal) | Named category — no meaningful numeric value |
| Stress Level | Quantitative (ordinal) | Ordered rating scale — numeric but ordinal |

### Manual Classification — Mental Health Dataset

| Column | Type | Reason |
|--------|------|--------|
| Entity (Country) | Qualitative (nominal) | Named category — country names |
| Year | Quantitative (discrete) | Numeric — countable time unit |
| Depression (%) | Quantitative (continuous) | Continuous percentage measure |
| Anxiety (%) | Quantitative (continuous) | Continuous percentage measure |

### Manual Classification — Credit Card Dataset

| Column | Type | Reason |
|--------|------|--------|
| Gender | Qualitative (nominal) | Categorical — M/F |
| Annual Income | Quantitative (continuous) | Continuous monetary value |
| Age | Quantitative (continuous) | Continuous numeric value |
| Family Status | Qualitative (nominal) | Named category |

---

## 🌟 Exercise 4 — Exploring Data Types: Iris Dataset

### Load the Dataset

```python
!kaggle datasets download -d uciml/iris --unzip -q

import pandas as pd

iris_df = pd.read_csv('Iris.csv')
print('First 5 rows:')
display(iris_df.head())

print('\nDataset info:')
iris_df.info()
```

### Identify Column Types

```python
print('🔢 Quantitative columns:')
print(' ', iris_df.select_dtypes(include='number').columns.tolist())

print('\n🏷️  Qualitative columns:')
print(' ', iris_df.select_dtypes(include='object').columns.tolist())
```

### Column Classification Table

| Column | Type | Sub-type | Justification |
|--------|------|----------|---------------|
| SepalLengthCm | Quantitative | Continuous | Physical measurement in cm — any real value within range |
| SepalWidthCm | Quantitative | Continuous | Physical measurement in cm — any real value within range |
| PetalLengthCm | Quantitative | Continuous | Physical measurement in cm — any real value within range |
| PetalWidthCm | Quantitative | Continuous | Physical measurement in cm — any real value within range |
| Species | Qualitative | Nominal | Named class label (Setosa/Versicolor/Virginica) — no numeric order |

```python
# Descriptive statistics for quantitative columns
display(iris_df.describe())
```

---

## 🌟 Exercise 5 — Basic Observation Skills

### Load the Sleep Dataset

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sleep_df = pd.read_csv('SleepStudyData.csv')

print('Columns:', sleep_df.columns.tolist())
display(sleep_df.head())
```

### Interesting Columns for Analysis

| Column | Analysis Type | Why Interesting? |
|--------|--------------|-----------------|
| Hours of Sleep | Trend analysis | Primary target variable — reveals how actual sleep varies across demographics |
| Sleep Quality | Group comparison | Comparing quality across age groups or occupations uncovers well-being patterns |
| Caffeine Consumption | Correlation analysis | May inversely correlate with sleep duration — a key lifestyle insight |
| Stress Level | Correlation | Stress is a major sleep disruptor; strong analytical pairing |
| Physical Activity | Group comparison | Active individuals likely sleep differently — useful for group comparisons |

### Correlation Heatmap

```python
numeric_df = sleep_df.select_dtypes(include='number')

plt.figure(figsize=(10, 6))
sns.heatmap(numeric_df.corr(), annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap — Sleep Study Dataset', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

### Distribution of Hours of Sleep

```python
plt.figure(figsize=(8, 4))
sns.histplot(sleep_df['Hours of Sleep'].dropna(), bins=15, kde=True, color='steelblue')
plt.title('Distribution of Hours of Sleep', fontweight='bold')
plt.xlabel('Hours of Sleep')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

col = sleep_df['Hours of Sleep'].dropna()
print(f'Mean   : {col.mean():.2f} hrs')
print(f'Median : {col.median():.2f} hrs')
print(f'Mode   : {col.mode().values[0]:.2f} hrs')
```

---

## 🌟 Exercise 6 — Structured vs Unstructured Data

| Data Source | Type | Reason |
|-------------|------|--------|
| Financial reports in an Excel file | ✅ Structured | Tabular rows and columns with a predefined schema — directly queryable |
| Photographs on a social media platform | ❌ Unstructured | Binary image files with no inherent schema or consistent metadata |
| Collection of news articles on a website | ❌ Unstructured | Free-form text with varying length, format, and structure per article |
| Inventory data in a relational database | ✅ Structured | Defined schema, enforced data types, and queryable with SQL |
| Recorded interviews from market research | ❌ Unstructured | Audio recordings require transcription and NLP before any structure exists |

```python
import pandas as pd

classification = pd.DataFrame({
    'Data Source': [
        'Financial reports in an Excel file',
        'Photographs on a social media platform',
        'Collection of news articles on a website',
        'Inventory data in a relational database',
        'Recorded interviews from market research'
    ],
    'Type': [
        '✅ Structured',
        '❌ Unstructured',
        '❌ Unstructured',
        '✅ Structured',
        '❌ Unstructured'
    ],
    'Reason': [
        'Tabular rows and columns with a predefined schema — directly queryable.',
        'Binary image files with no inherent schema or consistent metadata.',
        'Free-form text with varying length, format, and structure per article.',
        'Defined schema, enforced data types, and queryable with SQL.',
        'Audio recordings require transcription and NLP before any structure exists.'
    ]
})

display(classification)
```

---

## 🌟 Exercise 7 — Transformation Exercise

### Proposed Conversion Methods

| Unstructured Source | Method | Resulting Columns |
|--------------------|--------|------------------|
| 📝 Blog posts about travel | NLP (spaCy / NLTK) | `post_id`, `location`, `date_mentioned`, `sentiment_score`, `topics` |
| 🎙️ Audio customer service calls | Speech-to-Text + NLP | `call_id`, `duration`, `issue_category`, `resolution`, `sentiment` |
| ✍️ Handwritten brainstorming notes | OCR (Tesseract / Google Vision) | `idea_id`, `theme`, `keyword`, `participant` |
| 🎬 Cooking video tutorial | STT + Computer Vision | `step_number`, `description`, `timestamp`, `ingredients_used` |

### Explanation

**Blog Posts** — NLP libraries such as spaCy extract named entities (locations, dates), classify topics, and calculate sentiment scores. Each post becomes one structured row.

**Audio Calls** — Tools like OpenAI Whisper or Google Speech-to-Text transcribe speech to text, then NLP classifies the issue category and resolution outcome.

**Handwritten Notes** — OCR converts handwriting to digital text. Keyword extraction and topic modelling then group ideas into themes.

**Cooking Video** — The audio track is transcribed for step descriptions; computer vision identifies ingredients and detects scene changes at each step.

### Demo: Blog Posts → Structured DataFrame

```python
import pandas as pd

raw_blog_posts = [
    "Visited Paris in June 2023. The Eiffel Tower was breathtaking! Loved the food.",
    "Tokyo trip in March was amazing. Cherry blossoms everywhere. A must-visit!",
    "Rome in December was cold but the Colosseum visit was disappointing — too crowded."
]

# Simplified extraction (in practice use spaCy or an LLM)
structured = pd.DataFrame({
    'post_id':   [1, 2, 3],
    'raw_text':  raw_blog_posts,
    'location':  ['Paris', 'Tokyo', 'Rome'],
    'date':      ['June 2023', 'March', 'December'],
    'sentiment': ['Positive', 'Positive', 'Mixed']
})

print('✅ Unstructured blog posts → Structured DataFrame:')
display(structured)
```

---

## 🌟 Exercise 8 — Import a File from Kaggle

### Option A — Direct Download from GitHub (no API needed)

```python
import pandas as pd

url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
titanic_df = pd.read_csv(url)

print(f'✅ Dataset loaded — Shape: {titanic_df.shape}')
print(f'Columns: {titanic_df.columns.tolist()}\n')
display(titanic_df.head())
```

### Option B — Download via Kaggle API

```python
!kaggle competitions download -c titanic --unzip -q
titanic_df = pd.read_csv('train.csv')
display(titanic_df.head())
```

### Quick Inspection

```python
print('Dataset Info:')
titanic_df.info()

print('\nMissing values per column:')
print(titanic_df.isnull().sum())
```

---

## 🌟 Exercise 9 — Export DataFrame to Excel & JSON

### Install Required Library

```python
!pip install openpyxl -q
print('✅ openpyxl ready!')
```

### Create a Simple DataFrame

```python
import pandas as pd

data = {
    'Name':       ['Alice', 'Bob', 'Charlie', 'Diana', 'Ethan'],
    'Age':        [25, 30, 35, 28, 42],
    'Department': ['Engineering', 'Marketing', 'Engineering', 'HR', 'Finance'],
    'Salary':     [72000, 58000, 95000, 61000, 88000],
    'Remote':     [True, False, True, True, False]
}

df = pd.DataFrame(data)
print('📋 Original DataFrame:')
display(df)
```

### Export to Excel

```python
df.to_excel('employees.xlsx', index=False, sheet_name='Staff')
print('✅ Saved to employees.xlsx')

# Verify
df_from_excel = pd.read_excel('employees.xlsx')
display(df_from_excel)
```

### Export to JSON

```python
df.to_json('employees.json', orient='records', indent=4)
print('✅ Saved to employees.json')

# Preview raw JSON
with open('employees.json') as f:
    print(f.read())
```

### Read JSON Back & Download Files

```python
df_from_json = pd.read_json('employees.json')
display(df_from_json)

# Download to your computer (Google Colab only)
from google.colab import files
files.download('employees.xlsx')
files.download('employees.json')
```

---

## 🌟 Exercise 10 — Reading JSON Data from a URL

### Method 1 — pd.read_json() Directly

```python
import pandas as pd

url = 'https://jsonplaceholder.typicode.com/users'

df = pd.read_json(url)
print(f'✅ Loaded — Shape: {df.shape}')
print(f'Columns: {df.columns.tolist()}\n')

print('First 5 entries:')
display(df.head(5))
```

### Method 2 — Using requests

```python
import requests
import pandas as pd

response = requests.get('https://jsonplaceholder.typicode.com/posts')
data = response.json()  # Python list of dicts

posts_df = pd.DataFrame(data)
print(f'Shape: {posts_df.shape}')
display(posts_df.head())
```

### Method 3 — Handling Nested JSON with json_normalize

```python
import requests
import pandas as pd

response = requests.get('https://jsonplaceholder.typicode.com/users')
users_raw = response.json()

# Flatten nested objects (address, company) into columns
flat_df = pd.json_normalize(users_raw)
print(f'Flattened columns: {flat_df.columns.tolist()}')

display(flat_df[['id', 'name', 'email', 'address.city', 'company.name']].head())
```

> 💡 **Tip:** Use `pd.read_json()` for flat JSON arrays. For nested JSON (objects within objects), use `pd.json_normalize()` to flatten the structure before creating your DataFrame.

---

## 🎉 Summary

| # | Topic | Key Skills |
|---|-------|-----------|
| 1 | Introduction to Data Analysis | Conceptual understanding |
| 2 | Dataset Loading | Kaggle API, `pd.read_csv()` |
| 3 | Identifying Data Types | `df.dtypes`, `select_dtypes()` |
| 4 | Iris Dataset Types | Quantitative vs Qualitative classification |
| 5 | Observation Skills | Correlation, Seaborn heatmaps, histograms |
| 6 | Structured vs Unstructured | Data classification reasoning |
| 7 | Data Transformation | NLP, OCR, STT concepts + DataFrame demo |
| 8 | Kaggle / GitHub Import | `pd.read_csv()` from URL |
| 9 | Export to Excel & JSON | `to_excel()`, `to_json()`, `openpyxl` |
| 10 | Reading JSON from URL | `pd.read_json()`, `requests`, `json_normalize()` |

> 💡 **Tip for Colab:** Run cells top-to-bottom. For Exercises 2–5, upload your `kaggle.json` API token first!
