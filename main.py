import asyncio
import time
import random
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from playwright.async_api import async_playwright
from telegram import Bot

# ====== CONFIG ======
ASIN = "B0FZK3L04D"
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# ====== FAKE SERVER ======
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    server = HTTPServer(("0.0.0.0", 10000), Handler)
    server.serve_forever()

# ====== SCRAPER ======
async def get_price():
    print("🌐 opening amazon...")
    url = f"https://www.amazon.de/dp/{ASIN}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )

        page = await browser.new_page()
        await page.set_extra_http_headers({"User-Agent": "Mozilla/5.0"})

        await page.goto(url, timeout=60000)
        await page.wait_for_selector("span.a-price", timeout=10000)

        price = await page.locator("span.a-price").first.inner_text()

        print("💰 FOUND PRICE:", price)

        await browser.close()
        return price

async def send_alert(msg):
    print("📩 sending telegram...")
    await bot.send_message(chat_id=CHAT_ID, text=msg)

# ====== LOOP ======
def run_bot():
    last_price = None

    while True:
        try:
            print("🔄 checking price...")
            price = asyncio.run(get_price())

            if last_price is None or price != last_price:
                print("🔥 price changed!")
                asyncio.run(send_alert(f"🔥 السعر: {price}"))
                last_price = price

            time.sleep(random.randint(30, 60))

        except Exception as e:
            print("❌ ERROR:", e)
            time.sleep(60)

# ====== RUN ======
threading.Thread(target=run_server, daemon=True).start()
threading.Thread(target=run_bot, daemon=True).start()

# خليه يضل شغال
while True:
    time.sleep(1000)
