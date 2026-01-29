import React, { useEffect, useState } from 'react'

export default function App() {
  const [message, setMessage] = useState('')

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_URL || '/api'
    // Example fetch just to show usage of VITE_API_URL
    fetch(apiUrl)
      .then((r) => r.json())
      .then((d) => setMessage(JSON.stringify(d)))
      .catch(() => setMessage('API not available'))
  }, [])

  return (
    <div style={{ padding: 16 }}>
      <h1>Financial Dashboard (Vite)</h1>
      <p>{message || 'No data yet'}</p>
    </div>
  )
}
