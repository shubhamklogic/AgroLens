import requests

def is_land_location(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"

        response = requests.get(url, headers={"User-Agent": "AgroLens-App"})
        data = response.json()

        # If no address found → likely ocean
        if "address" not in data:
            return False

        return True

    except:
        return False
