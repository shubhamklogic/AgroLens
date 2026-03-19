from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from utils.fetch_weather import get_weather_data
from datetime import datetime
import pickle
import os
import json

# -------------------------------------------------
# FLASK APPLICATION INITIALIZATION
# -------------------------------------------------
# This creates the Flask backend server instance.
# All API routes in this file will attach to this object.
app = Flask(__name__)

# Enable CORS (Cross-Origin Resource Sharing)
# This allows frontend apps (React / Vue / Angular)
# running on different ports to communicate with this API.
CORS(app)


# -------------------------------------------------
# GLOBAL CONFIGURATION
# -------------------------------------------------
# These values are defined globally so they are loaded
# only once when the server starts instead of every request.
# This improves performance and keeps configuration centralized.

# Crop adjustment factors
# These slightly bias the yield score to simulate real-world
# productivity differences between crops.
crop_factor = {
    "Rice": 150,
    "Wheat": 80,
    "Maize": 60,
    "Sugarcane": 150,
    "Millets": 40
}

# NOTE FOR TEAMMATES:
# These were originally used for static crop advisories.
# Now the system uses a dynamic environment-aware advisory
# system instead. This dictionary is kept for reference.
advice_map = {
    "Rice": "High rainfall detected; perfect for Rice.",
    "Wheat": "Cooler temperature detected; Wheat is ideal.",
    "Sugarcane": "Stable heat and moisture detected; Sugarcane recommended.",
    "Millets": "Dry conditions detected; Millets are most resilient."
}


# -------------------------------------------------
# MODEL INITIALIZATION
# -------------------------------------------------
# Loads the trained ML model from model.pkl.
# If the file is missing or corrupted, the system
# automatically falls back to rule-based prediction logic.
def load_trained_model():

    # Locate model file relative to this script
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

    if os.path.exists(model_path):
        try:
            with open(model_path, "rb") as f:
                print("✅ Model V2.0 loaded successfully.")
                return pickle.load(f)

        except Exception as e:
            print(f"⚠️ Error loading model file: {e}")

    else:
        print("⚠️ model.pkl not found. Using fallback estimation logic.")

    # If model fails to load, return None
    return None


# Global model instance (loaded once when server starts)
model = load_trained_model()


# -------------------------------------------------
# DATA STORAGE FUNCTION
# -------------------------------------------------
# Stores prediction results into data/results.json.
# This helps with:
# - analytics
# - dashboard visualization
# - training future ML models
def save_prediction_result(data):

    file_path = os.path.join(os.path.dirname(__file__), "data", "results.json")

    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    results = []

    # Load previous results if file exists
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                results = json.load(f)
        except Exception:
            results = []

    # Add timestamp for tracking when prediction was made
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    results.append(data)

    try:
        with open(file_path, "w") as f:
            json.dump(results, f, indent=4)

        print("📊 Prediction result saved to results.json")

    except Exception as e:
        print(f"⚠️ Error saving result: {e}")


# -------------------------------------------------
# CLIMATE-AWARE ADVISORY SYSTEM
# -------------------------------------------------
# Generates farming advice dynamically based on
# environmental conditions instead of fixed crop rules.
def generate_advisory(predicted_yield, avg_temp, total_rain, soil_ph, top_feature):
    
    # HIGHEST PRIORITY: Extreme temperature
    if avg_temp < 5 or avg_temp > 45:
        advice = "Extreme temperature detected. Crop growth is not viable."

    # Low rainfall scenario
    elif total_rain < 50:
        advice = "Low rainfall detected. Consider drought-resistant crops or irrigation."

    # Excess rainfall scenario
    elif total_rain > 200:
        advice = "High rainfall detected. Water-tolerant crops may perform better."

    # High temperature scenario
    elif avg_temp > 32:
        advice = "High temperature detected. Mulching and irrigation are recommended."

    # Cold temperature scenario
    elif avg_temp < 18:
        advice = "Cool temperature detected. Suitable for temperate crops like wheat."

    # Alkaline soil scenario
    elif soil_ph > 8:
        advice = "Alkaline soil detected. Soil amendments may improve crop yield."

    # Balanced environment
    else:
        advice = "Environmental conditions are balanced for crop growth."

    return {
        "advice": advice,
        "primary_factor": top_feature
    }


# -------------------------------------------------
# DECISION EXPLANATION ENGINE
# -------------------------------------------------
# This function explains WHY a crop recommendation
# was made. This improves transparency and makes
# the system closer to a Prescriptive AI system.
def explain_recommendation(avg_temp, total_rain, humidity, soil_ph, soil_type):

    reasons = []

    if total_rain < 50:
        reasons.append("Low rainfall favors drought-resistant crops.")

    if avg_temp > 30:
        reasons.append("Higher temperatures favor heat-tolerant crops.")

    if humidity < 30:
        reasons.append("Low humidity indicates dry climate conditions.")

    if soil_type == 2:
        reasons.append("Loamy soil supports strong root development.")

    if soil_ph > 7:
        reasons.append("Slightly alkaline soil affects crop suitability.")

    return reasons


