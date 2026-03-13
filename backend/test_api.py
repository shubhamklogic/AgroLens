import requests

# 1. Update the URL to point to /advisory instead of /predict
url = "http://127.0.0.1:5000/advisory"

# 2. Update the data to match the expected Advisory inputs
data = {
    "temp": 35.0,
    "rain": 50.0,
    "soil_ph": 6.2,
    "predicted_yield": 2800.0
}

# 3. Keep your existing POST request logic
response = requests.post(url, json=data)

# 4. Print the response
print(response.json())