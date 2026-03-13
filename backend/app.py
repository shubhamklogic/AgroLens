from flask import Flask, jsonify, request
from utils import get_weather_data
from datetime import datetime
import pickle
import os
import json

app = Flask(__name__)

# -------------------------------------------------
# MODEL LOADING SECTION
# Loads the trained ML model from model.pkl
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

model = load_model()

# -------------------------------------------------
# PREDICTION API
# This endpoint receives user input and returns
# yield prediction + advisory reasoning
# -------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    
    # Get JSON data from request body
    user_data = request.get_json(silent=True) or {}

    # Extract input parameters (with defaults)
    crop = user_data.get("crop", "wheat").capitalize()
    lat = user_data.get("lat", 28.6)
    lon = user_data.get("lon", 77.2)
    soil_ph = user_data.get("soil_ph", 6.5)

    # Fetch weather data using helper utility
    weather = get_weather_data(lat=lat, lon=lon)

    if weather["status"] == "error":
        return jsonify({
            "status": "error",
            "message": "Weather service unavailable"
        }), 500

    # Extract weather parameters
    avg_temp = weather["avg_temp"]
    total_rain = weather["total_rain"]

    # Prepare model features
    features = [[avg_temp, total_rain, soil_ph]]

    # -------------------------------------------------
    # MODEL PREDICTION SECTION
    # Uses ML model if available, otherwise fallback logic
    # -------------------------------------------------
    try:
        if model and hasattr(model, "predict"):
            prediction = model.predict(features)
            predicted_yield = float(prediction[0])
        else:
            # Dummy fallback prediction
            predicted_yield = (avg_temp * 10) + (total_rain * 5) - (soil_ph * 2)
            print("DEBUG: Using Dummy/Mock prediction logic")

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Prediction failed: {e}"
        }), 500

    # -------------------------------------------------
    # ADVISORY LOGIC SECTION
    # Converts model output into human readable advice
    # -------------------------------------------------

    # For now assume rainfall is the most important feature
    top_feature = "rainfall"

    # Call advisory function
    advisory_data = generate_advisory(
        predicted_yield,
        avg_temp,
        total_rain,
        soil_ph,
        top_feature
    )

    # -------------------------------------------------
    # FINAL API RESPONSE
    # Returns prediction + advisory reasoning
    # -------------------------------------------------
    return jsonify({
        "status": "success",
        "prediction": round(predicted_yield, 2),
        "advisory": advisory_data["advice"],
        "reasoning": f"Based on {advisory_data['primary_factor']} importance"
    })


# -------------------------------------------------
# EVALUATION API SECTION
# Returns saved model performance metrics
# -------------------------------------------------
@app.route("/metrics", methods=["GET"])
def metrics_api():

    metrics_path = "metrics.json"

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
# ADVISORY GENERATION FUNCTION
# Converts ML numbers into farming advice
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
# RUN SERVER
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)