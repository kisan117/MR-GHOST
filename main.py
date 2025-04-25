from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time, json, threading
from datetime import datetime

app = Flask(__name__)

# ---- Facebook credentials ----
FB_EMAIL = "your_email_here"
FB_PASSWORD = "your_password_here"

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def load_token():
    config = load_config()
    return config.get("token")

def get_signature():
    config = load_config()
    return config.get("signature", "")

def load_times():
    with open("times.json", "r") as f:
        return json.load(f).get("schedule", [])

def load_comments():
    with open("comments.json", "r") as f:
        return json.load(f)

def post_facebook_comment(post_url, comment_text):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.facebook.com/login")
    time.sleep(3)

    try:
        driver.find_element(By.ID, "email").send_keys(FB_EMAIL)
        driver.find_element(By.ID, "pass").send_keys(FB_PASSWORD)
        driver.find_element(By.NAME, "login").click()
        time.sleep(5)

        driver.get(post_url)
        time.sleep(5)

        comment_area = driver.find_element(By.XPATH, "//div[@aria-label='Write a comment']")
        comment_area.click()
        time.sleep(1)
        signature = get_signature()
        comment_area.send_keys(comment_text + signature)
        time.sleep(1)
        comment_area.send_keys("\n")
        time.sleep(3)

        driver.quit()
        print(f"[{datetime.now()}] Comment posted to {post_url}")
        return True, "Comment posted"
    except Exception as e:
        driver.quit()
        print(f"[{datetime.now()}] Failed to comment: {e}")
        return False, str(e)

def scheduler_loop():
    posted_today = set()
    while True:
        token = load_token()
        times = load_times()
        comments = load_comments()
        now = datetime.now().strftime("%H:%M")

        if now in times:
            for item in comments:
                task_id = f"{item['url']}_{now}"
                if task_id not in posted_today:
                    post_facebook_comment(item["url"], item["comment"])
                    posted_today.add(task_id)
        time.sleep(60)

@app.route('/run', methods=['POST'])
def manual_run():
    data = request.json
    token_input = data.get("token")
    saved_token = load_token()

    if token_input != saved_token:
        return jsonify({"success": False, "message": "Invalid token"}), 403

    comments = load_comments()
    results = []
    for task in comments:
        success, msg = post_facebook_comment(task["url"], task["comment"])
        results.append({
            "url": task["url"],
            "comment": task["comment"],
            "success": success,
            "message": msg
        })
    return jsonify(results)

if __name__ == '__main__':
    print("\n=====================================")
    print("     Facebook Auto Comment Bot")
    print("     Created by: Mr. Devil")
    print("=====================================\n")
    threading.Thread(target=scheduler_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True)
