from flask import Flask
from config import BaseUrl
from analyzers.language import analyze_language
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/api/analyze/<username>")
def get_user_info(username):
    try:
        response = requests.get(
            f"{BaseUrl}/users/{username}",
            headers={"Accept": "application/vnd.github.v3+json"}
        )
        if response.status_code == 404:
            return {"error":"User not found"}, 404
        if response.status_code == 403:
            return {"error": "Rate limit exceeded"}, 429
        
        response.raise_for_status()
        requests_left = response.headers.get("X-RateLimit-Remaining")
        limit = response.headers.get("X-RateLimit-Limit")
        reset = response.headers.get("X-RateLimit-Reset")

        user_data = response.json()
        #print(user_data, end='\n')
        repo_reponse = requests.get(user_data["repos_url"])
        language = analyze_language(repo_reponse.json())
        print(language)

        return {
            "username": user_data["login"],
            "name": user_data["name"],
            "bio": user_data["bio"],
            "public_repos": user_data["public_repos"],
            "followers": user_data["followers"],
            "following": user_data["following"],
            "Requests left": requests_left
        }
    except:
        return {"error":"GitHub Api Unavailable"},502

if __name__ == "__main__":
    app.run(debug=True)