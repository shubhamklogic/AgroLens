from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.fetch_weather import get_weather_data
from datetime import datetime
import pickle
import os
import json

app = Flask(__name__)
CORS(app) # This allows the frontend to talk to your backend

# -------------------------------------------------
# MODEL INITIALIZATION
# -------------------------------------------------
# This function loads the trained ML model (model.pkl)
# when the server starts. Loading the model once improves
# performance because we avoid loading it for every request.
# -------------------------------------------------
def load_trained_model():

    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

    if os.path.exists(model_path):
        try:
            with open(model_path, "rb") as f:
                print("✅ Model V2.0 loaded successfully.")
                return pickle.load(f)

        except Exception as e:
            print(f"⚠️ Error loading model file: {e}")

    else:
        print("⚠️ model.pkl not found. Using improved V2 fallback logic.")

    return None


# Global variable
# Model is loaded only once when the server starts
model = load_trained_model()


# -------------------------------------------------
# DATA STORAGE FUNCTION
# -------------------------------------------------
# Saves prediction results into data/results.json
# This helps track experiments and analyze system usage.
# -------------------------------------------------
def save_prediction_result(data):

    file_path = os.path.join(os.path.dirname(__file__), "data", "results.json")

    # Create data directory if it does not exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    results = []

    # Load previous results if file exists
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                results = json.load(f)
        except Exception:
            results = []

    # Add timestamp for experiment tracking
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    results.append(data)

    try:
        with open(file_path, "w") as f:
            json.dump(results, f, indent=4)

        print("📊 Prediction result saved to results.json")

    except Exception as e:
        print(f"⚠️ Error saving result: {e}")


# -------------------------------------------------
# PREDICTION API
# -------------------------------------------------
# Endpoint: POST /predict
#
# Purpose:
# Predict crop yield for a specific crop using:
# - Weather data
# - Soil properties
# - ML model
#
# Input:
# lat, lon, soil_type, soil_ph
#
# Output:
# predicted yield + advisory
# -------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():

    user_data = request.get_json(silent=True) or {}

    # ------------------------------
    # 1. Validate coordinates
    # ------------------------------
    if "lat" not in user_data or "lon" not in user_data:
        return jsonify({
            "status": "error",
            "message": "Missing lat/lon."
        }), 400

    crop = user_data.get("crop", "wheat").capitalize()

    lat = user_data.get("lat")
    lon = user_data.get("lon")

    # ------------------------------
    # 2. Soil Type Validation
    #
    # Encoding:
    # 1 = Sandy
    # 2 = Loamy
    # 3 = Clayey
    # ------------------------------
    try:
        soil_type = int(user_data.get("soil_type", 2))

        if soil_type not in [1, 2, 3]:
            raise ValueError

    except (ValueError, TypeError):

        return jsonify({
            "status": "error",
            "message": "Invalid soil_type. Use 1 (Sandy), 2 (Loamy), or 3 (Clayey)."
        }), 422


    # ------------------------------
    # 3. Soil pH Validation
    # ------------------------------
    try:
        soil_ph = float(user_data.get("soil_ph", 6.5))

        if not (0 <= soil_ph <= 14):
            raise ValueError

    except:

        return jsonify({
            "status": "error",
            "message": "Invalid soil_ph (0–14 allowed)."
        }), 422


    # ------------------------------
    # 4. Fetch weather data
    # ------------------------------
    weather = get_weather_data(lat=lat, lon=lon)

    if weather.get("status") == "error":

        return jsonify({
            "status": "error",
            "message": "Weather service failed"
        }), 502


    # Extract weather features
    avg_temp = weather["avg_temp"]
    total_rain = weather["total_rain"]
    humidity = weather.get("humidity", 60.0)


    # -------------------------------------------------
    # 5. FEATURE VECTOR
    #
    # IMPORTANT:
    # Feature order must match the ML training dataset
    #
    # Order:
    # [Temperature, Rainfall, Humidity, Soil pH, Soil Type]
    # -------------------------------------------------
    features = [[avg_temp, total_rain, humidity, soil_ph, soil_type]]


    # -------------------------------------------------
    # 6. Prediction Logic
    # -------------------------------------------------
    try:

        # If trained model exists
        if model and hasattr(model, "predict"):

            predicted_yield = float(model.predict(features)[0])

        else:

            # -----------------------------------------
            # FALLBACK LOGIC
            # Used when model.pkl is not available
            # -----------------------------------------
            base = (avg_temp * 10) + (total_rain * 5)
            humidity_impact = (humidity * 1.5)
            soil_impact = 500 if soil_type == 2 else 200
            ph_penalty = abs(7.0 - soil_ph) * 50

            predicted_yield = base + humidity_impact + soil_impact - ph_penalty

            print("DEBUG: Using Improved V2 Mock logic")


    except Exception as e:

        return jsonify({
            "status": "error",
            "message": f"Prediction failed: {str(e)}"
        }), 500


    # Generate farming advisory
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
            "ph": soil_ph,
            "soil": soil_type
        }
    }


    # Save prediction result for analytics
    save_prediction_result(response)

    return jsonify(response)


