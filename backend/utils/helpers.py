import requests

def get_weather_data(lat, lon):
    """
    Fetches and cleans weather data from NASA POWER API.
    Returns average temperature and total rainfall.
    """
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "T2M,PRECTOTCORR",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": "20240101",
        "end": "20240107",
        "format": "JSON"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract required data
        weather_values = data["properties"]["parameter"]
        temp_dict = weather_values["T2M"]
        rain_dict = weather_values["PRECTOTCORR"]

        # Remove None values
        valid_temps = [t for t in temp_dict.values() if t is not None]
        valid_rain = [r for r in rain_dict.values() if r is not None]

        # Safety check
        if not valid_temps:
            return {
                "status": "error",
                "message": "No valid weather data found for this location."
            }

        avg_temp = sum(valid_temps) / len(valid_temps)
        total_rain = sum(valid_rain)

        return {
            "status": "success",
            "avg_temp": round(avg_temp, 2),
            "total_rain": round(total_rain, 2)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
