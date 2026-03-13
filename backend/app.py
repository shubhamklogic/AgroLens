from flask import Flask, jsonify, request
from utils import get_weather_data
from datetime import datetime
import pickle
import os
import json

app = Flask(__name__)

# -------------------------------------------------
# MODEL LOADING SECTION
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
# -------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    user_data = request.get_json(silent=True) or {}

    crop = user_data.get("crop", "wheat").capitalize()
    lat = user_data.get("lat", 28.6)
    lon = user_data.get("lon", 77.2)
    soil_ph = user_data.get("soil_ph", 6.5)

    weather = get_weather_data(lat=lat, lon=lon)
    if weather["status"] == "error":
        return jsonify({"status": "error", "message": "Weather service unavailable"}), 500

    avg_temp = weather["avg_temp"]
    total_rain = weather["total_rain"]

    features = [[avg_temp, total_rain, soil_ph]]

    try:
        if model and hasattr(model, "predict"):
            prediction = model.predict(features)
            predicted_yield = float(prediction[0])
        else:
            predicted_yield = (avg_temp * 10) + (total_rain * 5) - (soil_ph * 2)
            print("DEBUG: Using Dummy/Mock prediction logic")
    except Exception as e:
        return jsonify({"status": "error", "message": f"Prediction failed: {e}"}), 500

    if total_rain > 10:
        advice = f"High rainfall ({total_rain} mm) detected. Avoid extra irrigation."
    else:
        advice = f"Weather stable for {crop}. Maintain standard soil moisture."

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
# EVALUATION API SECTION (Moved Above app.run)
# -------------------------------------------------
@app.route("/metrics", methods=["GET"])
def metrics_api():
    """
    API endpoint to return model performance metrics (MAE, RMSE, R2). [cite: 44, 45]
    """
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
# RUN SERVER (Keep this at the very bottom!)
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)