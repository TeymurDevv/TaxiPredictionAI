import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import requests
import os
import threading

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
data = data.dropna(subset=[target_column])

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

# Evaluate the model
y_pred = model.predict(X_test)

# Calculate metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model Evaluation Metrics:")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R² Score: {r2:.2f}")

# Function to generate speech using ElevenLabs API
def generate_speech_in_background(text):
    def generate_speech():
        try:
            api_key = "sk_7bc8a5b430a1c0e9671b2db80d7b55436cde1bdb66ad5242"  # Replace with your ElevenLabs API Key
            voice_id = "fmK7TlnXbQkMPhz8hWek"  # Default voice ID
            
            # ElevenLabs API URL
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            # Payload
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            }
            data = {
                "text": text,
                "voice_settings": {
                    "stability": 0.75,
                    "similarity_boost": 0.75
                }
            }
            
            # API Request
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                # Save the audio file locally
                with open("taxi_price_prediction.mp3", "wb") as f:
                    f.write(response.content)
                print("Speech generated successfully. Saved as 'taxi_price_prediction.mp3'.")
                
                # Automatically play the audio (macOS and Linux)
                os.system("afplay taxi_price_prediction.mp3")  # For macOS
                # For Windows, replace with:
                # os.system("start taxi_price_prediction.mp3")
            else:
                print(f"Error generating speech: {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Start the thread
    threading.Thread(target=generate_speech).start()

# Function to predict price and call ElevenLabs TTS
def predict_price():
    try:
        # Collect input from user
        distance = float(distance_entry.get())
        duration = float(duration_entry.get())
        passenger_count = int(passenger_entry.get())
        base_fare = float(base_fare_entry.get())
        per_km_rate = float(per_km_rate_entry.get())
        per_minute_rate = float(per_minute_rate_entry.get())
        time_of_day = time_entry.get()
        day_of_week = day_entry.get()
        traffic_conditions = traffic_entry.get()
        weather = weather_entry.get()

        # Validate categorical inputs
        if time_of_day not in ["Morning", "Afternoon", "Evening", "Night"]:
            raise ValueError("Invalid Time of Day.")
        if day_of_week not in ["Weekday", "Weekend"]:
            raise ValueError("Invalid Day of Week.")
        if traffic_conditions not in ["Low", "Medium", "High"]:
            raise ValueError("Invalid Traffic Conditions.")
        if weather not in ["Clear", "Rain", "Snow"]:
            raise ValueError("Invalid Weather.")

        # Create a dataframe for prediction
        input_data = pd.DataFrame({
            "Trip_Distance_km": [distance],
            "Trip_Duration_Minutes": [duration],
            "Passenger_Count": [passenger_count],
            "Base_Fare": [base_fare],
            "Per_Km_Rate": [per_km_rate],
            "Per_Minute_Rate": [per_minute_rate],
            "Time_of_Day": [time_of_day],
            "Day_of_Week": [day_of_week],
            "Traffic_Conditions": [traffic_conditions],
            "Weather": [weather]
        })

        # Make prediction
        prediction = model.predict(input_data)
        estimated_price = prediction[0]
        result_text = f"The estimated taxi price is ${estimated_price:.2f}"
        
        # Generate speech in a background thread
        generate_speech_in_background(result_text)
        
        # Show popup
        messagebox.showinfo("Prediction", result_text)

    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to show evaluation metrics
def show_metrics():
    metrics_text = (
        f"Model Evaluation Metrics:\n"
        f"Mean Absolute Error (MAE): {mae:.2f}\n"
        f"Mean Squared Error (MSE): {mse:.2f}\n"
        f"R² Score: {r2:.2f}"
    )
    messagebox.showinfo("Model Metrics", metrics_text)

# GUI setup
app = tk.Tk()
app.title("Taxi Price Prediction")

# Input Fields
distance_label = ttk.Label(app, text="Trip Distance (km):")
distance_label.grid(row=0, column=0, padx=10, pady=10)
distance_entry = ttk.Entry(app)
distance_entry.grid(row=0, column=1, padx=10, pady=10)

duration_label = ttk.Label(app, text="Trip Duration (minutes):")
duration_label.grid(row=1, column=0, padx=10, pady=10)
duration_entry = ttk.Entry(app)
duration_entry.grid(row=1, column=1, padx=10, pady=10)

passenger_label = ttk.Label(app, text="Passenger Count:")
passenger_label.grid(row=2, column=0, padx=10, pady=10)
passenger_entry = ttk.Entry(app)
passenger_entry.grid(row=2, column=1, padx=10, pady=10)

base_fare_label = ttk.Label(app, text="Base Fare:")
base_fare_label.grid(row=3, column=0, padx=10, pady=10)
base_fare_entry = ttk.Entry(app)
base_fare_entry.grid(row=3, column=1, padx=10, pady=10)

per_km_rate_label = ttk.Label(app, text="Per KM Rate:")
per_km_rate_label.grid(row=4, column=0, padx=10, pady=10)
per_km_rate_entry = ttk.Entry(app)
per_km_rate_entry.grid(row=4, column=1, padx=10, pady=10)

per_minute_rate_label = ttk.Label(app, text="Per Minute Rate:")
per_minute_rate_label.grid(row=5, column=0, padx=10, pady=10)
per_minute_rate_entry = ttk.Entry(app)
per_minute_rate_entry.grid(row=5, column=1, padx=10, pady=10)

time_label = ttk.Label(app, text="Time of Day:")
time_label.grid(row=6, column=0, padx=10, pady=10)
time_entry = ttk.Combobox(app, values=["Morning", "Afternoon", "Evening", "Night"])
time_entry.grid(row=6, column=1, padx=10, pady=10)

day_label = ttk.Label(app, text="Day of Week:")
day_label.grid(row=7, column=0, padx=10, pady=10)
day_entry = ttk.Combobox(app, values=["Weekday", "Weekend"])
day_entry.grid(row=7, column=1, padx=10, pady=10)

traffic_label = ttk.Label(app, text="Traffic Conditions:")
traffic_label.grid(row=8, column=0, padx=10, pady=10)
traffic_entry = ttk.Combobox(app, values=["Low", "Medium", "High"])
traffic_entry.grid(row=8, column=1, padx=10, pady=10)

weather_label = ttk.Label(app, text="Weather:")
weather_label.grid(row=9, column=0, padx=10, pady=10)
weather_entry = ttk.Combobox(app, values=["Clear", "Rain", "Snow"])
weather_entry.grid(row=9, column=1, padx=10, pady=10)

predict_button = ttk.Button(app, text="Predict Price", command=predict_price)
predict_button.grid(row=10, column=0, columnspan=2, pady=20)

metrics_button = ttk.Button(app, text="Show Metrics", command=show_metrics)
metrics_button.grid(row=11, column=0, columnspan=2, pady=20)

app.mainloop()