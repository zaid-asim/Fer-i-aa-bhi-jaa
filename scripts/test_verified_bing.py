import urllib.request
import urllib.parse
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

def fetch_top_image(query):
    try:
        url = "https://www.bing.com/images/search?q=" + urllib.parse.quote(query) + "&first=1"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
            for m in matches:
                # Test if URL actually returns 200
                try:
                    head_req = urllib.request.Request(m, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(head_req, timeout=3) as img_resp:
                        if img_resp.status == 200:
                            return m
                except:
                    continue
    except Exception as e:
        return f"Error: {e}"
    return None

test_list = [
    "Parle-G Gold Biscuits packet",
    "Amul Butter 500g pack",
    "Coca Cola bottle 750ml",
    "Maggi Masala 2-Minute Noodles packet",
    "Surf Excel Easy Wash detergent powder pack",
    "Tata Salt 1kg packet",
    "Britannia Good Day Cashew packet",
    "Lays Magic Masala packet India",
    "Dettol Original Soap pack",
    "Dove Cream Beauty Bar pack"
]

for item in test_list:
    img = fetch_top_image(item)
    print(f"{item} => {img}", flush=True)
