from flask import Flask
import threading
import schedule
import time

app = Flask(__name__)

def background_job():
    import requests
from bs4 import BeautifulSoup

def background_job():
    print("🔁 Running background task...")

    try:
        url = "https://news.ycombinator.com/"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        headlines = soup.select(".storylink")[:5]
        for idx, headline in enumerate(headlines):
            print(f"{idx+1}. {headline.text}")
    except Exception as e:
        print("❌ Scraper error:", str(e))

    # You can place your scraping, OpenAI logic, or any automation here

def run_scheduler():
    schedule.every(10).seconds.do(background_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    thread = threading.Thread(target=run_scheduler)
    thread.daemon = True
    thread.start()

@app.route('/')
def home():
    return "✅ Leviathan is running with background tasks."

if __name__ == "__main__":
    start_scheduler()
    app.run(host="0.0.0.0", port=5000)
