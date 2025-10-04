import React from 'react'

export default function WeatherCard({ data }: { data: any }){
  const w = data.weather
  const suggestions = data.suggestions || []
  
  return (
    <div className="weather-card">
      {/* Weather Header */}
      <div className="weather-header">
        <h2 className="location">{w.location}</h2>
        <div className="condition">{w.condition}</div>
        <div className="temperature">{w.temperature}°C</div>
        <div className="feels-like">Feels like {w.feelsLike}°C</div>
      </div>

      {/* Weather Details Grid */}
      <div className="weather-details">
        <div className="detail-item">
          <div className="detail-label">Wind Speed</div>
          <div className="detail-value">{w.windSpeed ?? '—'} m/s</div>
        </div>
      </div>

      {/* Suggestions Section */}
      {suggestions.length > 0 && (
        <div className="suggestions">
          <h3 className="suggestions-title">Outfit Recommendations</h3>
          <ul className="suggestions-list">
            {suggestions.map((s: any, i: number) => (
              <li key={i} className="suggestion-item">
                <div className="suggestion-title">{s.title}</div>
                <div className="suggestion-description">{s.description}</div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
