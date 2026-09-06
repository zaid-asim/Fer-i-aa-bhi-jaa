import urllib.request
import urllib.parse
import ssl
import json
import re

ssl._create_default_https_context = ssl._create_unverified_context

def search_ddg_image(query):
    try:
        # Step 1: get vqd token
        url = "https://duckduckgo.com/?q=" + urllib.parse.quote(query)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            m = re.search(r'vqd=([0-9-]+)&', html) or re.search(r'vqd="([0-9-]+)"', html)
            if not m:
                return "No vqd token"
            vqd = m.group(1)
        
        # Step 2: query i.js
        img_url = f"https://duckduckgo.com/i.js?q={urllib.parse.quote(query)}&o=json&p=1&s=0&u=bing&f=,,,&l=in-en&vqd={vqd}"
        req2 = urllib.request.Request(img_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': 'https://duckduckgo.com/'
        })
        with urllib.request.urlopen(req2, timeout=5) as resp2:
            data = json.loads(resp2.read().decode('utf-8'))
            results = data.get('results', [])
            for r in results:
                u = r.get('image')
                if u and any(u.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                    return u
    except Exception as e:
        return f"Error: {e}"
    return "Not found"

test_queries = [
    "Surf Excel Easy Wash 2kg packet",
    "Vim Dishwash Gel 750ml bottle",
    "Parachute Coconut Oil 600ml bottle",
    "Aashirvaad Atta 10kg packet",
    "Good Day Butter Cookies Britannia",
    "Tata Tea Gold 250g packet"
]

for q in test_queries:
    res = search_ddg_image(q)
    print(f"{q} => {res}")
