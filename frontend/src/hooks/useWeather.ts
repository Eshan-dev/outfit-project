export type Weather = {
  location: string
  temperature: number
  condition: string
  humidity?: number
  windSpeed?: number
  feelsLike?: number
}

export type Suggestion = { title: string; description: string }

export type WeatherResponse = { weather: Weather; suggestions: Suggestion[] }
