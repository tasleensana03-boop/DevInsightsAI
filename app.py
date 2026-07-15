from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    username = request.form["username"]

    # ----------------------------
    # GitHub Profile API
    # ----------------------------
    profile_url = f"https://api.github.com/users/{username}"
    response = requests.get(profile_url)

    if response.status_code != 200:
        return render_template("error.html")

    data = response.json()

    # ----------------------------
    # GitHub Repository API
    # ----------------------------
    repo_url = f"https://api.github.com/users/{username}/repos"
    repo_response = requests.get(repo_url)
    repositories = repo_response.json()

    # ----------------------------
    # Analytics Variables
    # ----------------------------
    top_repo = None
    max_stars = -1
    total_stars = 0

    languages = {}

    # ----------------------------
    # Analyze Repositories
    # ----------------------------
    for repo in repositories:

        # Total Stars
        total_stars += repo["stargazers_count"]

        # Languages
        language = repo["language"]

        if language:
            if language in languages:
                languages[language] += 1
            else:
                languages[language] = 1

        # Top Repository
        if repo["stargazers_count"] > max_stars:
            max_stars = repo["stargazers_count"]
            top_repo = repo

    # ----------------------------
    # Developer Intelligence
    # ----------------------------
    if total_stars >= 20:
        developer_type = "Open Source Contributor"
    elif len(repositories) >= 5:
        developer_type = "Active Developer"
    else:
        developer_type = "Growing Developer"

    if "Python" in languages:
        strength = "Python & AI Development"
    elif "JavaScript" in languages:
        strength = "Web Development"
    elif "HTML" in languages:
        strength = "Frontend Development"
    else:
        strength = "Exploring Multiple Technologies"

    # ----------------------------
    # Experience Level
    # ----------------------------
    if len(repositories) >= 20:
        experience = "Advanced"
    elif len(repositories) >= 10:
        experience = "Intermediate"
    else:
        experience = "Beginner"

    # ----------------------------
    # Developer Score
    # ----------------------------
    score = 0

    score += min(len(repositories) * 3, 30)
    score += min(data["followers"], 25)
    score += min(total_stars, 25)
    score += min(len(languages) * 5, 20)

    # ----------------------------
    # Developer Rank
    # ----------------------------
    if score >= 90:
        rank = "🏆 Platinum"
    elif score >= 75:
        rank = "🥇 Gold"
    elif score >= 50:
        rank = "🥈 Silver"
    else:
        rank = "🥉 Bronze"

    # ----------------------------
    # Render Page
    # ----------------------------
    return render_template(
        "result.html",
        avatar=data["avatar_url"],
        name=data["name"],
        username=data["login"],
        bio=data["bio"],
        location=data["location"],
        repos=data["public_repos"],
        followers=data["followers"],
        following=data["following"],
        repositories=repositories,
        top_repo=top_repo,
        total_stars=total_stars,
        languages=languages,
        developer_type=developer_type,
        strength=strength,
        experience=experience,
        score=score,
        rank=rank
    )
if __name__ == "__main__":
    app.run(debug=True)