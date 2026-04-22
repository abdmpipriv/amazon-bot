import requests
import re

def get_price():
    print("🌐 Fetching Amazon JSON...", flush=True)

    url = f"https://www.amazon.de/gp/product/{ASIN}?th=1&psc=1"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "de-DE,de;q=0.9,en;q=0.8"
    }

    r = requests.get(url, headers=headers)
    html = r.text

    # 🔥 استخراج السعر من JSON embedded
    patterns = [
        r'"priceToPay"\s*:\s*\{"amount"\s*:\s*([\d\.]+)',
        r'"price"\s*:\s*"([\d\,\.]+)"',
        r'€\s?([\d\.,]+)'
    ]

    for p in patterns:
        m = re.search(p, html)
        if m:
            price = m.group(1)
            print("💰 FOUND PRICE:", price, flush=True)
            return price

    print("❌ price not found", flush=True)
    return None
