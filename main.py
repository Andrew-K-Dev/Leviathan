from flask import Flask, jsonify
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

@app.route('/')
def home():
    return "Leviathan is scanning for arbitrage deals..."

@app.route('/api/leads', methods=['GET'])
def get_leads():
    leads = [
        {
            "email": "leadone@example.com",
            "product": "Dewalt Drill",
            "timestamp": "2025-07-29 22:35"
        },
        {
            "email": "leadtwo@example.com",
            "product": "Milwaukee Saw",
            "timestamp": "2025-07-29 22:36"
        }
    ]
    return jsonify(leads)


# === Arbitrage Scanner Logic ===

def scan_craigslist():
    print("🔍 Scanning Craigslist for deals...")
    url = "https://geo.craigslist.org/iso/us"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.content, "html.parser")
        links = soup.find_all("a")
        deals = []
        for link in links:
            text = link.get_text().lower()
            if "dewalt" in text or "milwaukee" in text:
                deals.append(link.get("href"))
        print(f"✅ Found {len(deals)} potential flips.")
        if deals:
            summarize_and_alert(deals)
    except Exception as e:
        print("❌ Error during scan:", e)

def summarize_and_alert(deals):
    prompt = "Analyze the following Craigslist items and tell me if they are good resale opportunities:\n\n" + "\n".join(deals[:5])
    try:
        summary = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        message = summary['choices'][0]['message']['content']
        print("💡 GPT Profit Summary:", message)
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
