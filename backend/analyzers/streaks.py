from datetime import datetime, timedelta
import requests

def analyze_streaks(username, repos, base_url, headers):
    commit_dates = set()

    for repo in repos:
        if repo.get('fork'):
            continue
        url = f"{base_url}/repos/{username}/{repo['name']}/commits"
        response = requests.get(url, headers=headers, params={"per_page": 100})
        if response.status_code != 200:
            continue

        for commit in response.json():
            date_str = commit.get('commit', {}).get('author', {}).get('date', '')
            if date_str:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                commit_dates.add(dt.date())

    if not commit_dates:
        return {"longest_streak": 0, "current_streak": 0, "total_active_days": 0}

    sorted_dates = sorted(commit_dates)

    longest = 1
    current = 1
    for i in range(1, len(sorted_dates)):
        if sorted_dates[i] - sorted_dates[i - 1] == timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    today = datetime.utcnow().date()
    current_streak = 0
    check_date = today
    while check_date in commit_dates:
        current_streak += 1
        check_date -= timedelta(days=1)

    return {
        "longest_streak": longest,
        "current_streak": current_streak,
        "total_active_days": len(commit_dates)
    }