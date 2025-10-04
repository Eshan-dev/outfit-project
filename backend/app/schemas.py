from pydantic import BaseModel
from typing import Optional, List

class Weather(BaseModel):
    location: str
    temperature: float
    condition: str
    humidity: Optional[int]
    windSpeed: Optional[float]
    feelsLike: Optional[float]

class Suggestion(BaseModel):
    title: str
    description: str

class WeatherResponse(BaseModel):
    weather: Weather
    suggestions: List[Suggestion]
