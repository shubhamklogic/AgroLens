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
# DATA STORAGE FUNCTION
# Saves every prediction result to results.json
# This acts like a log file for all predictions
# -------------------------------------------------
def save_prediction_result(data):
    """
    Saves the prediction inputs and outputs to a JSON file.
    This is useful for:
    - reporting
    - evaluation
    - dataset creation for future ML training
    """

    # Path to data/results.json
    file_path = os.path.join(os.path.dirname(__file__), "data", "results.json")

    # List that will hold all past prediction records
    results = []

    # -------------------------------------------------
    # STEP 1: READ EXISTING FILE (if it exists)
    # This ensures we don't overwrite old predictions
    # -------------------------------------------------
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                results = json.load(f)
        except Exception:
            # If file is corrupted or empty
            results = []

    # -------------------------------------------------
    # STEP 2: ADD TIMESTAMP
    # Helps track when the prediction was made
    # -------------------------------------------------
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Add new prediction entry
    results.append(data)

    # -------------------------------------------------
    # STEP 3: SAVE BACK TO FILE
    # -------------------------------------------------
    try:
        with open(file_path, "w") as f:
            json.dump(results, f, indent=4)

        print("📊 Prediction result saved to results.json")

    except Exception as e:
        print(f"⚠️ Error saving result: {e}")


# -------------------------------------------------
# PREDICTION API
# -------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():

    # Get JSON data from request body
    user_data = request.get_json(silent=True) or {}

    # -------------------------------------------------
    # STEP 1: INPUT VALIDATION (Coordinates Required)
    # -------------------------------------------------
    if "lat" not in user_data or "lon" not in user_data:
        return jsonify({
            "status": "error",
            "message": "Missing required coordinates: 'lat' and 'lon' are required."
        }), 400

    # Extract input parameters
    crop = user_data.get("crop", "wheat").capitalize()
    lat = user_data.get("lat")
    lon = user_data.get("lon")

    # -------------------------------------------------
    # STEP 2: DATA TYPE VALIDATION
    # Validates soil pH value
    # -------------------------------------------------
    try:
        soil_ph = float(user_data.get("soil_ph", 6.5))

        if not (0 <= soil_ph <= 14):
            raise ValueError("pH must be between 0 and 14")

    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "message": "Invalid 'soil_ph'. Please provide a numeric value between 0 and 14."
        }), 422

    # -------------------------------------------------
    # STEP 3: WEATHER SERVICE CALL
    # Fetch weather data using latitude and longitude
    # -------------------------------------------------
    try:
        weather = get_weather_data(lat=lat, lon=lon)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Critical failure connecting to weather service: {str(e)}"
        }), 503

    # Handle weather API failure
    if weather.get("status") == "error":
        return jsonify({
            "status": "error",
            "message": "Weather service returned an error. Please check coordinates."
        }), 502

    avg_temp = weather["avg_temp"]
    total_rain = weather["total_rain"]

    # -------------------------------------------------
    # PREPARE FEATURES FOR ML MODEL
    # Format expected by sklearn model
    # -------------------------------------------------
    features = [[avg_temp, total_rain, soil_ph]]

    # -------------------------------------------------
    # MODEL PREDICTION SECTION
    # -------------------------------------------------
    try:
        if model and hasattr(model, "predict"):
            prediction = model.predict(features)
            predicted_yield = float(prediction[0])
        else:
            # fallback prediction logic if model is missing
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

    # -------------------------------------------------
    # FINAL RESPONSE PAYLOAD
    # This will be returned to the client
    # -------------------------------------------------
    response_payload = {
        "status": "success",
        "crop": crop,
        "inputs": {
            "lat": lat,
            "lon": lon,
            "temp": avg_temp,
            "rain": total_rain,
            "soil_ph": soil_ph
        },
        "prediction": round(predicted_yield, 2),
        "advisory": advisory_data["advice"]
    }

    # -------------------------------------------------
    # SAVE PREDICTION RESULT
    # Logs the prediction into data/results.json
    # Useful for evaluation and reporting
    # -------------------------------------------------
    save_prediction_result(response_payload)

    return jsonify(response_payload)


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
# WEATHER API (New Endpoint)
# -------------------------------------------------
@app.route("/weather", methods=["GET"])
def weather_api():

    # Extract latitude and longitude from URL parameters
    lat = request.args.get("lat", default=28.6, type=float)
    lon = request.args.get("lon", default=77.2, type=float)

    # Call weather helper function
    weather = get_weather_data(lat=lat, lon=lon)

    if weather["status"] == "success":
        return jsonify({
            "status": "success",
            "location": {"lat": lat, "lon": lon},
            "data": {
                "avg_temp": weather["avg_temp"],
                "total_rain": weather["total_rain"]
            }
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Weather data could not be retrieved"
        }), 500


# -------------------------------------------------
# RUN SERVER
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)