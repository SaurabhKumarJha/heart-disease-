import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
import joblib
import numpy as np

# Create dummy data for demonstration
X = np.array([[63, 1, 3, 145, 233, 1] + [0]*7 for _ in range(100)])  # 100 samples with dummy values
y = np.random.randint(0, 2, 100)  # Random binary outcomes

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = DummyClassifier(strategy='most_frequent')
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# Save model
joblib.dump(model, 'model.pkl')

print("Model trained and saved successfully!")