from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    # 1. Get JSON data sent by user
    user_data = request.get_json()

    # 2. Extract crop name
    selected_crop = user_data.get("crop", "Unknown")

    # 3. Create response
    result = {
        "received_crop": selected_crop,
        "yield_prediction": 2600,  # Dummy value
        "status": "success"
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
