import pandas as pd
from sklearn.model_selection import train_test_split

# Load the dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"

columns = [
    'Pregnancies',
    'Glucose',
    'BloodPressure',
    'SkinThickness',
    'Insulin',
    'BMI',
    'DiabetesPedigreeFunction',
    'Age',
    'Outcome'
]

diabetes = pd.read_csv(url, names=columns)

# Explore the data
print("First 5 rows:")
print(diabetes.head())

print("\nDataset info:")
print(diabetes.info())

print("\nStatistical summary:")
print(diabetes.describe())

# Count positive and negative diabetes cases
print("\nOutcome counts:")
print(diabetes['Outcome'].value_counts())

# Separate features and target
X = diabetes.drop('Outcome', axis=1)
y = diabetes['Outcome']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Check sizes
print("\nTraining set size:", X_train.shape)
print("Testing set size:", X_test.shape)
