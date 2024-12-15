import tkinter as tk
from tkinter import ttk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Load the dataset
data_path = "./taxi_trip_pricing.csv"
data = pd.read_csv(data_path)

# Define feature columns and target column
numeric_features = [
    "Trip_Distance_km", "Trip_Duration_Minutes", "Passenger_Count", 
    "Base_Fare", "Per_Km_Rate", "Per_Minute_Rate"
]
categorical_features = ["Time_of_Day", "Day_of_Week", "Traffic_Conditions", "Weather"]
target_column = "Trip_Price"

# Drop rows with missing target values
data = data.dropna(subset=[target_column])

# Function to plot statistics
def show_statistics():
    stats_window = tk.Toplevel(app)
    stats_window.title("Dataset Statistics")

    # Display summary statistics
    stats_text = tk.Text(stats_window, wrap="word", height=15, width=60)
    stats_text.pack(pady=10)
    stats_text.insert("1.0", data.describe(include="all").to_string())

    # Create a matplotlib figure for graphs
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))

    # Plot 1: Trip Price Distribution
    ax[0, 0].hist(data[target_column], bins=20, color="skyblue", edgecolor="black")
    ax[0, 0].set_title("Trip Price Distribution")
    ax[0, 0].set_xlabel("Price")
    ax[0, 0].set_ylabel("Frequency")

    # Plot 2: Trip Distance vs. Price
    ax[0, 1].scatter(data["Trip_Distance_km"], data[target_column], alpha=0.5, color="green")
    ax[0, 1].set_title("Trip Distance vs. Price")
    ax[0, 1].set_xlabel("Distance (km)")
    ax[0, 1].set_ylabel("Price")

    # Plot 3: Average Price by Time of Day
    avg_price_by_time = data.groupby("Time_of_Day")[target_column].mean()
    avg_price_by_time.plot(kind="bar", ax=ax[1, 0], color="orange", edgecolor="black")
    ax[1, 0].set_title("Average Price by Time of Day")
    ax[1, 0].set_xlabel("Time of Day")
    ax[1, 0].set_ylabel("Average Price")

    # Plot 4: Average Price by Day of Week
    avg_price_by_day = data.groupby("Day_of_Week")[target_column].mean()
    avg_price_by_day.plot(kind="bar", ax=ax[1, 1], color="purple", edgecolor="black")
    ax[1, 1].set_title("Average Price by Day of Week")
    ax[1, 1].set_xlabel("Day of Week")
    ax[1, 1].set_ylabel("Average Price")

    plt.tight_layout()

    # Embed the plot into the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=stats_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Create the GUI
app = tk.Tk()
app.title("Taxi Price Statistics")

# Statistics Button
stats_button = ttk.Button(app, text="Show Statistics", command=show_statistics)
stats_button.pack(pady=20)

app.mainloop()