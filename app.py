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
        return "GitHub user not found"


    data = response.json()



    # GitHub Repository API
    repo_url = f"https://api.github.com/users/{username}/repos"

    repo_response = requests.get(repo_url)

    repositories = repo_response.json()



    # Analytics variables

    top_repo = None

    max_stars = -1

    total_stars = 0

    languages = {}



    # Analyze repositories

    for repo in repositories:


        # Total stars

        total_stars += repo["stargazers_count"]



        # Language count

        language = repo["language"]


        if language:

            if language in languages:

                languages[language] += 1

            else:

                languages[language] = 1



        # Top repository

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


        total_stars=total_stars,


        languages=languages

    )



if __name__ == "__main__":

    app.run(debug=True)