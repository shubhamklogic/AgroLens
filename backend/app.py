from flask import Flask, jsonify, request
from utils import get_weather_data
from datetime import datetime
import pickle
import os

app = Flask(__name__)

# ---------------------------------------------------
# Load ML Model ONCE when server starts
# ---------------------------------------------------

MODEL_PATH = "model.pkl"

def load_prediction_model():
    if not os.path.exists(MODEL_PATH):
        print("ERROR: model.pkl not found!")
        return None

    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print("Model load failed:", e)
        return None

model = load_prediction_model()

# ---------------------------------------------------
# Prediction API
# ---------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    # 1. Read Input
    user_data = request.get_json(silent=True) or {}

    crop = user_data.get("crop", "unknown").capitalize()
    lat = user_data.get("lat", 26.91)   # Jaipur default
    lon = user_data.get("lon", 75.78)
    soil_ph = user_data.get("soil_ph", 6.5)

    # 2. Validate Coordinates
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return jsonify({
            "status": "error",
            "message": "Invalid coordinates"
        }), 400

    # 3. Fetch Weather
    weather = get_weather_data(lat=lat, lon=lon)

    if weather["status"] == "error":
        return jsonify({
            "status": "error",
            "message": "Weather service unavailable"
        }), 500

    # 4. Extract Values
    temp = weather["avg_temp"]
    rain = weather["total_rain"]

    # ---------------------------------------------------
    # 5. CREATE FEATURE VECTOR (2D ARRAY)
    # ---------------------------------------------------
    features = [[temp, rain, soil_ph]]

    print(f"DEBUG Features -> {features}")

    # ---------------------------------------------------
    # 6. Prediction
    # ---------------------------------------------------

    if model:
        predicted_yield = int(model.predict(features)[0])
    else:
        # fallback dummy logic
        predicted_yield = 3200 if temp < 28 else 2700

    # ---------------------------------------------------
    # 7. Recommendation
    # ---------------------------------------------------

    if rain > 10:
        advice = f"High rainfall ({rain} mm). Avoid extra irrigation."
    elif temp > 30:
        advice = f"High temperature ({temp} °C). Maintain soil moisture."
    else:
        advice = f"Weather conditions are stable for {crop}."

    # ---------------------------------------------------
    # 8. Response
    # ---------------------------------------------------

    return jsonify({
        "status": "success",
        "metadata": {
            "crop": crop,
            "location": {
                "lat": lat,
                "lon": lon
            },
            "timestamp": datetime.utcnow().isoformat()
        },
        "analysis": {
            "temperature": temp,
            "rainfall": rain,
            "soil_ph": soil_ph,
            "predicted_yield": predicted_yield
        },
        "recommendation": advice
    })

# ---------------------------------------------------
# Start Server
# ---------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)