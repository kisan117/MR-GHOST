import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# CONFIG
EMAIL = "your_email@example.com"
PASSWORD = "your_password"
HEADLESS = False
COMMENT_LIST = [
    "Great post!", "Awesome!", "Loved this!", "Interesting perspective!", "Thanks for sharing!"
]
POST_FILE = "post_urls.txt"
WAIT_TIME_RANGE = (5, 10)  # random wait between actions

def get_post_urls(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]

def init_browser(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)

def login(driver, email, password):
    driver.get("https://www.facebook.com")
    time.sleep(random.randint(*WAIT_TIME_RANGE))
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.NAME, "login").click()
    time.sleep(random.randint(*WAIT_TIME_RANGE))

def comment_on_post(driver, url, comment_text):
    try:
        driver.get(url)
        time.sleep(random.randint(*WAIT_TIME_RANGE))
        comment_box = driver.find_element(By.XPATH, "//div[@aria-label='Write a comment']")
        comment_box.click()
        time.sleep(1)
        comment_box.send_keys(comment_text)
        time.sleep(1)
        comment_box.send_keys(Keys.RETURN)
        print(f"[+] Comment posted on: {url}")
    except Exception as e:
        print(f"[!] Failed to comment on: {url}
    {e}")

def main():
    driver = init_browser(HEADLESS)
    login(driver, EMAIL, PASSWORD)
    post_urls = get_post_urls(POST_FILE)

    for url in post_urls:
        comment = random.choice(COMMENT_LIST)
        comment_on_post(driver, url, comment)
        time.sleep(random.randint(*WAIT_TIME_RANGE))

    driver.quit()

if __name__ == "__main__":
    main()
