import { useState } from 'react'
import './App.css'
import ProfileCard from './components/ProfileCard'
import ScoreCard from './components/ScoreCard'
import LanguagePieChart from './components/LanguagePieChart'
import CommitBarChart from './components/CommitBarChart'
import ActivityLineChart from './components/ActivityLineChart'

export default function App() {
  const [input, setInput] = useState('')
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSearch(e) {
    e.preventDefault()
    const username = input.trim()
    if (!username) return
    setLoading(true)
    setError(null)
    setData(null)
    try {
      const res = await fetch(`/api/analyze/${username}`)
      if (!res.ok) {
        const json = await res.json().catch(() => ({}))
        setError(json.error || `Server error ${res.status}`)
        return
      }
      const json = await res.json()
      setData(json)
    } catch {
      setError('Could not reach the server — make sure the Flask API is running on port 5000.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>GitHub Contribution Analyzer</h1>
        <p>Enter a GitHub username to analyze their contribution patterns</p>
      </header>

      <form className="search-form" onSubmit={handleSearch}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="GitHub username"
          disabled={loading}
          autoComplete="off"
          spellCheck={false}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing…' : 'Analyze'}
        </button>
      </form>

      {loading && <div className="loading">Fetching data from GitHub…</div>}
      {error && <div className="error-msg">{error}</div>}

      {data && (
        <div className="results">
          <div className="row-two-col">
            <ProfileCard data={data} />
            <ScoreCard score={data.score} />
          </div>
          <div className="row-two-col">
            <LanguagePieChart language={data.language} />
            <CommitBarChart byDay={data.frequency.by_day} />
          </div>
          <ActivityLineChart byDate={data.frequency.by_date} />
        </div>
      )}
    </div>
  )
}
