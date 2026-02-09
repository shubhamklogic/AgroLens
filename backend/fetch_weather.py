import requests  # Importing the requests library to make HTTP API calls

# NASA POWER API URL for fetching daily point-based weather data
url = "https://power.larc.nasa.gov/api/temporal/daily/point"

# Parameters required by the NASA POWER API
params = {
    "parameters": "T2M,PRECTOTCORR",  # T2M = Temperature at 2 meters, PRECTOTCORR = Corrected rainfall
    "community": "AG",                # AG indicates agricultural community data
    "longitude": 77.2,                # Longitude of the selected location
    "latitude": 28.6,                 # Latitude of the selected location
    "start": "20240101",              # Start date in YYYYMMDD format
    "end": "20240110",                # End date in YYYYMMDD format
    "format": "JSON"                  # Response format set to JSON
}

# Sending the GET request to the NASA POWER API
print("Fetching data from NASA...")
response = requests.get(url, params=params)

# Checking if the request was successful
if response.status_code == 200:
    data = response.json()            # Converting the response into JSON format
    print("Successfully fetched data!")
    print(data)                       # Printing the full raw JSON response
else:
    print(f"Error: {response.status_code}")  # Printing error code if request fails