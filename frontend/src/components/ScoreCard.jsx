function scoreColor(score) {
  if (score >= 75) return '#28a745'
  if (score >= 50) return '#e36209'
  return '#d73a49'
}

function scoreTier(score) {
  if (score >= 85) return 'Expert'
  if (score >= 70) return 'Advanced'
  if (score >= 50) return 'Active'
  if (score >= 30) return 'Developing'
  return 'Beginner'
}

const LABELS = {
  commit_volume: 'Commit Volume',
  commit_spread: 'Day Spread',
  longest_streak: 'Longest Streak',
  active_days: 'Active Days',
  language_diversity: 'Languages',
  original_repos: 'Original Repos',
  star_count: 'Stars',
  original_ratio: 'Original Work',
}

export default function ScoreCard({ score }) {
  const color = scoreColor(score.overall)
  const tier = scoreTier(score.overall)

  return (
    <div className="card">
      <h3>Contributor Score</h3>
      <div className="score-display">
        <div className="score-circle" style={{ borderColor: color }}>
          <span className="score-number" style={{ color }}>{score.overall}</span>
          <span className="score-denom">/100</span>
        </div>
        <div>
          <div className="score-tier">{tier}</div>
          <div className="score-desc">
            Based on commit patterns, language breadth, streaks, and original work.
          </div>
        </div>
      </div>
      <div className="breakdown-grid">
        {Object.entries(score.breakdown).map(([key, value]) => {
          const max = score.weights[key]
          const pct = max > 0 ? (value / max) * 100 : 0
          return (
            <div key={key} className="metric-row">
              <div className="metric-labels">
                <span>{LABELS[key] || key}</span>
                <span>{value} / {max}</span>
              </div>
              <div className="bar-bg">
                <div className="bar-fill" style={{ width: `${pct}%`, background: color }} />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
