import requests

# 1. Fetch weather data from NASA POWER API
url = "https://power.larc.nasa.gov/api/temporal/daily/point"
params = {
    "parameters": "T2M,PRECTOTCORR",
    "community": "AG",
    "longitude": 77.2,
    "latitude": 28.6,
    "start": "20240101",
    "end": "20240105",
    "format": "JSON"
}

response = requests.get(url, params=params)
raw_data = response.json()

# 2. Clean the data
weather_data = raw_data["properties"]["parameter"]

temp_dict = weather_data["T2M"]
rain_dict = weather_data["PRECTOTCORR"]

print("--- Cleaned Weather Data ---")
for date in temp_dict:
    temp = temp_dict[date]
    rain = rain_dict[date]
    print(f"Date: {date} | Temp: {temp}°C | Rain: {rain} mm")

# 3. Calculate average temperature (safe calculation)
valid_temps = [t for t in temp_dict.values() if t is not None]
avg_temp = sum(valid_temps) / len(valid_temps)

print("\nSummary for Farmer:")
print(f"Average Temperature: {avg_temp:.2f}°C")