import urllib.request
import urllib.parse
import re

def get_bing_image(query):
    try:
        url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&first=1"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        })
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
            if not matches:
                matches = re.findall(r'"murl":"(http[^"]+)"', html)
            # Filter for jpg, jpeg, png, webp and avoid wallpaper sites
            for m in matches:
                if any(ext in m.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']) and 'wallpaper' not in m.lower():
                    return m
            if matches:
                return matches[0]
    except Exception as e:
        return f"Error: {e}"
    return None

test_queries = [
    "Parle-G Gold Biscuits amazon india product",
    "Amul Butter 500g amazon india product",
    "Coca Cola bottle 750ml amazon india product",
    "Surf Excel Easy Wash detergent amazon india product",
    "Britannia Good Day Cashew amazon india product",
    "Maggi 2-Minute Noodles amazon india product",
    "Tata Tea Premium amazon india product",
    "Lays Magic Masala amazon india product",
    "Kurkure Masala Munch amazon india product",
    "Dabur Red Paste amazon india product"
]

for q in test_queries:
    print(q, "->", get_bing_image(q))
