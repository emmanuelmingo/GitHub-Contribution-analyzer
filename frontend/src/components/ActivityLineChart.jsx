import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function ActivityLineChart({ byDate }) {
  if (!byDate || Object.keys(byDate).length === 0) {
    return (
      <div className="card">
        <h3>Commit Activity Over Time</h3>
        <p style={{ color: '#586069', fontSize: 14 }}>No activity data available.</p>
      </div>
    )
  }

  const today = new Date()
  const start = new Date(today)
  start.setDate(today.getDate() - 89)

  const data = []
  for (let d = new Date(start); d <= today; d.setDate(d.getDate() + 1)) {
    const iso = d.toISOString().slice(0, 10)
    data.push({ date: iso.slice(5), commits: byDate[iso] || 0 })
  }

  const tickInterval = Math.floor(data.length / 8)

  return (
    <div className="card">
      <h3>Commit Activity — Last 90 Days</h3>
      <ResponsiveContainer width="100%" height={240}>
        <LineChart data={data} margin={{ top: 10, right: 20, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e1e4e8" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 12 }}
            axisLine={false}
            tickLine={false}
            interval={tickInterval}
          />
          <YAxis tick={{ fontSize: 12 }} axisLine={false} tickLine={false} allowDecimals={false} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="commits"
            stroke="#0366d6"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4, strokeWidth: 0 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
