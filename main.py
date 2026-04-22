import requests
from bs4 import BeautifulSoup
import time
import random
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Bot

# ====== CONFIG ======
ASIN = "B0FZK3L04D"
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# ====== SERVER ======
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    server = HTTPServer(("0.0.0.0", 10000), Handler)
    server.serve_forever()

# ====== SCRAPER ======
def get_price():
    print("🌐 fetching amazon...")

    url = f"https://www.amazon.de/dp/{ASIN}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    price = soup.select_one("span.a-price span.a-offscreen")

    if price:
        price_text = price.text.strip()
        print("💰 FOUND PRICE:", price_text)
        return price_text
    else:
        print("❌ price not found")
        return None

# ====== TELEGRAM ======
def send_alert(msg):
    print("📩 sending telegram...")
    bot.send_message(chat_id=CHAT_ID, text=msg)

# ====== LOOP ======
def run_bot():
    last_price = None

    while True:
        try:
            print("🔄 checking price...")
            price = get_price()

            if price and (last_price is None or price != last_price):
                print("🔥 price changed!")
                send_alert(f"🔥 السعر: {price}")
                last_price = price

            time.sleep(random.randint(30, 60))

        except Exception as e:
            print("❌ ERROR:", e)
            time.sleep(60)

# ====== RUN ======
threading.Thread(target=run_server, daemon=True).start()
threading.Thread(target=run_bot, daemon=True).start()

while True:
    time.sleep(1000)
