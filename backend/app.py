from flask import Flask, jsonify, request
from utils import get_weather_data

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    user_data = request.get_json(silent=True) or {}
    crop = user_data.get("crop", "unknown")

    # Step 1: Get dynamic coordinates
    lat = user_data.get("lat", 26.91)
    lon = user_data.get("lon", 75.78)

    # Step 2: Validation
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return jsonify({
            "status": "error",
            "message": "Invalid coordinates provided."
        }), 400

    # Step 3: Fetch weather
    weather = get_weather_data(lat=lat, lon=lon)

    if weather["status"] == "error":
        return jsonify({
            "status": "error",
            "message": "NASA API Error",
            "details": weather["message"]
        }), 500

    # Dummy prediction logic
    prediction = 3500 if weather["avg_temp"] > 25 else 2500

    return jsonify({
        "status": "success",
        "crop": crop,
        "location": {"lat": lat, "lon": lon},
        "weather_summary": weather,
        "predicted_yield": prediction
    })

if __name__ == "__main__":
    app.run(debug=True)