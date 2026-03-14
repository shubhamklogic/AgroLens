import requests
from datetime import datetime, timedelta

# -------------------------------------------------
# FETCH WEATHER DATA FROM NASA POWER API
# This function fetches weather data using latitude
# and longitude provided by the user.
#
# Data fetched from NASA:
# 1. Average Temperature (T2M)
# 2. Total Rainfall (PRECTOTCORR)
# 3. Average Humidity (RH2M)
#
# We fetch the weather of the LAST 7 DAYS from
# the current date for better crop prediction.
# -------------------------------------------------

def get_weather_data(lat, lon):

    # -------------------------------------------------
    # CALCULATE DATE RANGE (LAST 7 DAYS)
    # -------------------------------------------------
    today = datetime.today()
    start_date = (today - timedelta(days=7)).strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")

    # NASA POWER API endpoint
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    # -------------------------------------------------
    # API PARAMETERS
    #
    # T2M = Temperature at 2 meters
    # PRECTOTCORR = Rainfall
    # RH2M = Relative Humidity
    # -------------------------------------------------
    params = {
        "parameters": "T2M,PRECTOTCORR,RH2M",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_date,
        "end": end_date,
        "format": "JSON"
    }

    print("Fetching data from NASA...")

    try:

        # -------------------------------------------------
        # SEND REQUEST TO NASA API
        # -------------------------------------------------
        response = requests.get(url, params=params)

        # If API request fails, return error
        if response.status_code != 200:
            return {"status": "error"}

        data = response.json()

        # -------------------------------------------------
        # EXTRACT WEATHER DATA
        # NASA returns data inside nested JSON structure
        # -------------------------------------------------
        temps = list(data["properties"]["parameter"]["T2M"].values())
        rains = list(data["properties"]["parameter"]["PRECTOTCORR"].values())
        humidity_values = list(data["properties"]["parameter"]["RH2M"].values())

        # -------------------------------------------------
        # REMOVE INVALID NASA VALUES
        # NASA uses -999 when data is missing
        # -------------------------------------------------
        temps = [t for t in temps if t != -999]
        rains = [r for r in rains if r != -999]
        humidity_values = [h for h in humidity_values if h != -999]

        # -------------------------------------------------
        # SAFETY CHECK (IMPORTANT)
        # Prevent "Division by Zero" errors.
        # If NASA returns empty lists (all values -999),
        # calculating averages would crash the server.
        # -------------------------------------------------
        if len(temps) == 0 or len(rains) == 0 or len(humidity_values) == 0:
            return {
                "status": "error",
                "message": "No valid meteorological data found."
            }

        # -------------------------------------------------
        # CALCULATE FINAL WEATHER FEATURES
        # These values will be used by the ML model
        # -------------------------------------------------
        avg_temp = sum(temps) / len(temps)
        total_rain = sum(rains)
        avg_humidity = sum(humidity_values) / len(humidity_values)

        # -------------------------------------------------
        # RETURN CLEAN WEATHER DATA TO BACKEND
        # -------------------------------------------------
        return {
            "status": "success",
            "avg_temp": avg_temp,
            "total_rain": total_rain,
            "humidity": avg_humidity
        }

    except Exception as e:
        # Catch unexpected errors such as network issues
        print("Weather API Error:", e)
        return {"status": "error"}