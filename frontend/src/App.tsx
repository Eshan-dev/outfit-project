import React, { useState } from 'react'
import SearchBar from './components/SearchBar'
import WeatherCard from './components/WeatherCard'
import type { WeatherResponse } from './hooks/useWeather'

export default function App(){
  const [data, setData] = useState<WeatherResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSearch(location: string){
    setLoading(true)
    setError(null)
    setData(null)
    try{
      // For full-stack Vercel deployment, use relative API path
      const res = await fetch(`/api/weather?location=${encodeURIComponent(location)}`)
      if(!res.ok) throw new Error(`Server error: ${res.status}`)
      const json = await res.json()
      setData(json)
    }catch(err:any){
      setError(err.message || 'Unknown error')
    }finally{
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="app-header">
        <h1 className="app-title">Outfit Guide</h1>
        <p className="app-subtitle">Get personalized clothing recommendations based on weather</p>
      </div>
      <div className="card">
        <SearchBar onSearch={handleSearch} />
        {loading && <div className="loading">Loading weather data...</div>}
        {error && <div className="error">{error}</div>}
        {data && <div className="weather" suppressHydrationWarning><WeatherCard key={data.weather.location} data={data} /></div>}
      </div>
    </div>
  )
}
