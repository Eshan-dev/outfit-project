# backend/app/services/weather.py
"""
Service wrapper: if OPENWEATHER_KEY present -> use OpenWeather;
otherwise use Nominatim (geocode) + Open-Meteo (no key required).
"""
import os
from typing import Dict, Any, Tuple, Optional
import httpx
import math

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# Simple mapping of open-meteo weather codes to human text (not exhaustive).
_WEATHERCODE_MAP = {
    0: "Clear",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Rain showers (moderate)",
    82: "Rain showers (violent)",
    95: "Thunderstorm",
}

async def fetch_weather_by_location(location: str) -> Dict[str, Any]:
    """
    Unified entry: returns a normalized dict with keys:
    { location, temperature, condition, humidity, windSpeed, feelsLike }
    """
    if OPENWEATHER_KEY:
        # use OpenWeather (requires key)
        raw = await _fetch_openweather_by_location(location)
        return _normalize_openweather(raw)
    else:
        # fallback: geocode with Nominatim, then call Open-Meteo
        geodata = await _geocode_nominatim(location)
        if geodata is None:
            raise RuntimeError(f"Could not geocode location: {location}")
        lat, lon, display = geodata
        raw = await _fetch_open_meteo(lat, lon)
        return _normalize_open_meteo(raw, display, lat, lon)

# -----------------------
# OpenWeather helpers
# -----------------------
async def _fetch_openweather_by_location(location: str) -> Dict[str, Any]:
    if not OPENWEATHER_KEY:
        raise RuntimeError("OPENWEATHER_KEY not configured")
    params = {"q": location, "appid": OPENWEATHER_KEY, "units": "metric"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(OPENWEATHER_URL, params=params)
        r.raise_for_status()
        return r.json()

def _normalize_openweather(data: Dict[str, Any]) -> Dict[str, Any]:
    name = data.get("name", "")
    sys = data.get("sys", {})
    weather = (data.get("weather") or [{}])[0]
    main = data.get("main", {}) or {}
    wind = data.get("wind", {}) or {}

    return {
        "location": f"{name}, {sys.get('country','')}".strip(", "),
        "temperature": float(main.get("temp", 0.0)),
        "condition": weather.get("main", ""),
        "humidity": main.get("humidity"),
        "windSpeed": wind.get("speed"),
        "feelsLike": float(main.get("feels_like", main.get("temp", 0.0))),
    }

# -----------------------
# Nominatim geocoding
# -----------------------
async def _geocode_nominatim(location: str) -> Optional[Tuple[float, float, str]]:
    """
    Returns (lat, lon, display_name) or None
    """
    params = {"q": location, "format": "json", "limit": 1}
    headers = {"User-Agent": "outfit-guide/1.0 (contact: you@example.com)"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(NOMINATIM_URL, params=params, headers=headers)
        r.raise_for_status()
        arr = r.json()
        if not arr:
            return None
        first = arr[0]
        lat = float(first.get("lat"))
        lon = float(first.get("lon"))
        display = first.get("display_name", location)
        return lat, lon, display

# -----------------------
# Open-Meteo helpers
# -----------------------
async def _fetch_open_meteo(lat: float, lon: float) -> Dict[str, Any]:
    """
    Call open-meteo for current weather. We request current_weather=true and timezone=auto.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "auto",  # returns times in local timezone
        # humidity isn't present in current_weather; additional queries could request hourly humidity
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(OPEN_METEO_URL, params=params)
        r.raise_for_status()
        return r.json()

def _normalize_open_meteo(raw: Dict[str, Any], display_location: str, lat: float, lon: float) -> Dict[str, Any]:
    """
    Normalize Open-Meteo response to the same shape used by the rest of the app.
    raw example contains a 'current_weather' dict with keys: temperature, windspeed, winddirection, weathercode, time
    """
    cw = raw.get("current_weather") or {}
    temp = cw.get("temperature")
    wind = cw.get("windspeed")
    code = cw.get("weathercode")
    # Open-Meteo's current_weather doesn't include humidity; leave as None
    condition = _WEATHERCODE_MAP.get(int(code) if code is not None else -1, f"Weather code {code}")

    # Optionally, compute feelsLike as temp (no RH available) — keep same number
    feels_like = float(temp) if temp is not None else None

    loc_str = display_location or f"{lat:.4f},{lon:.4f}"
    return {
        "location": loc_str,
        "temperature": float(temp) if temp is not None else 0.0,
        "condition": condition,
        "humidity": None,
        "windSpeed": float(wind) if wind is not None else None,
        "feelsLike": feels_like,
    }