# -------------------------------------------------
# PREDICTION API
# -------------------------------------------------
# Predict yield for a specific crop.
@app.route("/predict", methods=["POST"])
def predict():

    try:

        user_data = request.get_json(silent=True) or {}

        # Ensure coordinates exist
        if "lat" not in user_data or "lon" not in user_data:
            return jsonify({
                "status": "error",
                "message": "Missing lat/lon."
            }), 400

        crop = user_data.get("crop", "wheat").capitalize()
        
        try:
          lat = float(user_data.get("lat"))
          lon = float(user_data.get("lon"))
        except (TypeError, ValueError):
          return jsonify({
        "status": "error",
        "message": "Latitude and Longitude must be valid numbers"
         }), 400
        
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
         return jsonify({
        "status": "error",
        "message": "Invalid latitude or longitude"
        }), 422

        # Soil type validation
        try:
            soil_type = int(user_data.get("soil_type", 2))

            if soil_type not in [1, 2, 3]:
                raise ValueError

        except (ValueError, TypeError):

            return jsonify({
                "status": "error",
                "message": "Invalid soil_type. Use 1 (Sandy), 2 (Loamy), or 3 (Clayey)."
            }), 422

        # Soil pH validation
        try:
            soil_ph = float(user_data.get("soil_ph", 6.5))

            if not (0 <= soil_ph <= 14):
                raise ValueError

        except:

            return jsonify({
                "status": "error",
                "message": "Invalid soil_ph (0–14 allowed)."
            }), 422

        # Fetch weather data from weather utility
        weather = get_weather_data(lat=lat, lon=lon)

        if weather.get("status") == "error":

            return jsonify({
                "status": "error",
                "message": "Weather service failed"
            }), 502

        avg_temp = weather["avg_temp"]
        total_rain = weather["total_rain"]
        humidity = weather.get("humidity", 60.0)

        # Environmental sanity validation
        if not (isinstance(total_rain, (int, float)) and 0 <= total_rain <= 2000):
         return jsonify({
        "status": "error",
        "message": "Invalid rainfall value"
        }), 422

        if not isinstance(avg_temp, (int, float)) or not (-60 <= avg_temp <= 60):
         return jsonify({
        "status": "error",
        "message": "Temperature out of realistic Earth bounds"
        }), 422

        if not isinstance(humidity, (int, float)) or not (0 <= humidity <= 100):
         return jsonify({
        "status": "error",
        "message": "Humidity must be between 0 and 100%"
        }), 422

        # Feature vector for ML model
        features = [[avg_temp, total_rain, humidity, soil_ph, soil_type]]

        # If ML model exists use it
        if model and hasattr(model, "predict"):

            predicted_yield = float(model.predict(features)[0])

        else:
            # Fallback rule-based yield estimation
            base = (avg_temp * 10) + (total_rain * 5)
            humidity_impact = (humidity * 1.5)
            soil_impact = 500 if soil_type == 2 else 200
            ph_penalty = abs(7.0 - soil_ph) * 50

            predicted_yield = max(0, base + humidity_impact + soil_impact - ph_penalty)

        # 🌱 Biological Kill Switch (GLOBAL AGRICULTURE LOGIC)
        if avg_temp < 5 or avg_temp > 45:
           predicted_yield = 0

        advisory_data = generate_advisory(
            predicted_yield,
            avg_temp,
            total_rain,
            soil_ph,
            "weather"
        )

        response = {

            "status": "success",
            "crop": crop,
            "prediction": round(predicted_yield, 2),
            "advisory": advisory_data["advice"],

            "inputs": {
                "temp": round(avg_temp,2),
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
# Determines the best crop among multiple options.
@app.route("/recommend", methods=["POST"])
def recommend_crop():

    try:

        user_data = request.get_json(silent=True) or {}

        if "lat" not in user_data or "lon" not in user_data:
            return jsonify({
                "status": "error",
                "message": "Missing coordinates."
            }), 400

        try:
          lat = float(user_data.get("lat"))
          lon = float(user_data.get("lon"))
        except (TypeError, ValueError):
          return jsonify({
        "status": "error",
        "message": "Latitude and Longitude must be valid numbers"
         }), 400

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
         return jsonify({
        "status": "error",
        "message": "Invalid latitude or longitude"
        }), 422

        try:
            soil_type = int(user_data.get("soil_type", 2))
            if soil_type not in [1, 2, 3]:
                raise ValueError

        except (ValueError, TypeError):
            return jsonify({
                "status": "error",
                "message": "Invalid soil_type"
            }), 422

        try:
            soil_ph = float(user_data.get("soil_ph", 6.5))
            if not (0 <= soil_ph <= 14):
                raise ValueError

        except:
            return jsonify({
                "status": "error",
                "message": "Invalid soil_ph"
            }), 422

        weather = get_weather_data(lat=lat, lon=lon)

        # Safer weather status check
        if weather.get("status") == "error":
            return jsonify({
                "status": "error",
                "message": "Weather failed"
            }), 502

        avg_temp = weather["avg_temp"]
        total_rain = weather["total_rain"]
        humidity = weather.get("humidity", 60.0)

        # Environmental validation
        if not (isinstance(total_rain, (int, float)) and 0 <= total_rain <= 2000):
         return jsonify({
        "status": "error",
        "message": "Invalid rainfall value"
        }), 422

        if not isinstance(avg_temp, (int, float)) or not (-60 <= avg_temp <= 60):
         return jsonify({
        "status": "error",
        "message": "Temperature out of realistic Earth bounds"
        }), 422

        if not isinstance(humidity, (int, float)) or not (0 <= humidity <= 100):
         return jsonify({
        "status": "error",
        "message": "Humidity must be between 0 and 100%"
        }), 422

        possible_crops = [
            "Rice",
            "Wheat",
            "Maize",
            "Sugarcane",
            "Millets"
        ]

        predictions = {}

        # Evaluate yield for each crop
        for crop in possible_crops:

            features = [[avg_temp, total_rain, humidity, soil_ph, soil_type]]

            if model and hasattr(model, "predict"):

                yield_val = float(model.predict(features)[0])

            else:

                base = (avg_temp * 5) + (humidity * 2)

                if crop == "Rice":
                    yield_val = base + (total_rain * 20) + (600 if soil_type == 3 else 0)

                elif crop == "Sugarcane":
                    yield_val = base + (avg_temp * 10) + (humidity * 2)

                elif crop == "Wheat":
                    yield_val = base + (250 if avg_temp < 25 else 50) + (200 if soil_type == 2 else 0) + (150 if total_rain > 40 else 0)

                elif crop == "Millets":
                    yield_val = base + (500 if total_rain < 50 else 0) + (300 if humidity < 40 else 0) + (300 if soil_type == 1 else 0)

                else:
                    yield_val = base + (total_rain * 2)
                    # climate penalty
            if total_rain == 0:
                 yield_val -= 100
            total_yield = yield_val + crop_factor.get(crop, 0)
            final_score = 0 if (avg_temp < 5 or avg_temp > 45) else max(0, total_yield)
            predictions[crop] = round(final_score, 2)
            if all(value == 0 for value in predictions.values()):
              best_crop = "None"
              expected_yield = 0
            else:
              best_crop = max(predictions, key=predictions.get)
              expected_yield = predictions[best_crop]

        response = {

            "status": "success",

            "recommended_crop": best_crop,

            "expected_yield": expected_yield,

            # Dynamic advisory instead of static crop message
            "advisory": generate_advisory(
                expected_yield,
                avg_temp,
                total_rain,
                soil_ph,
                "environment"
            )["advice"],

            # Explain why the crop was recommended
            "decision_factors": explain_recommendation(
                avg_temp,
                total_rain,
                humidity,
                soil_ph,
                soil_type
            ),

            "all_predictions": predictions,

            "environment": {
                "temp": round(avg_temp,2),
                "rain": round(total_rain,2),
                "humidity": round(humidity,2)
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
# METRICS API
# -------------------------------------------------
# Returns stored model performance metrics if available.
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
# WEATHER API
# -------------------------------------------------
# Simple endpoint for retrieving weather data.
@app.route("/weather", methods=["GET"])
def weather_api():

    lat = request.args.get("lat", default=28.6, type=float)
    lon = request.args.get("lon", default=77.2, type=float)

    weather = get_weather_data(lat=lat, lon=lon)

    if weather.get("status") == "success":

        return jsonify({
            "status": "success",
            "data": weather
        })

    else:

        return jsonify({
            "status": "error"
        }), 500

# -------------------------------------------------
# HOME PAGE ROUTE
# -------------------------------------------------
# This route loads the frontend HTML page when
# someone opens the base URL of the server.

@app.route("/")
def home():
    return render_template("index.html")

# -------------------------------------------------
# HEALTH CHECK API
# -------------------------------------------------
# Used by monitoring tools or deployment services
# to verify the backend is running.
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
# Starts the Flask development server.
# debug=True enables automatic reload and error logs.
if __name__ == "__main__":

    app.run(debug=True)