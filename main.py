from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Function to post a single comment using Graph API
def post_page_comment(post_id, comment_text, page_access_token):
    url = f"https://graph.facebook.com/{post_id}/comments"
    params = {
        "message": comment_text,
        "access_token": page_access_token
    }
    response = requests.post(url, params=params)

    if response.status_code == 200:
        return f"Comment '{comment_text}' posted successfully."
    else:
        return f"Failed: {response.json()}"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    post_id = request.form.get("post_id")
    comments = request.form.get("comments")
    token = request.form.get("token")

    if not post_id or not comments or not token:
        return render_template("index.html", result="Missing data. Please fill in all fields.")

    # Split the comments by newline and remove any extra spaces
    comment_list = [comment.strip() for comment in comments.split("\n") if comment.strip()]

    results = []
    for comment in comment_list:
        result = post_page_comment(post_id, comment, token)
        results.append(result)

    # Combine all results into a single response
    return render_template("index.html", result="<br>".join(results))

if __name__ == "__main__":
    app.run(debug=True)
