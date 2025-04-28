import math
import requests
from typing import Tuple

def geocode_location(location_name: str) -> Tuple[float, float]:
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location_name,
        "key": "AIzaSyDzDUoFbFMjXUroFZEJgmuORhurXdoZR7E"
    }
    response = requests.get(url, params=params)
    result = response.json()

    if result["status"] == "OK":
        location = result["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        raise ValueError(f"Geocoding failed: {result['status']}")

def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2.0)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c
    miles = meters / 1609.34
    return miles
