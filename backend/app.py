from flask import Flask, jsonify, request
from utils.fetch_weather import get_weather_data
from datetime import datetime
import pickle
import os
import json

app = Flask(__name__)

# -------------------------------------------------
# MODEL INITIALIZATION
# This function loads the trained ML model
# when the backend server starts.
# This avoids loading the model again and again.
# -------------------------------------------------
def load_trained_model():

    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

    if os.path.exists(model_path):

        try:
            with open(model_path, "rb") as f:
                print("✅ Model loaded successfully.")
                return pickle.load(f)

        except Exception as e:
            print(f"⚠️ Error loading model file: {e}")

    else:
        print("⚠️ model.pkl not found. Using fallback logic.")

    return None


# Global model variable
model = load_trained_model()


# -------------------------------------------------
# DATA STORAGE FUNCTION
# Saves prediction results into data/results.json
# This helps for future analysis and model tracking
# -------------------------------------------------
def save_prediction_result(data):

    file_path = os.path.join(os.path.dirname(__file__), "data", "results.json")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    results = []

    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                results = json.load(f)
        except Exception:
            results = []

    # Add timestamp
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    results.append(data)

    try:
        with open(file_path, "w") as f:
            json.dump(results, f, indent=4)

        print("📊 Prediction result saved")

    except Exception as e:
        print(f"⚠️ Error saving result: {e}")


# -------------------------------------------------
# PREDICTION API
# Predicts yield for a specific crop
# -------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():

    user_data = request.get_json(silent=True) or {}

    # Validate coordinates
    if "lat" not in user_data or "lon" not in user_data:
        return jsonify({
            "status": "error",
            "message": "Missing lat/lon."
        }), 400

    crop = user_data.get("crop", "wheat").capitalize()

    lat = user_data.get("lat")
    lon = user_data.get("lon")

    # Soil type encoding (default = Loamy soil)
    soil_type = user_data.get("soil_type", 2)

    # Validate soil pH
    try:
        soil_ph = float(user_data.get("soil_ph", 6.5))

        if not (0 <= soil_ph <= 14):
            raise ValueError

    except:
        return jsonify({
            "status": "error",
            "message": "Invalid soil_ph."
        }), 422

    # Fetch weather data from NASA API
    weather = get_weather_data(lat=lat, lon=lon)

    if weather.get("status") == "error":
        return jsonify({
            "status": "error",
            "message": "Weather service failed"
        }), 502

    avg_temp = weather["avg_temp"]
    total_rain = weather["total_rain"]

    # New weather variable
    humidity = weather.get("humidity", 60.0)

    # -------------------------------------------------
    # PREPARE ML FEATURES
    #
    # Feature order must match training dataset:
    #
    # 1 Temperature
    # 2 Rainfall
    # 3 Humidity
    # 4 Soil pH
    # 5 Soil Type
    # -------------------------------------------------
    features = [[avg_temp, total_rain, humidity, soil_ph, soil_type]]

    # ML prediction
    try:

        if model and hasattr(model, "predict"):

            predicted_yield = float(model.predict(features)[0])

        else:
            # Fallback logic if model is missing
            predicted_yield = (
                (avg_temp * 10)
                + (total_rain * 5)
                + (humidity * 2)
                - (soil_ph * 2)
                + (soil_type * 3)
            )

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": f"Prediction failed: {str(e)}"
        }), 500

    # Generate advisory message
    advisory_data = generate_advisory(
        predicted_yield,
        avg_temp,
        total_rain,
        soil_ph,
        "rainfall"
    )

    response = {
        "status": "success",
        "crop": crop,
        "prediction": round(predicted_yield, 2),
        "advisory": advisory_data["advice"],
        "inputs": {
            "temp": avg_temp,
            "rain": total_rain,
            "humidity": humidity,
            "soil_ph": soil_ph,
            "soil_type": soil_type
        }
    }

    # Save prediction
    save_prediction_result(response)

    return jsonify(response)


