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

        # Send request to NASA API
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return {"status": "error"}

        data = response.json()

        # -------------------------------------------------
        # EXTRACT WEATHER DATA
        # -------------------------------------------------
        temps = list(data["properties"]["parameter"]["T2M"].values())
        rains = list(data["properties"]["parameter"]["PRECTOTCORR"].values())
        humidity_values = list(data["properties"]["parameter"]["RH2M"].values())

        # -------------------------------------------------
        # REMOVE INVALID NASA VALUES (-999 means missing)
        # -------------------------------------------------
        temps = [t for t in temps if t != -999]
        rains = [r for r in rains if r != -999]
        humidity_values = [h for h in humidity_values if h != -999]

        # -------------------------------------------------
        # CHECK IF DATA EXISTS
        # -------------------------------------------------
        if not temps or not rains or not humidity_values:
            return {"status": "error"}

        # -------------------------------------------------
        # CALCULATE FINAL WEATHER FEATURES
        # -------------------------------------------------
        avg_temp = sum(temps) / len(temps)
        total_rain = sum(rains)
        avg_humidity = sum(humidity_values) / len(humidity_values)

        # -------------------------------------------------
        # RETURN CLEAN DATA TO BACKEND
        # -------------------------------------------------
        return {
            "status": "success",
            "avg_temp": avg_temp,
            "total_rain": total_rain,
            "humidity": avg_humidity
        }

    except Exception as e:
        print("Weather API Error:", e)
        return {"status": "error"}