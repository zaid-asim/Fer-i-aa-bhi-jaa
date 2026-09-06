import urllib.request
import urllib.parse
import re

def get_bb_image(query):
    try:
        url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query + ' site:bbassets.com')}&first=1"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'murl&quot;:&quot;(https://www\.bbassets\.com/[^&]+)&quot;', html)
            if not matches:
                matches = re.findall(r'"murl":"(https://www\.bbassets\.com/[^"]+)"', html)
            if matches:
                return matches[0]
    except Exception as e:
        return str(e)
    return None

test_items = [
    "Parle-G",
    "Amul Butter",
    "Coca Cola",
    "Surf Excel Easy Wash",
    "Maggi 2-Minute Noodles",
    "Britannia Good Day Cashew",
    "Tata Salt",
    "Lays Magic Masala",
    "Kurkure Masala Munch",
    "Dabur Red Paste"
]

for item in test_items:
    print(item, "->", get_bb_image(item))
