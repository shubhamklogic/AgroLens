from flask import Flask, jsonify, request
from utils import get_weather_data
from datetime import datetime
import pickle
import os

app = Flask(__name__)

# --- MODEL LOADING SECTION ---
def load_model():
    model_path = "model.pkl"
    if os.path.exists(model_path):
        try:
            with open(model_path, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading model: {e}")
    return None

# Load the model once when the server starts
model = load_model()

@app.route("/predict", methods=["POST"])
def predict():
    # Read input safely
    user_data = request.get_json(silent=True) or {}

    # Standardizing inputs
    crop = user_data.get("crop", "wheat").capitalize()
    lat = user_data.get("lat", 28.6)
    lon = user_data.get("lon", 77.2)
    soil_ph = user_data.get("soil_ph", 6.5)

    # 2. Fetch live weather data
    weather = get_weather_data(lat=lat, lon=lon)
    if weather["status"] == "error":
        return jsonify({"status": "error", "message": "Weather service unavailable"}), 500

    avg_temp = weather["avg_temp"]
    total_rain = weather["total_rain"]

    # 3. FEATURE FORMATTING (Feb 2 Task)
    # Creating the 2D array: [[temp, rain, ph]]
    features = [[avg_temp, total_rain, soil_ph]]

    # 4. PREDICTION LOGIC (Feb 3 Task)
    try:
        if model and hasattr(model, 'predict'):
            # Real model prediction
            prediction = model.predict(features)
            predicted_yield = float(prediction[0])
        else:
            # DUMMY LOGIC (Since we are using your placeholder data)
            # Simulated calculation: (Temp * 10) + (Rain * 5) - (pH * 2)
            predicted_yield = (avg_temp * 10) + (total_rain * 5) - (soil_ph * 2)
            print("DEBUG: Using Dummy/Mock prediction logic")
    except Exception as e:
        return jsonify({"status": "error", "message": f"Prediction failed: {e}"}), 500

    # 5. Recommendation Logic (From Week 2)
    if total_rain > 10:
        advice = f"High rainfall ({total_rain} mm) detected. Avoid extra irrigation."
    else:
        advice = f"Weather stable for {crop}. Maintain standard soil moisture."

    # 6. Final Structured Response
    return jsonify({
        "status": "success",
        "metadata": {
            "crop": crop,
            "location": {"lat": lat, "lon": lon},
            "timestamp": datetime.utcnow().isoformat()
        },
        "analysis": {
            "avg_temp": avg_temp,
            "total_rain": total_rain,
            "soil_ph": soil_ph,
            "predicted_yield": round(predicted_yield, 2)
        },
        "recommendation": advice
    })

if __name__ == "__main__":
    app.run(debug=True)