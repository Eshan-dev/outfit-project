import React, { useState } from 'react'

export default function SearchBar({ onSearch }: { onSearch: (loc: string)=>void }){
  const [q, setQ] = useState('New Delhi')

  function submit(e?: React.FormEvent){
    e?.preventDefault()
    if(!q) return
    onSearch(q)
  }

  return (
    <form onSubmit={submit} className="search">
      <input 
        value={q} 
        onChange={e=>setQ(e.target.value)} 
        placeholder="Enter city name (e.g. New Delhi, London, Tokyo)" 
        className="search-input"
      />
      <button type="submit" className="search-button">
        <span>Get Weather</span>
      </button>
    </form>
  )
}
