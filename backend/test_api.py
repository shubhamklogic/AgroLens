import requests

url = "http://127.0.0.1:5000/predict"

# Testing for a location in Bihar (Gopalganj area)
data = {
    "crop": "Wheat",
    "lat": 26.47,
    "lon": 84.44
}

response = requests.post(url, json=data)
print(response.json())