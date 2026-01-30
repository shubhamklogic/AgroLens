import requests

# The URL of your local Flask server
url = "http://127.0.0.1:5000/predict"

# The data you want to send to the backend
data = {"crop": "Rice"}

# Sending the POST request
response = requests.post(url, json=data)

# Printing the result
print("Status Code:", response.status_code)
print("Response from Backend:", response.json())