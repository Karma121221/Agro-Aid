import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load the dataset (update 'your_data.csv' with your actual filename)
df = pd.read_csv('your_data.csv')

# Prepare features and target:
# Assuming 'Plant_Health_Status' is the label and we drop 'Timestamp' and 'Plant_ID'
X = df.drop(['Timestamp', 'Plant_ID', 'Plant_Health_Status'], axis=1)
y = df['Plant_Health_Status']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Optionally, evaluate the model on test data
score = rf_model.score(X_test, y_test)
print(f"Model accuracy: {score:.2f}")

# Save the trained model to a file
joblib.dump(rf_model, 'plant_stress_rf_model.pkl')
print("Model saved as 'plant_stress_rf_model.pkl'")
