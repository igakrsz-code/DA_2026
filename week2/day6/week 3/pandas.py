# Load the Iris dataset from sklearn (it's built-in)
from sklearn.datasets import load_iris

# Load the raw data
iris_data = load_iris()

# Create a DataFrame
df = pd.DataFrame(
    data=iris_data.data,
    columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
)

# Add the species column
# Convert numbers (0,1,2) to names (setosa, versicolor, virginica)
df['species'] = [iris_data.target_names[i] for i in iris_data.target]

# Show that it worked
print(f"Dataset loaded successfully!")
print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")