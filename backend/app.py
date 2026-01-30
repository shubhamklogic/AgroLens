from flask import Flask, jsonify   # Import Flask and jsonify

# Initialize the Flask application
app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return "AgroLens Backend is working! 🌾"

# Prediction API route
@app.route("/predict")
def predict():
    # Dummy prediction data
    result = {
        "crop": "Wheat",
        "yield_prediction": 2500,
        "unit": "kg/ha",
        "status": "success"
    }
    return jsonify(result)

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)