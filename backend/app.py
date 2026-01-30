from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    crop = data.get("crop", "unknown").lower() # Get crop and make it lowercase
    
    # Using if-else to simulate ML logic
    if crop == "wheat":
        yield_val = 3000
        advice = "Ideal time for nitrogen-based fertilizer."
    elif crop == "rice":
        yield_val = 2800
        advice = "Ensure consistent water levels in the field."
    elif crop == "maize":
        yield_val = 3200
        advice = "Watch for stem borer pests during this stage."
    else:
        yield_val = 0
        advice = "Crop data not found. Please try Wheat, Rice, or Maize."

    return jsonify({
        "crop": crop,
        "yield_prediction": yield_val,
        "advice": advice,
        "status": "success" if yield_val > 0 else "error"
    })

if __name__ == "__main__":
    app.run(debug=True)