import requests

# -------------------------------------------------
# FETCH WEATHER DATA FROM NASA API
# -------------------------------------------------

def get_weather_data(lat, lon):

    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    params = {
        "parameters": "T2M,PRECTOTCORR",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": "20240101",
        "end": "20240110",
        "format": "JSON"
    }

    print("Fetching data from NASA...")

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return {"status": "error"}

        data = response.json()

        # Extract temperature data
        temps = list(data["properties"]["parameter"]["T2M"].values())

        # Extract rainfall data
        rains = list(data["properties"]["parameter"]["PRECTOTCORR"].values())

        avg_temp = sum(temps) / len(temps)
        total_rain = sum(rains)

        return {
            "status": "success",
            "avg_temp": avg_temp,
            "total_rain": total_rain
        }

    except Exception as e:
        print("Weather API Error:", e)
        return {"status": "error"}