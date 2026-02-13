from flask import Flask, jsonify, request
from utils import get_weather_data
from datetime import datetime
import pickle
import os

app = Flask(__name__)

# -------------------------------------------------
# MODEL LOADING SECTION
# Load the pre-trained model once at startup to save resources [cite: 10, 24]
# -------------------------------------------------

def load_model():
    model_path = "model.pkl"
    if os.path.exists(model_path):
        try:
            with open(model_path, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading model: {e}")
    return None

# Model is loaded only once when server starts
model = load_model()


# -------------------------------------------------
# PREDICTION API
# -------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    # -------------------------------------------------
    # Step 1: Extract data from the frontend request [cite: 48, 55]
    # Read JSON input safely and assign default values
    # -------------------------------------------------
    user_data = request.get_json(silent=True) or {}

    crop = user_data.get("crop", "wheat").capitalize()
    lat = user_data.get("lat", 28.6)
    lon = user_data.get("lon", 77.2)
    soil_ph = user_data.get("soil_ph", 6.5)


    # -------------------------------------------------
    # Step 2: Fetch meteorological data (Weather) using coordinates [cite: 56]
    # -------------------------------------------------
    weather = get_weather_data(lat=lat, lon=lon)
    if weather["status"] == "error":
        return jsonify({"status": "error", "message": "Weather service unavailable"}), 500

    avg_temp = weather["avg_temp"]
    total_rain = weather["total_rain"]


    # -------------------------------------------------
    # Step 3: Format inputs into a 2D Feature Vector for the ML model [cite: 31, 57]
    # -------------------------------------------------
    # ML models expect input in 2D array format
    # [[temperature, rainfall, soil_ph]]
    features = [[avg_temp, total_rain, soil_ph]]


    # -------------------------------------------------
    # Step 4: Perform inference and return the JSON response [cite: 58, 59]
    # -------------------------------------------------
    try:
        if model and hasattr(model, "predict"):
            # Real ML model prediction
            prediction = model.predict(features)
            predicted_yield = float(prediction[0])
        else:
            # Dummy logic used if model is not available
            predicted_yield = (avg_temp * 10) + (total_rain * 5) - (soil_ph * 2)
            print("DEBUG: Using Dummy/Mock prediction logic")

    except Exception as e:
        return jsonify({"status": "error", "message": f"Prediction failed: {e}"}), 500


    # -------------------------------------------------
    # Recommendation Logic (Week 2)
    # -------------------------------------------------
    if total_rain > 10:
        advice = f"High rainfall ({total_rain} mm) detected. Avoid extra irrigation."
    else:
        advice = f"Weather stable for {crop}. Maintain standard soil moisture."


    # -------------------------------------------------
    # Final Structured JSON Response
    # -------------------------------------------------
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


# -------------------------------------------------
# RUN SERVER
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)