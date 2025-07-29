from flask import Flask
import threading
import schedule
import time
import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return "Leviathan is scanning for arbitrage deals..."

# === Arbitrage Scanner Logic ===

def scan_craigslist():
    print("🔍 Scanning Craigslist for deals...")
    url = "https://geo.craigslist.org/iso/us"  # Can be a sub-region or product category
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.content, "html.parser")
        links = soup.find_all("a")
        deals = []
        for link in links:
            text = link.get_text().lower()
            if "dewalt" in text or "milwaukee" in text:  # Example niche
                deals.append(link.get("href"))
        print(f"✅ Found {len(deals)} potential flips.")
        if deals:
            summarize_and_alert(deals)
    except Exception as e:
        print("❌ Error during scan:", e)

def summarize_and_alert(deals):
    prompt = f"Analyze the following Craigslist items and tell me if they are good resale opportunities:\n\n" + "\n".join(deals[:5])
    try:
        summary = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        message = summary['choices'][0]['message']['content']
        print("💡 GPT Profit Summary:", message)
        # Optional: Send to Telegram or Discord here
    except Exception as e:
        print("❌ OpenAI failed:", e)

def run_scheduler():
    schedule.every(15).minutes.do(scan_craigslist)
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    thread = threading.Thread(target=run_scheduler)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    start_scheduler()
    app.run(host="0.0.0.0", port=5000)
