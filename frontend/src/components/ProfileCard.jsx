export default function ProfileCard({ data }) {
  return (
    <div className="card">
      <h3>Profile</h3>
      <div className="profile-header">
        <img src={data.avatar_url} alt={data.username} className="avatar" />
        <div>
          <div className="profile-name">{data.name || data.username}</div>
          <div className="profile-username">@{data.username}</div>
          {data.bio && <div className="profile-bio">{data.bio}</div>}
        </div>
      </div>
      <div className="profile-stats">
        <div className="stat">
          <span className="stat-value">{data.public_repos}</span>
          <span className="stat-label">Repos</span>
        </div>
        <div className="stat">
          <span className="stat-value">{data.followers}</span>
          <span className="stat-label">Followers</span>
        </div>
        <div className="stat">
          <span className="stat-value">{data.following}</span>
          <span className="stat-label">Following</span>
        </div>
        <div className="stat">
          <span className="stat-value">{data.streaks.current_streak}</span>
          <span className="stat-label">Streak</span>
        </div>
      </div>
    </div>
  )
}
