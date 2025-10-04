# backend/app/main.py
import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from typing import List

from .schemas import WeatherResponse, Weather, Suggestion
from .services.weather import fetch_weather_by_location  # unified fetcher

load_dotenv()  # read .env if present

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
if ALLOWED_ORIGINS == "*":
    allow_origins: List[str] = ["*"]
else:
    allow_origins = [o.strip() for o in ALLOWED_ORIGINS.split(",") if o.strip()]

app = FastAPI(title="Outfit Guide API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# For Vercel serverless, we don't serve static files from the backend
# The frontend will be served by Vercel's static hosting


@app.get("/api/weather", response_model=WeatherResponse)
async def get_weather(location: str = Query(..., description="Location name e.g. 'New Delhi,IN' or 'London'")):
    try:
        # fetch_weather_by_location returns a normalized dict already
        weather_dict = await fetch_weather_by_location(location)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    weather = Weather(**weather_dict)
    suggestions = build_suggestions_from_weather(weather)
    return WeatherResponse(weather=weather, suggestions=suggestions)


def build_suggestions_from_weather(weather: Weather) -> List[Suggestion]:
    t = weather.temperature
    cond = (weather.condition or "").lower()
    sugg = []

    # Simple rule-based suggestions — expand as you like
    if "rain" in cond or "drizzle" in cond:
        sugg.append(Suggestion(title="Rain Gear", description="Waterproof jacket and umbrella"))
    if "snow" in cond:
        sugg.append(Suggestion(title="Warm Winter Coat", description="Insulated coat, gloves, and hat"))
    if t >= 30:
        sugg.append(Suggestion(title="Light Clothing", description="Breathable cotton or linen clothes"))
    elif t >= 20:
        sugg.append(Suggestion(title="Mild Weather", description="Light layers — t-shirt with a thin jacket"))
    elif t >= 10:
        sugg.append(Suggestion(title="Cool Weather", description="Sweater or light jacket"))
    else:
        sugg.append(Suggestion(title="Cold Weather", description="Heavy coat, scarf, gloves"))

    # add a generic suggestion
    if not any("rain" in (s.description.lower()) for s in sugg):
        # if not raining, suggest sun protection when hot
        if t >= 25:
            sugg.append(Suggestion(title="Sun Protection", description="Sunglasses and sunscreen"))

    return sugg
