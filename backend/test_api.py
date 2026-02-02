import requests

url = "http://127.0.0.1:5000/predict"

# Testing for a location in Bihar (Gopalganj area)
data = {
    "crop": "wheat", "lat": 26.4, "lon": 84.4
}

response = requests.post(url, json=data)
print(response.json())