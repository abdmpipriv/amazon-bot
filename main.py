import requests
from bs4 import BeautifulSoup
import time
import random
import os
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
    PORT = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"🌐 Server running on port {PORT}", flush=True)

    # نخلي السيرفر يعمل بدون ما يوقف البوت
    import threading
    threading.Thread(target=server.serve_forever, daemon=True).start()

# ====== SCRAPER ======
def get_price():
    print("🌐 Fetching Amazon...", flush=True)

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
        print("💰 FOUND PRICE:", price_text, flush=True)
        return price_text
    else:
        print("❌ price not found", flush=True)
        return None

# ====== TELEGRAM ======
def send_alert(msg):
    print("📩 Sending Telegram...", flush=True)
    bot.send_message(chat_id=CHAT_ID, text=msg)

# ====== MAIN LOOP ======
def run_bot():
    print("🚀 Bot started!", flush=True)

    last_price = None

    while True:
        try:
            print("🔄 Checking price...", flush=True)

            price = get_price()

            if price and (last_price is None or price != last_price):
                print("🔥 Price changed!", flush=True)
                send_alert(f"🔥 السعر: {price}")
                last_price = price

            time.sleep(30)

        except Exception as e:
            print("❌ ERROR:", e, flush=True)
            time.sleep(60)

# ====== RUN ======
run_server()
run_bot()
