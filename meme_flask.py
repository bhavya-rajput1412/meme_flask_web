import requests, random, os
from flask import Flask, render_template

app = Flask(__name__)

def get_memes():
    subreddits = ["IndianDankMemes", "dankindianmemes", "bollywoodmemes"]
    subreddit = random.choice(subreddits)
    url = f"https://meme-api.com/gimme/{subreddit}/50"
    headers = {"User-agent": "meme-site/1.0"}
    response = requests.get(url, headers=headers)
    data = response.json()

    memes = []
    for post in data["memes"]:
        if not post.get("nsfw", False):
            memes.append({
                "title": post["title"],
                "url": post["url"],
                "upvotes": post["ups"],
                "author": post["author"],
                "link": post["postLink"]
            })

    return random.sample(memes, min(12, len(memes)))


@app.route("/")
def index():
    memes = get_memes()
    return render_template("index.html", memes=memes)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)  