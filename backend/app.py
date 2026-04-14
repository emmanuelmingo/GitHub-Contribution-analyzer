from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from config import BaseUrl, CACHE_CONFIG, FRONTEND_ORIGINS
from analyzers.language import analyze_language
from analyzers.repo import analyze_repo
from analyzers.commit_frequency import analyze_commit_frequency
from analyzers.streaks import analyze_streaks
from analyzers.scorer import calculate_score
import requests

app = Flask(__name__)
CORS(app, origins=FRONTEND_ORIGINS)
cache = Cache(app, config=CACHE_CONFIG)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route("/api/analyze/<username>")
@cache.cached(timeout=3600)
def get_user_info(username):
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(f"{BaseUrl}/users/{username}", headers=headers)

    if response.status_code == 404:
        return {"error": "User not found"}, 404
    if response.status_code == 403:
        return {"error": "Rate limit exceeded"}, 429
    if not response.ok:
        return {"error": "GitHub API unavailable"}, 502

    user_data = response.json()

    repo_response = requests.get(user_data["repos_url"], headers=headers)
    if not repo_response.ok:
        return {"error": "Could not fetch repositories"}, 502

    repos = repo_response.json()

    language = analyze_language(repos)
    repo_stats = analyze_repo(repos)
    frequency = analyze_commit_frequency(username, repos, BaseUrl, headers)
    streaks = analyze_streaks(username, repos, BaseUrl, headers)
    score = calculate_score(frequency, streaks, language, repo_stats)

    return {
        "username": user_data["login"],
        "name": user_data["name"],
        "bio": user_data["bio"],
        "avatar_url": user_data["avatar_url"],
        "public_repos": user_data["public_repos"],
        "followers": user_data["followers"],
        "following": user_data["following"],
        "score": score,
        "language": language,
        "repo_stats": repo_stats,
        "frequency": frequency,
        "streaks": streaks,
    }


if __name__ == "__main__":
    app.run(debug=True)
