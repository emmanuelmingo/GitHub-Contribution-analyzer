import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const DAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
const DAY_SHORT = {
  Monday: 'Mon', Tuesday: 'Tue', Wednesday: 'Wed',
  Thursday: 'Thu', Friday: 'Fri', Saturday: 'Sat', Sunday: 'Sun',
}

export default function CommitBarChart({ byDay }) {
  const data = DAY_ORDER.map(day => ({
    day: DAY_SHORT[day],
    commits: byDay[day] || 0,
  }))

  if (data.every(d => d.commits === 0)) {
    return (
      <div className="card">
        <h3>Commits by Day of Week</h3>
        <p style={{ color: '#586069', fontSize: 14 }}>No commit data available.</p>
      </div>
    )
  }

  return (
    <div className="card">
      <h3>Commits by Day of Week</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e1e4e8" />
          <XAxis dataKey="day" tick={{ fontSize: 13 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
          <Tooltip cursor={{ fill: '#f6f8fa' }} />
          <Bar dataKey="commits" fill="#0366d6" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
