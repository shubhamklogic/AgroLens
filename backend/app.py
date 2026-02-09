from flask import Flask, jsonify, request
from utils import get_weather_data
from datetime import datetime

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    # 1. Read input safely
    user_data = request.get_json(silent=True) or {}

    crop = user_data.get("crop", "unknown").capitalize()
    lat = user_data.get("lat", 26.91)   # Default: Jaipur
    lon = user_data.get("lon", 75.78)

    # 2. Validate coordinates
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return jsonify({
            "status": "error",
            "message": "Invalid coordinates provided."
        }), 400

    # 3. Fetch live weather data
    weather = get_weather_data(lat=lat, lon=lon)
    if weather["status"] == "error":
        return jsonify({
            "status": "error",
            "message": "Weather service unavailable",
            "details": weather["message"]
        }), 500

    # 4. Extract values
    avg_temp = weather["avg_temp"]
    total_rain = weather["total_rain"]

    # 5. Weather-aware recommendation logic
    if total_rain > 10:
        advice = f"High rainfall ({total_rain} mm) detected. Avoid extra irrigation."
    elif avg_temp > 30:
        advice = f"High temperature ({avg_temp} °C). Ensure soil moisture is maintained."
    else:
        advice = f"Weather conditions are stable for {crop}."

    # 6. Yield prediction (dummy logic)
    predicted_yield = 3200 if avg_temp < 28 else 2700

    # 7. Final response
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
            "avg_temp": avg_temp,
            "total_rain": total_rain,
            "predicted_yield": predicted_yield
        },
        "recommendation": advice
    })

# REQUIRED to start the Flask server
if __name__ == "__main__":
    app.run(debug=True)
