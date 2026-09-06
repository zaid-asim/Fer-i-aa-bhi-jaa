import urllib.request
import urllib.parse
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

def test_bing_product(brand, product, extra):
    query = f'"{brand}" "{product}" {extra}'
    url = "https://www.bing.com/images/search?q=" + urllib.parse.quote(query) + "&first=1"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
            for m in matches[:5]:
                m_low = m.lower()
                # filter out obvious bad ones
                if not any(bad in m_low for bad in ['car', 'wallpaper', 'hotel', 'portrait', 'meme']):
                    if any(ext in m_low for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                        return m
    except Exception as e:
        return f"Error: {e}"
    return "None"

items = [
    ("Surf Excel", "Easy Wash", "detergent powder packet"),
    ("Vim", "Dishwash Gel", "lemon bottle"),
    ("Parachute", "100% Pure Coconut Oil", "blue bottle"),
    ("Aashirvaad", "Superior MP Atta", "atta packet"),
    ("Britannia", "Good Day Cashew", "biscuit packet"),
    ("Sprite", "Clear Lime", "soft drink green bottle"),
    ("Thums Up", "Toofani", "cola bottle"),
    ("Fanta", "Orange", "soda bottle"),
    ("Red Label", "Tea", "chai box"),
    ("Dettol", "Liquid Handwash", "pump bottle")
]

for b, p, ex in items:
    res = test_bing_product(b, p, ex)
    print(f"{b} {p} => {res}", flush=True)
