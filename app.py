from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    username = request.form["username"]

    # GitHub Profile API
    profile_url = f"https://api.github.com/users/{username}"
    response = requests.get(profile_url)

    if response.status_code != 200:
        return render_template("error.html")

    data = response.json()

    # GitHub Repositories API
    repo_url = f"https://api.github.com/users/{username}/repos"
    repo_response = requests.get(repo_url)
    repositories = repo_response.json()

    # Find Top Repository
    top_repo = None
    max_stars = -1

    # Count Total Stars
    total_stars = 0

    for repo in repositories:

        total_stars += repo["stargazers_count"]

        if repo["stargazers_count"] > max_stars:
            max_stars = repo["stargazers_count"]
            top_repo = repo

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
        total_stars=total_stars
    )


if __name__ == "__main__":
    app.run(debug=True)