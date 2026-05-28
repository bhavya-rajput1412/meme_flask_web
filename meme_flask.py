import requests, random
from flask import Flask, render_template

app = Flask(__name__)

def get_memes():
    url = "https://www.reddit.com/r/memes/top.json?limit=100"
    headers = {"User-agent": "meme-site/1.0"}
    response = requests.get(url, headers=headers)
    data = response.json()

    memes = []
    for post in data["data"]["children"]:
        post_data = post["data"]
        # only include image posts
        if post_data.get("url", "").endswith((".jpg", ".jpeg", ".png", ".gif")):
            memes.append({
                "title": post_data["title"],
                "url": post_data["url"],
                "upvotes": post_data["ups"],
                "author": post_data["author"],
                "link": f"https://reddit.com{post_data['permalink']}"
            })

    return random.sample(memes, k=min(12, len(memes)))


@app.route("/")
def index():
    memes = get_memes()
    return render_template("index.html", memes=memes)


if __name__ == "__main__":
    app.run(debug=True)