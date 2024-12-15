from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import os

# Load the dataset
try:
    data_path = "./taxi_trip_pricing.csv"  # Ensure the file exists in this location
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Please check the path.")
    
    # Read the dataset
    data = pd.read_csv(data_path)
    print("Dataset loaded successfully.")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

# Define feature columns and target column
numeric_features = [
    "Trip_Distance_km", "Trip_Duration_Minutes", "Passenger_Count", 
    "Base_Fare", "Per_Km_Rate", "Per_Minute_Rate"
]
categorical_features = ["Time_of_Day", "Day_of_Week", "Traffic_Conditions", "Weather"]
target_column = "Trip_Price"

# Check for missing values in the target column
print(f"Missing values in target column before cleaning: {data[target_column].isna().sum()}")

# Drop rows with missing target values
data = data.dropna(subset=[target_column])
print(f"Missing values in target column after cleaning: {data[target_column].isna().sum()}")

# Reassign features and target after cleaning
X = data[numeric_features + categorical_features]
y = data[target_column]

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessing pipeline for numeric and categorical features
numeric_transformer = SimpleImputer(strategy="mean")
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)

# Model pipeline
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train the model
print("Training the model...")
model.fit(X_train, y_train)
print("Model training complete.")

# Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

@app.route('/predict', methods=['POST'])
def predict_price():
    try:
        # Parse JSON input
        input_data = request.get_json()

        # Check required fields
        required_fields = numeric_features + categorical_features
        missing_fields = [field for field in required_fields if field not in input_data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {missing_fields}"}), 400

        # Create a DataFrame for prediction
        input_df = pd.DataFrame([input_data])

        # Make prediction
        prediction = model.predict(input_df)
        estimated_price = prediction[0]

        # Return result as JSON
        return jsonify({"estimated_price": round(estimated_price, 2)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the server
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")  # Host set to 0.0.0.0 for all network interfaces