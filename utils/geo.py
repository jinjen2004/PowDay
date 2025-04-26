# utils/geo.py
from math import radians, cos, sin, asin, sqrt
from geopy import Nominatim                       #  pip install geopy

geocoder = Nominatim(user_agent="powday-search")   # free OpenStreetMap geocoder

def geocode(text: str) -> tuple[float, float] | None:
    """Turn 'Salt Lake City, UT' → (40.7608, -111.8910)."""
    loc = geocoder.geocode(text, exactly_one=True, timeout=10)
    return (loc.latitude, loc.longitude) if loc else None


def haversine_mi(lat1, lon1, lat2, lon2):
    """Great-circle distance in miles."""
    R = 3958.8                                    # Earth radius (mi)
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    dlat  = lat2 - lat1
    dlon  = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))