# -------------------------------------------------
# SMART CROP RECOMMENDATION API
# Compares multiple crops and selects best crop
# -------------------------------------------------
@app.route("/recommend", methods=["POST"])
def recommend_crop():

    user_data = request.get_json(silent=True) or {}

    if "lat" not in user_data or "lon" not in user_data:
        return jsonify({
            "status": "error",
            "message": "Missing coordinates."
        }), 400

    lat = user_data.get("lat")
    lon = user_data.get("lon")

    soil_type = user_data.get("soil_type", 2)

    try:
        soil_ph = float(user_data.get("soil_ph", 6.5))

        if not (0 <= soil_ph <= 14):
            raise ValueError

    except:
        return jsonify({
            "status": "error",
            "message": "Invalid soil_ph."
        }), 422

    # Fetch weather data
    weather = get_weather_data(lat=lat, lon=lon)

    if weather.get("status") == "error":
        return jsonify({
            "status": "error",
            "message": "Weather failed"
        }), 502

    avg_temp = weather["avg_temp"]
    total_rain = weather["total_rain"]
    humidity = weather.get("humidity", 60.0)

    # Crops supported by system
    possible_crops = [
        "Rice",
        "Wheat",
        "Maize",
        "Sugarcane",
        "Millets"
    ]

    predictions = {}

    # Predict yield for each crop
    for crop in possible_crops:

        features = [[avg_temp, total_rain, humidity, soil_ph, soil_type]]

        if model and hasattr(model, "predict"):

            yield_val = float(model.predict(features)[0])

        else:

            yield_val = (
                (avg_temp * 10)
                + (total_rain * 4)
                + (humidity * 2)
                + (soil_type * 3)
            )

        predictions[crop] = round(yield_val, 2)

    # Select best crop
    best_crop = max(predictions, key=predictions.get)

    advice_map = {
        "Rice": "High rainfall detected; perfect for Rice.",
        "Wheat": "Cooler temperature detected; Wheat is ideal.",
        "Sugarcane": "Stable heat and moisture detected; Sugarcane recommended.",
        "Millets": "Dry conditions detected; Millets are most resilient."
    }

    advisory_message = advice_map.get(
        best_crop,
        "Optimal crop for current scenario."
    )

    response = {
        "status": "success",
        "recommended_crop": best_crop,
        "expected_yield": predictions[best_crop],
        "advisory": advisory_message,
        "all_predictions": predictions,
        "environment": {
            "temp": avg_temp,
            "rain": total_rain,
            "humidity": humidity
        }
    }

    save_prediction_result(response)

    return jsonify(response)


# -------------------------------------------------
# METRICS API
# Returns model evaluation metrics
# -------------------------------------------------
@app.route("/metrics", methods=["GET"])
def metrics_api():

    path = os.path.join(os.path.dirname(__file__), "data", "metrics.json")

    if os.path.exists(path):

        with open(path, "r") as f:

            return jsonify({
                "status": "success",
                "data": json.load(f)
            })

    return jsonify({
        "status": "error",
        "message": "No metrics found"
    }), 404


# -------------------------------------------------
# ADVISORY FUNCTION
# Generates simple farming advice
# -------------------------------------------------
def generate_advisory(predicted_yield, avg_temp, total_rain, soil_ph, top_feature):

    if total_rain < 100:

        advice = "Low rainfall. Increase irrigation."

    elif avg_temp > 30:

        advice = "High heat. Use mulch."

    else:

        advice = "Conditions optimal."

    return {
        "advice": advice,
        "primary_factor": top_feature
    }


# -------------------------------------------------
# WEATHER API
# Allows frontend to fetch weather directly
# -------------------------------------------------
@app.route("/weather", methods=["GET"])
def weather_api():

    lat = request.args.get("lat", default=28.6, type=float)
    lon = request.args.get("lon", default=77.2, type=float)

    weather = get_weather_data(lat=lat, lon=lon)

    if weather["status"] == "success":

        return jsonify({
            "status": "success",
            "data": weather
        })

    else:

        return jsonify({
            "status": "error"
        }), 500


# -------------------------------------------------
# RUN SERVER
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)