# -------------------------------------------------
# SMART CROP RECOMMENDATION API
# -------------------------------------------------
# Endpoint: POST /recommend
#
# Purpose:
# Predict yield for multiple crops and recommend
# the crop with the highest expected yield.
# -------------------------------------------------
@app.route("/recommend", methods=["POST"])
def recommend_crop():

    user_data = request.get_json(silent=True) or {}

    # Validate coordinates
    if "lat" not in user_data or "lon" not in user_data:
        return jsonify({
            "status": "error",
            "message": "Missing coordinates."
        }), 400


    lat = user_data.get("lat")
    lon = user_data.get("lon")


    # Soil Type Validation
    try:

        soil_type = int(user_data.get("soil_type", 2))

        if soil_type not in [1,2,3]:
            raise ValueError

    except (ValueError,TypeError):

        return jsonify({
            "status":"error",
            "message":"Invalid soil_type"
        }),422


    # Soil pH Validation
    try:

        soil_ph = float(user_data.get("soil_ph",6.5))

        if not (0 <= soil_ph <= 14):
            raise ValueError

    except:

        return jsonify({
            "status":"error",
            "message":"Invalid soil_ph"
        }),422


    weather = get_weather_data(lat=lat, lon=lon)

    if weather.get("status") == "error":

        return jsonify({
            "status":"error",
            "message":"Weather failed"
        }),502


    avg_temp = weather["avg_temp"]
    total_rain = weather["total_rain"]
    humidity = weather.get("humidity",60.0)


    # Crops supported by the system
    possible_crops = [
        "Rice",
        "Wheat",
        "Maize",
        "Sugarcane",
        "Millets"
    ]


    # Crop-specific adjustment factors
    crop_factor = {

        "Rice":120,
        "Wheat":80,
        "Maize":60,
        "Sugarcane":150,
        "Millets":40
    }


    predictions = {}


    for crop in possible_crops:

        features = [[avg_temp,total_rain,humidity,soil_ph,soil_type]]

        if model and hasattr(model,"predict"):

            yield_val = float(model.predict(features)[0])

        else:

            # Same fallback logic used in /predict
            base = (avg_temp * 10) + (total_rain * 5)
            humidity_impact = (humidity * 1.5)
            soil_impact = 500 if soil_type == 2 else 200
            ph_penalty = abs(7.0 - soil_ph) * 50

            yield_val = base + humidity_impact + soil_impact - ph_penalty


        adjusted_yield = yield_val + crop_factor.get(crop,0)

        predictions[crop] = round(adjusted_yield,2)


    best_crop = max(predictions,key=predictions.get)


    advice_map = {

        "Rice":"High rainfall detected; perfect for Rice.",
        "Wheat":"Cooler temperature detected; Wheat is ideal.",
        "Sugarcane":"Stable heat and moisture detected; Sugarcane recommended.",
        "Millets":"Dry conditions detected; Millets are most resilient."
    }


    response = {

        "status":"success",

        "recommended_crop":best_crop,

        "expected_yield":predictions[best_crop],

        "advisory":advice_map.get(best_crop,"Conditions support this crop."),

        "all_predictions":predictions,

        "environment":{

            "temp":avg_temp,
            "rain":total_rain,
            "humidity":humidity
        }
    }


    save_prediction_result(response)

    return jsonify(response)


# -------------------------------------------------
# METRICS API
# -------------------------------------------------
@app.route("/metrics", methods=["GET"])
def metrics_api():

    path = os.path.join(os.path.dirname(__file__), "data", "metrics.json")

    if os.path.exists(path):

        with open(path,"r") as f:

            return jsonify({
                "status":"success",
                "data":json.load(f)
            })

    return jsonify({
        "status":"error",
        "message":"No metrics found"
    }),404


# -------------------------------------------------
# ADVISORY FUNCTION
# -------------------------------------------------
# Generates simple farming advice based on weather
# -------------------------------------------------
def generate_advisory(predicted_yield,avg_temp,total_rain,soil_ph,top_feature):

    if total_rain < 100:

        advice = "Low rainfall. Increase irrigation."

    elif avg_temp > 30:

        advice = "High heat. Use mulch."

    else:

        advice = "Conditions optimal."

    return {

        "advice":advice,
        "primary_factor":top_feature
    }


# -------------------------------------------------
# WEATHER API
# -------------------------------------------------
# Allows frontend to directly fetch weather data
#
# Example:
# /weather?lat=28.6&lon=77.2
# -------------------------------------------------
@app.route("/weather", methods=["GET"])
def weather_api():

    lat = request.args.get("lat",default=28.6,type=float)

    lon = request.args.get("lon",default=77.2,type=float)

    weather = get_weather_data(lat=lat,lon=lon)

    if weather["status"] == "success":

        return jsonify({

            "status":"success",
            "data":weather
        })

    else:

        return jsonify({
            "status":"error"
        }),500


# -------------------------------------------------
# RUN SERVER
# -------------------------------------------------
if __name__ == "__main__":

    app.run(debug=True)