from flask import Flask, jsonify, request
from utils.fetch_weather import get_weather_data
from datetime import datetime
import pickle
import os
import json

app = Flask(__name__)

# -------------------------------------------------
# MODEL INITIALIZATION
# Loads the trained ML model from model.pkl
# -------------------------------------------------
def load_trained_model():

    # Path to model.pkl in project root
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

    if os.path.exists(model_path):
        try:
            with open(model_path, "rb") as f:
                print("✅ Model loaded successfully.")
                return pickle.load(f)
        except Exception as e:
            print(f"⚠️ Error loading model file: {e}")
    else:
        print("⚠️ model.pkl not found. Using internal fallback logic.")

    return None


# Load model once when server starts
model = load_trained_model()


# -------------------------------------------------
# PREDICTION API
# -------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():

    # Get JSON data from request body
    user_data = request.get_json(silent=True) or {}

    # Extract input parameters
    crop = user_data.get("crop", "wheat").capitalize()
    lat = user_data.get("lat", 28.6)
    lon = user_data.get("lon", 77.2)
    soil_ph = user_data.get("soil_ph", 6.5)

    # Fetch weather data
    weather = get_weather_data(lat=lat, lon=lon)

    if weather["status"] == "error":
        return jsonify({
            "status": "error",
            "message": "Weather service unavailable"
        }), 500

    avg_temp = weather["avg_temp"]
    total_rain = weather["total_rain"]

    # Prepare features for model
    features = [[avg_temp, total_rain, soil_ph]]

    # -------------------------------------------------
    # MODEL PREDICTION SECTION
    # -------------------------------------------------
    try:
        if model and hasattr(model, "predict"):
            prediction = model.predict(features)
            predicted_yield = float(prediction[0])
        else:
            # fallback prediction
            predicted_yield = (avg_temp * 10) + (total_rain * 5) - (soil_ph * 2)
            print("DEBUG: Using Dummy/Mock prediction logic")

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Prediction failed: {e}"
        }), 500

    # -------------------------------------------------
    # ADVISORY LOGIC
    # -------------------------------------------------

    top_feature = "rainfall"

    advisory_data = generate_advisory(
        predicted_yield,
        avg_temp,
        total_rain,
        soil_ph,
        top_feature
    )

    return jsonify({
        "status": "success",
        "prediction": round(predicted_yield, 2),
        "advisory": advisory_data["advice"],
        "reasoning": f"Based on {advisory_data['primary_factor']} importance"
    })


# -------------------------------------------------
# METRICS API
# -------------------------------------------------
@app.route("/metrics", methods=["GET"])
def metrics_api():

    # Updated path to data/metrics.json
    metrics_path = os.path.join(os.path.dirname(__file__), "data", "metrics.json")

    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, "r") as f:
                metrics_data = json.load(f)

            return jsonify({
                "status": "success",
                "data": metrics_data
            }), 200

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Failed to read metrics: {e}"
            }), 500

    else:
        return jsonify({
            "status": "error",
            "message": "Metrics file not found. Please run evaluation first."
        }), 404


# -------------------------------------------------
# ADVISORY FUNCTION
# -------------------------------------------------
def generate_advisory(predicted_yield, avg_temp, total_rain, soil_ph, top_feature):

    advice = ""

    if total_rain < 100:
        advice = "Low rainfall detected. Increase irrigation to maintain yield."

    elif avg_temp > 30:
        advice = "High temperature warning. Consider using mulch to keep soil cool."

    elif soil_ph < 6.0:
        advice = "Soil is acidic. Consider adding lime to balance pH levels."

    else:
        advice = "Conditions are optimal for current crop growth."

    return {
        "advice": advice,
        "primary_factor": top_feature
    }


# -------------------------------------------------
# ADVISORY API
# -------------------------------------------------
@app.route("/advisory", methods=["POST"])
def advisory_api():

    try:
        user_data = request.get_json(silent=True) or {}

        temp = user_data.get("temp", 25.0)
        rain = user_data.get("rain", 150.0)
        ph = user_data.get("soil_ph", 6.5)
        predicted_yield = user_data.get("predicted_yield", 3000.0)

        important_feature = "rainfall" if rain < 100 else "temperature"

        if rain < 100:
            advice = "Low rainfall detected. Increase irrigation."
        elif temp > 32:
            advice = "Heat stress likely. Ensure adequate soil moisture."
        else:
            advice = "Conditions are stable. Follow standard crop cycle."

        return jsonify({
            "status": "success",
            "advice": advice,
            "important_feature": important_feature,
            "impact_level": "High"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# -------------------------------------------------
# RUN SERVER
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)