import requests

# API endpoint
url = "http://127.0.0.1:5000/predict"

# Test input data
data = {
    "crop": "wheat",
    "lat": 28.6,
    "lon": 77.2,
    "soil_ph": 6.5
}

# Sending POST request
response = requests.post(url, json=data)

# Printing API response
print(response.json())