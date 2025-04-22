# weather.py  (new helper file – import it in app.py)
import os, time, requests, functools
from typing import Dict, Any, List
from datetime import datetime as dt

API_KEY = "6a8dc08d5123e7c104b59aa3b4c138d1" # This is horrible practice but i never put any payment on the api so fingers crossed
BASE = "https://api.openweathermap.org/data"

# ---- tiny decorator for in‑memory caching ---------------------------------
def ttl_cache(seconds: int):
    def wrapper(func):
        cache: Dict[str, Any] = {}
        stamp: Dict[str, float] = {}
        @functools.wraps(func)
        def inner(*args):
            k = repr(args)
            if k in cache and time.time() - stamp[k] < seconds:
                return cache[k]
            cache[k] = val = func(*args)
            stamp[k] = time.time()
            return val
        return inner
    return wrapper

@ttl_cache(600)             # 10 min is fine for current weather
def current(lat: float, lon: float) -> Dict[str, Any]:
    r = requests.get(f"{BASE}/2.5/weather",
                     params={"lat": lat, "lon": lon,
                             "units": "imperial", "appid": API_KEY},
                     timeout=4)
    r.raise_for_status()
    j = r.json()
    return {
        "temp": round(j["main"]["temp"]),
        "feels_like": round(j["main"]["feels_like"]),
        "wind":  round(j["wind"]["speed"]),
        "gust":  round(j.get("wind", {}).get("gust", 0)),
        "desc":  j["weather"][0]["description"].title(),
        "icon":  j["weather"][0]["icon"],
        # snow volume (mm) for last 1 h / 3 h – might be missing
        "snow_1h":  j.get("snow", {}).get("1h", 0),
        "snow_3h":  j.get("snow", {}).get("3h", 0)
    }

@ttl_cache(1800)            # 30 min – hourly forecast rarely changes faster
def hourly(lat: float, lon: float) -> List[Dict[str, Any]]:
    """
    Returns next 48 × 1 h buckets (OpenWeather ‘forecast’ endpoint is 3 h;
    we’ll aggregate to hourly by repeating values).
    """
    r = requests.get(f"{BASE}/2.5/forecast",
                     params={"lat": lat, "lon": lon,
                             "units": "imperial", "appid": API_KEY},
                     timeout=4)
    r.raise_for_status()
    out = []
    for slot in r.json()["list"][:16]:      # ≈ next 48 h (16 × 3 h)
        out.append({
            "dt": slot["dt"],
            "temp": round(slot["main"]["temp"]),
            "wind": slot["wind"]["speed"],
            "gust": slot["wind"].get("gust", 0),
            "snow": slot.get("snow", {}).get("3h", 0),
            "pop": slot["pop"]             # probability of precip (0‑1)
        })
    return out

@ttl_cache(3600)            
def daily(lat: float, lon: float) -> List[Dict[str, Any]]:
    r = requests.get(f"{BASE}/2.5/forecast/daily",
                     params={"lat": lat, "lon": lon,
                              "units": "imperial",
                             "appid": API_KEY},
                     timeout=4)
    r.raise_for_status()
    out = []
    for d in r.json()["list"]:
        out.append({
            "dt": d["dt"],
            "min": round(d["temp"]["min"]),
            "max": round(d["temp"]["max"]),
            "snow": d.get("snow", 0),
            "wind": d["speed"],
            "prob": d.get("pop", 0)
        })
    for d in out:                       # inside your daily() helper
        d["day"] = dt.fromtimestamp(d["dt"]).strftime("%a %m/%d")
    return out

def ski_summary(hourly_data):
    # next‑24‑h fresh snow & worst wind‑gust
    next24 = hourly_data[:8]                       # 8 × 3 h ≈ 24 h
    fresh_snow_in = round(sum(h["snow"] for h in next24), 1)
    max_gust = round(max(h["gust"] for h in next24), 1)
    coldest = round(min(h["temp"] for h in next24))
    return {
        "fresh_24h": fresh_snow_in,    # mm or “0” if none
        "max_gust": max_gust,          # mph
        "coldest": coldest             # °F
    }


