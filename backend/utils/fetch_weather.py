import requests
from datetime import datetime, timedelta

# -------------------------------------------------
# FETCH WEATHER DATA FROM NASA POWER API
# -------------------------------------------------
# This function retrieves weather data using
# latitude and longitude coordinates.
#
# Data fetched from NASA POWER API:
# 1. Average Temperature (T2M)
# 2. Total Rainfall (PRECTOTCORR)
# 3. Relative Humidity (RH2M)
#
# Weather data from the LAST 7 DAYS is used
# because agriculture decisions depend on
# recent environmental conditions.
# -------------------------------------------------

def get_weather_data(lat, lon):

    # -------------------------------------------------
    # CALCULATE DATE RANGE (LAST 7 DAYS)
    # -------------------------------------------------
    # NASA API requires date format: YYYYMMDD
    today = datetime.today()
    start_date = (today - timedelta(days=7)).strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")

    # NASA POWER API endpoint
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    # -------------------------------------------------
    # API PARAMETERS
    #
    # T2M          = Temperature at 2 meters
    # PRECTOTCORR  = Corrected rainfall
    # RH2M         = Relative humidity
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
        # timeout=10 prevents the backend from hanging
        # if NASA servers respond slowly or stop responding.
        # This is important for live demos and production APIs.
        # -------------------------------------------------
        response = requests.get(url, params=params, timeout=10)

        # If NASA API returns a failure HTTP status
        if response.status_code != 200:
            return {"status": "error"}

        data = response.json()

        # -------------------------------------------------
        # EXTRACT WEATHER DATA FROM NASA RESPONSE
        # -------------------------------------------------
        temps = list(data["properties"]["parameter"]["T2M"].values())
        rains = list(data["properties"]["parameter"]["PRECTOTCORR"].values())
        humidity_values = list(data["properties"]["parameter"]["RH2M"].values())

        # -------------------------------------------------
        # REMOVE INVALID NASA VALUES
        # -------------------------------------------------
        # NASA uses -999 when data is missing
        # These values must be removed before averaging
        # -------------------------------------------------
        temps = [t for t in temps if t != -999]
        rains = [r for r in rains if r != -999]
        humidity_values = [h for h in humidity_values if h != -999]

        # -------------------------------------------------
        # SAFETY CHECK
        # -------------------------------------------------
        # Prevent division-by-zero errors if NASA
        # returns empty datasets
        # -------------------------------------------------
        if len(temps) == 0 or len(rains) == 0:
            return {
                "status": "error",
                "message": "No valid meteorological data found."
            }

        # -------------------------------------------------
        # CALCULATE FINAL WEATHER FEATURES
        # -------------------------------------------------
        avg_temp = sum(temps) / len(temps)

        # Total rainfall accumulated in last 7 days
        total_rain = sum(rains)

        # -------------------------------------------------
        # HUMIDITY FALLBACK LOGIC
        # -------------------------------------------------
        # If NASA returns missing humidity data,
        # we safely default to 60% humidity.
        # This prevents ML model crashes.
        # -------------------------------------------------
        avg_humidity = sum(humidity_values) / len(humidity_values) if humidity_values else 60.0

        # -------------------------------------------------
        # RETURN CLEAN WEATHER DATA
        # -------------------------------------------------
        return {
    "status": "success",
    "avg_temp": round(avg_temp, 2),
    "total_rain": round(total_rain, 2),
    "humidity": round(avg_humidity, 2)
    }

    except requests.exceptions.Timeout:
        # -------------------------------------------------
        # TIMEOUT ERROR HANDLING
        # -------------------------------------------------
        # Happens when NASA API takes too long to respond.
        # Instead of crashing, we return a controlled error.
        # -------------------------------------------------
        print("Weather API Timeout")
        return {"status": "error"}

    except Exception as e:
        # -------------------------------------------------
        # GENERAL ERROR HANDLING
        # -------------------------------------------------
        # Handles unexpected errors such as:
        # - Network issues
        # - JSON parsing failures
        # -------------------------------------------------
        print("Weather API Error:", e)
        return {"status": "error"}