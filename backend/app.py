from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.fetch_weather import get_weather_data
from datetime import datetime
import pickle
import os
import json

app = Flask(__name__)
CORS(app)  # Allows frontend applications (different ports/domains) to access this backend API


# -------------------------------------------------
# GLOBAL CONFIGURATION
# -------------------------------------------------
# These dictionaries are defined globally so they
# load only once when the server starts.
# This improves readability and performance.
# -------------------------------------------------

# Crop-specific yield adjustment factors
# These values slightly bias the prediction so that
# crops with naturally higher productivity still compete fairly
crop_factor = {
    "Rice": 150,      # Increased to match Sugarcane advantage in rainfall conditions
    "Wheat": 80,
    "Maize": 60,
    "Sugarcane": 150,
    "Millets": 40
}

# Advisory messages for recommended crops
advice_map = {
    "Rice": "High rainfall detected; perfect for Rice.",
    "Wheat": "Cooler temperature detected; Wheat is ideal.",
    "Sugarcane": "Stable heat and moisture detected; Sugarcane recommended.",
    "Millets": "Dry conditions detected; Millets are most resilient."
}


# -------------------------------------------------
# MODEL INITIALIZATION
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


# Global model instance
model = load_trained_model()


# -------------------------------------------------
# DATA STORAGE FUNCTION
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
@app.route("/predict", methods=["POST"])
def predict():

    try:

        user_data = request.get_json(silent=True) or {}

        if "lat" not in user_data or "lon" not in user_data:
            return jsonify({
                "status": "error",
                "message": "Missing lat/lon."
            }), 400

        crop = user_data.get("crop", "wheat").capitalize()

        lat = user_data.get("lat")
        lon = user_data.get("lon")

        # Soil Type Validation
        try:
            soil_type = int(user_data.get("soil_type", 2))

            if soil_type not in [1, 2, 3]:
                raise ValueError

        except (ValueError, TypeError):

            return jsonify({
                "status": "error",
                "message": "Invalid soil_type. Use 1 (Sandy), 2 (Loamy), or 3 (Clayey)."
            }), 422


        # Soil pH Validation
        try:
            soil_ph = float(user_data.get("soil_ph", 6.5))

            if not (0 <= soil_ph <= 14):
                raise ValueError

        except:

            return jsonify({
                "status": "error",
                "message": "Invalid soil_ph (0–14 allowed)."
            }), 422


        weather = get_weather_data(lat=lat, lon=lon)

        if weather.get("status") == "error":

            return jsonify({
                "status": "error",
                "message": "Weather service failed"
            }), 502


        avg_temp = weather["avg_temp"]
        total_rain = weather["total_rain"]
        humidity = weather.get("humidity", 60.0)

        features = [[avg_temp, total_rain, humidity, soil_ph, soil_type]]

        if model and hasattr(model, "predict"):

            predicted_yield = float(model.predict(features)[0])

        else:

            base = (avg_temp * 10) + (total_rain * 5)
            humidity_impact = (humidity * 1.5)
            soil_impact = 500 if soil_type == 2 else 200
            ph_penalty = abs(7.0 - soil_ph) * 50

            predicted_yield = base + humidity_impact + soil_impact - ph_penalty


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

        save_prediction_result(response)

        return jsonify(response)

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": f"An internal server error occurred: {str(e)}"
        }), 500


# -------------------------------------------------
# SMART CROP RECOMMENDATION API
# -------------------------------------------------
@app.route("/recommend", methods=["POST"])
def recommend_crop():

    try:

        user_data = request.get_json(silent=True) or {}

        if "lat" not in user_data or "lon" not in user_data:
            return jsonify({
                "status": "error",
                "message": "Missing coordinates."
            }), 400


        lat = user_data.get("lat")
        lon = user_data.get("lon")


        try:

            soil_type = int(user_data.get("soil_type", 2))

            if soil_type not in [1,2,3]:
                raise ValueError

        except (ValueError,TypeError):

            return jsonify({
                "status":"error",
                "message":"Invalid soil_type"
            }),422


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


        possible_crops = [
            "Rice",
            "Wheat",
            "Maize",
            "Sugarcane",
            "Millets"
        ]


        predictions = {}

        # -------------------------------------------------
        # CROP RECOMMENDATION PREDICTION LOOP
        # -------------------------------------------------
        # Each crop is evaluated separately.
        # ML model -> used if available
        # Fallback logic -> used if model missing
        # -------------------------------------------------
        for crop in possible_crops:

            features = [[avg_temp, total_rain, humidity, soil_ph, soil_type]]

            if model and hasattr(model,"predict"):

                yield_val = float(model.predict(features)[0])

            else:

                # Base environmental score used for all crops
                base = (avg_temp * 5) + (humidity * 2)

                # -------------------------------------------------
                # Updated Rice Logic
                # -------------------------------------------------
                # Rice heavily depends on rainfall.
                # Increasing rainfall multiplier ensures
                # Rice wins in tropical/high rainfall climates.
                if crop == "Rice":
                    yield_val = base + (total_rain * 20) + (600 if soil_type == 3 else 0)

                # -------------------------------------------------
                # Updated Sugarcane Logic
                # -------------------------------------------------
                # Sugarcane prefers heat + humidity but we reduced
                # the multiplier so it doesn't dominate every case.
                elif crop == "Sugarcane":
                    yield_val = base + (avg_temp * 10) + (humidity * 2)

                elif crop == "Wheat":
                    yield_val = base + (200 if avg_temp < 25 else 50) + (500 if soil_type == 2 else 0)

                elif crop == "Millets":
                    yield_val = base + (500 if total_rain < 50 else 0) + (400 if soil_type == 1 else 0)

                else:
                    yield_val = base + (total_rain * 2)


            # Final adjustment factor
            adjusted_yield = yield_val + crop_factor.get(crop,0)

            predictions[crop] = round(adjusted_yield,2)


        best_crop = max(predictions,key=predictions.get)


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

    except Exception as e:

        return jsonify({
            "status":"error",
            "message":f"An internal server error occurred: {str(e)}"
        }),500


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