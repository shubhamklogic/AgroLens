from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.fetch_weather import get_weather_data
from datetime import datetime
import pickle
import os
import json

# -------------------------------------------------
# FLASK APPLICATION INITIALIZATION
# -------------------------------------------------
# Flask app object created
app = Flask(__name__)

# Enable CORS so frontend apps (React, Vue, etc.)
# running on different ports can access this API
CORS(app)


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
    "Rice": 150,
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
# Loads the trained ML model from model.pkl
# If the file is missing or corrupted, fallback logic is used
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


# Global model instance (loaded once at server start)
model = load_trained_model()


# -------------------------------------------------
# DATA STORAGE FUNCTION
# -------------------------------------------------
# Saves prediction responses to data/results.json
# This allows later analysis or visualization
# -------------------------------------------------
def save_prediction_result(data):

    file_path = os.path.join(os.path.dirname(__file__), "data", "results.json")

    # Ensure the data folder exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    results = []

    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                results = json.load(f)
        except Exception:
            results = []

    # Add timestamp to each saved prediction
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
# Predicts crop yield based on environmental data
# -------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():

    try:

        user_data = request.get_json(silent=True) or {}

        # Check if coordinates exist
        if "lat" not in user_data or "lon" not in user_data:
            return jsonify({
                "status": "error",
                "message": "Missing lat/lon."
            }), 400

        crop = user_data.get("crop", "wheat").capitalize()

        lat = user_data.get("lat")
        lon = user_data.get("lon")

        # -------------------------------------------------
        # SOIL TYPE VALIDATION
        # -------------------------------------------------
        try:
            soil_type = int(user_data.get("soil_type", 2))

            if soil_type not in [1, 2, 3]:
                raise ValueError

        except (ValueError, TypeError):

            return jsonify({
                "status": "error",
                "message": "Invalid soil_type. Use 1 (Sandy), 2 (Loamy), or 3 (Clayey)."
            }), 422


        # -------------------------------------------------
        # SOIL PH VALIDATION
        # -------------------------------------------------
        try:
            soil_ph = float(user_data.get("soil_ph", 6.5))

            if not (0 <= soil_ph <= 14):
                raise ValueError

        except:

            return jsonify({
                "status": "error",
                "message": "Invalid soil_ph (0–14 allowed)."
            }), 422


        # -------------------------------------------------
        # WEATHER DATA FETCH
        # -------------------------------------------------
        weather = get_weather_data(lat=lat, lon=lon)

        if weather.get("status") == "error":

            return jsonify({
                "status": "error",
                "message": "Weather service failed"
            }), 502


        avg_temp = weather["avg_temp"]
        total_rain = weather["total_rain"]
        humidity = weather.get("humidity", 60.0)


        # -------------------------------------------------
        # ENVIRONMENTAL INPUT VALIDATION
        # -------------------------------------------------
        # Ensures realistic agricultural values
        # Prevents impossible predictions
        # -------------------------------------------------
        try:

            # Rainfall cannot be negative
            if total_rain < 0:
                return jsonify({
                    "status": "error",
                    "message": "Invalid rainfall: cannot be negative"
                }), 422

            # Temperature must stay within realistic agricultural bounds
            if not (-10 <= avg_temp <= 60):
                return jsonify({
                    "status": "error",
                    "message": "Temperature out of realistic agricultural bounds"
                }), 422

            # Humidity must be between 0 and 100%
            if not (0 <= humidity <= 100):
                return jsonify({
                    "status": "error",
                    "message": "Humidity must be between 0 and 100%"
                }), 422

        except Exception as e:

            return jsonify({
                "status": "error",
                "message": f"Validation failed: {str(e)}"
            }), 400


        features = [[avg_temp, total_rain, humidity, soil_ph, soil_type]]

        # -------------------------------------------------
        # ML MODEL PREDICTION
        # -------------------------------------------------
        if model and hasattr(model, "predict"):

            predicted_yield = float(model.predict(features)[0])

        else:

            # Fallback mathematical estimation logic
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


        # -------------------------------------------------
        # ENVIRONMENTAL INPUT VALIDATION
        # -------------------------------------------------
        try:

            if total_rain < 0:
                return jsonify({
                    "status":"error",
                    "message":"Invalid rainfall: cannot be negative"
                }),422

            if not (-10 <= avg_temp <= 60):
                return jsonify({
                    "status":"error",
                    "message":"Temperature out of realistic agricultural bounds"
                }),422

            if not (0 <= humidity <= 100):
                return jsonify({
                    "status":"error",
                    "message":"Humidity must be between 0 and 100%"
                }),422

        except Exception as e:

            return jsonify({
                "status":"error",
                "message":f"Validation failed: {str(e)}"
            }),400


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
        for crop in possible_crops:

            features = [[avg_temp, total_rain, humidity, soil_ph, soil_type]]

            if model and hasattr(model,"predict"):

                yield_val = float(model.predict(features)[0])

            else:

                base = (avg_temp * 5) + (humidity * 2)

                if crop == "Rice":
                    yield_val = base + (total_rain * 20) + (600 if soil_type == 3 else 0)

                elif crop == "Sugarcane":
                    yield_val = base + (avg_temp * 10) + (humidity * 2)

                elif crop == "Wheat":
                    yield_val = base + (200 if avg_temp < 25 else 50) + (500 if soil_type == 2 else 0)

                elif crop == "Millets":
                    yield_val = base + (500 if total_rain < 50 else 0) + (400 if soil_type == 1 else 0)

                else:
                    yield_val = base + (total_rain * 2)


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
# HEALTH CHECK API
# -------------------------------------------------
# This endpoint helps verify that the backend
# server is running properly.
# It is commonly used in production deployments,
# monitoring tools, and load balancers.
# -------------------------------------------------
@app.route("/health", methods=["GET"])
def health_check():

    return jsonify({
        "status": "success",
        "message": "AgroLens backend is running",
        "model_loaded": True if model else False
    })

# -------------------------------------------------
# RUN SERVER
# -------------------------------------------------
if __name__ == "__main__":

    # debug=True enables auto-reload and error logs
    app.run(debug=True)