import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const COLORS = ['#0366d6', '#28a745', '#e36209', '#6f42c1', '#d73a49', '#0075ca', '#22863a', '#b08800']

export default function LanguagePieChart({ language }) {
  if (!language || language.length === 0) {
    return (
      <div className="card">
        <h3>Language Distribution</h3>
        <p style={{ color: '#586069', fontSize: 14 }}>No language data available.</p>
      </div>
    )
  }

  const data = language.map(([name, value]) => ({ name, value }))

  return (
    <div className="card">
      <h3>Language Distribution</h3>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={65}
            outerRadius={105}
            paddingAngle={2}
            dataKey="value"
          >
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(v) => `${v}%`} />
          <Legend iconType="circle" iconSize={10} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
