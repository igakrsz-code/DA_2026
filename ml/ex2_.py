from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

# Fit ONLY on training data
X_train_scaled = scaler.fit_transform(X_train)

# Transform test data using the same scaler
X_test_scaled = scaler.transform(X_test)


import numpy as np

print("Train mean (should be ~0):", np.mean(X_train_scaled, axis=0))
print("Train std (should be ~1):", np.std(X_train_scaled, axis=0))