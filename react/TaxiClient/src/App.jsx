import React, { useState } from "react";
import Swal from "sweetalert2";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [formData, setFormData] = useState({
    Trip_Distance_km: "",
    Trip_Duration_Minutes: "",
    Passenger_Count: "",
    Base_Fare: "",
    Per_Km_Rate: "",
    Per_Minute_Rate: "",
    Time_of_Day: "",
    Day_of_Week: "",
    Traffic_Conditions: "",
    Weather: "",
  });

  // Placeholder values for ElevenLabs API Key and Voice ID
  const ELEVEN_LABS_API_KEY = "sk_7bc8a5b430a1c0e9671b2db80d7b55436cde1bdb66ad5242";
  const VOICE_ID = "fmK7TlnXbQkMPhz8hWek";

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const playVoice = async (text) => {
    try {
      const response = await axios.post(
        `https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`,
        { text },
        {
          headers: {
            "Content-Type": "application/json",
            "xi-api-key": ELEVEN_LABS_API_KEY,
          },
          responseType: "arraybuffer", // Ensure we receive audio data
        }
      );

      // Convert response to an audio blob and play it
      const audioBlob = new Blob([response.data], { type: "audio/mpeg" });
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Error playing voice: " + error.message,
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      const message = `The estimated taxi fare is ${data.estimated_price} dollars.`;

      Swal.fire({
        icon: "success",
        title: "Success!",
        text: message,
        confirmButtonText: "OK",
      });

      // Call ElevenLabs TTS to play the message
      playVoice(message);
    } catch (err) {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: `Error: ${err.message}`,
        confirmButtonText: "Try Again",
      });
    }
  };

  return (
    <div className="d-flex align-items-center justify-content-center vh-100 bg-light">
      <div className="card p-4 shadow" style={{ width: "100%", maxWidth: "500px" }}>
        <h1 className="text-center mb-4">Trip Fare Calculator</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="Trip_Distance_km" className="form-label">
              Trip Distance (km)
            </label>
            <input
              type="number"
              step="0.1"
              className="form-control"
              id="Trip_Distance_km"
              name="Trip_Distance_km"
              value={formData.Trip_Distance_km}
              onChange={handleChange}
              placeholder="Enter trip distance"
            />
          </div>
          <div className="mb-3">
            <label htmlFor="Trip_Duration_Minutes" className="form-label">
              Trip Duration (minutes)
            </label>
            <input
              type="number"
              step="0.1"
              className="form-control"
              id="Trip_Duration_Minutes"
              name="Trip_Duration_Minutes"
              value={formData.Trip_Duration_Minutes}
              onChange={handleChange}
              placeholder="Enter trip duration"
            />
          </div>
          <div className="mb-3">
            <label htmlFor="Passenger_Count" className="form-label">
              Passenger Count
            </label>
            <input
              type="number"
              className="form-control"
              id="Passenger_Count"
              name="Passenger_Count"
              value={formData.Passenger_Count}
              onChange={handleChange}
              placeholder="Enter passenger count"
            />
          </div>
          <div className="mb-3">
            <label htmlFor="Base_Fare" className="form-label">
              Base Fare
            </label>
            <input
              type="number"
              step="0.1"
              className="form-control"
              id="Base_Fare"
              name="Base_Fare"
              value={formData.Base_Fare}
              onChange={handleChange}
              placeholder="Enter base fare"
            />
          </div>
          <div className="mb-3">
            <label htmlFor="Per_Km_Rate" className="form-label">
              Per Km Rate
            </label>
            <input
              type="number"
              step="0.1"
              className="form-control"
              id="Per_Km_Rate"
              name="Per_Km_Rate"
              value={formData.Per_Km_Rate}
              onChange={handleChange}
              placeholder="Enter per km rate"
            />
          </div>
          <div className="mb-3">
            <label htmlFor="Per_Minute_Rate" className="form-label">
              Per Minute Rate
            </label>
            <input
              type="number"
              step="0.1"
              className="form-control"
              id="Per_Minute_Rate"
              name="Per_Minute_Rate"
              value={formData.Per_Minute_Rate}
              onChange={handleChange}
              placeholder="Enter per minute rate"
            />
          </div>
          <div className="mb-3">
            <label htmlFor="Time_of_Day" className="form-label">
              Time of Day
            </label>
            <select
              className="form-select"
              id="Time_of_Day"
              name="Time_of_Day"
              value={formData.Time_of_Day}
              onChange={handleChange}
            >
              <option value="" disabled>
                Select time of day
              </option>
              <option value="Morning">Morning</option>
              <option value="Afternoon">Afternoon</option>
              <option value="Evening">Evening</option>
              <option value="Night">Night</option>
            </select>
          </div>
          <div className="mb-3">
            <label htmlFor="Day_of_Week" className="form-label">
              Day of Week
            </label>
            <select
              className="form-select"
              id="Day_of_Week"
              name="Day_of_Week"
              value={formData.Day_of_Week}
              onChange={handleChange}
            >
              <option value="" disabled>
                Select day of week
              </option>
              <option value="Weekday">Weekday</option>
              <option value="Weekend">Weekend</option>
            </select>
          </div>
          <div className="mb-3">
            <label htmlFor="Traffic_Conditions" className="form-label">
              Traffic Conditions
            </label>
            <select
              className="form-select"
              id="Traffic_Conditions"
              name="Traffic_Conditions"
              value={formData.Traffic_Conditions}
              onChange={handleChange}
            >
              <option value="" disabled>
                Select traffic conditions
              </option>
              <option value="Low">Light</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </div>
          <div className="mb-3">
            <label htmlFor="Weather" className="form-label">
              Weather
            </label>
            <select
              className="form-select"
              id="Weather"
              name="Weather"
              value={formData.Weather}
              onChange={handleChange}
            >
              <option value="" disabled>
                Select weather
              </option>
              <option value="Clear">Clear</option>
              <option value="Rain">Rain</option>
              <option value="Snow">Snow</option>
            </select>
          </div>
          <button type="submit" className="btn btn-primary w-100">
            Submit
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;