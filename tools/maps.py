import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MAPS_API_KEY")

# Step 1: Convert city → coordinates
def get_coordinates(city):
    url = "https://api.openrouteservice.org/geocode/search"

    params = {
        "api_key": API_KEY,
        "text": city
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        coords = data["features"][0]["geometry"]["coordinates"]
        return coords  # [lon, lat]
    except:
        return None


# Step 2: Get distance
def get_distance(city1, city2):
    coords1 = get_coordinates(city1)
    coords2 = get_coordinates(city2)

    if not coords1 or not coords2:
        return "Could not find one of the locations"

    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [coords1, coords2]
    }

    response = requests.post(url, json=body, headers=headers)
    data = response.json()

    try:
        distance_km = data["routes"][0]["summary"]["distance"] / 1000
        return f"Distance between {city1} and {city2} is {distance_km:.2f} km"
    except:
        return "Error calculating distance"