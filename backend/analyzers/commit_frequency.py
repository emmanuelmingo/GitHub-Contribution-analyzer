from collections import defaultdict
from datetime import datetime
import requests

def analyze_commit_frequency(username, repos, base_url, headers):
    days = defaultdict(int)
    hours = defaultdict(int)
    by_date = defaultdict(int)
    total_commits = 0

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
                days[dt.strftime('%A')] += 1
                hours[dt.hour] += 1
                by_date[dt.strftime('%Y-%m-%d')] += 1
                total_commits += 1

    return {
        "total_commits": total_commits,
        "by_day": dict(sorted(days.items(), key=lambda x: x[1], reverse=True)),
        "by_hour": dict(sorted(hours.items(), key=lambda x: x[1], reverse=True)),
        "by_date": dict(sorted(by_date.items())),
        "most_active_day": max(days, key=days.get) if days else None,
        "most_active_hour": max(hours, key=hours.get) if hours else None
    }