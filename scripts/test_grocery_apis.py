import urllib.request
import urllib.parse
import json

def search_blinkit(query):
    try:
        url = f"https://blinkit.com/v1/search?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Blinkit success:", list(data.keys())[:5])
    except Exception as e:
        print("Blinkit error:", e)

def search_bigbasket(query):
    try:
        url = f"https://www.bigbasket.com/product/svc/mb/v1/product-deck-search/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.bigbasket.com/'
        })
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("BigBasket success:", list(data.keys())[:5])
    except Exception as e:
        print("BigBasket error:", e)

search_blinkit("Amul Butter")
search_bigbasket("Amul Butter")
