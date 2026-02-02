from flask import Flask, jsonify, request
from utils import get_weather_data

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    user_data = request.get_json(silent=True) or {}
    crop = user_data.get("crop", "unknown")

    # Using Jaipur coordinates (default)
    weather = get_weather_data(lat=26.91, lon=75.78)

    if weather["status"] == "error":
        return jsonify({
            "status": "error",
            "message": "NASA API Error",
            "details": weather["message"]
        }), 500

    # Dummy prediction logic
    prediction = 3000 if weather["avg_temp"] > 20 else 2000

    return jsonify({
        "status": "success",
        "crop": crop,
        "weather_summary": weather,
        "predicted_yield": prediction
    })

if __name__ == "__main__":
    app.run(debug=True)