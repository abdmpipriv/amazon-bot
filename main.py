def get_price():
    print("🌐 Fetching Amazon...", flush=True)

    url = f"https://www.amazon.de/dp/{ASIN}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml",
        "Connection": "keep-alive"
    }

    response = requests.get(url, headers=headers)

    print("STATUS:", response.status_code, flush=True)

    html = response.text

    # 🔥 fallback parsing
    import re

    match = re.search(r'"priceToPay"\s*:\s*\{"amount"\s*:\s*([\d\.]+)', html)

    if match:
        price = match.group(1)
        print("💰 FOUND PRICE:", price, flush=True)
        return price

    print("❌ price not found", flush=True)
    return None
