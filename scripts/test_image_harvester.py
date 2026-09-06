import urllib.request
import urllib.parse
import ssl
import json
import re
import time

ssl._create_default_https_context = ssl._create_unverified_context

def check_image_url(url):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=4) as resp:
            if resp.status == 200:
                ct = resp.headers.get('Content-Type', '').lower()
                length = int(resp.headers.get('Content-Length', 0))
                if 'image' in ct or any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                    return True
    except:
        pass
    return False

BAD_WORDS = ['wallpaper', 'hotel', 'car', 'vehicle', 'diagram', 'anatomy', 'meme', 'desktop', 'screenshot', 'hand-worksheet', 'portrait', 'tata_tiago']

def find_verified_image(brand, name):
    # Try query variants
    queries = [
        f'"{brand}" "{name}" product packaging white background',
        f'"{name}" packaging packet',
        f'{brand} {name} bigbasket packaging'
    ]
    for q in queries:
        try:
            url = "https://www.bing.com/images/search?q=" + urllib.parse.quote(q) + "&first=1"
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=5) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
                if not matches:
                    matches = re.findall(r'"murl":"(http[^"]+)"', html)
                
                # Check candidate matches
                for m in matches:
                    m_low = m.lower()
                    if any(bad in m_low for bad in BAD_WORDS):
                        continue
                    if any(ext in m_low for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                        if check_image_url(m):
                            return m
        except Exception as e:
            pass
        time.sleep(0.5)
    return None

test_items = [
    ("Parle", "Parle-G Gold Biscuits"),
    ("Britannia", "Good Day Butter Cookies"),
    ("Amul", "Amul Butter"),
    ("Nestle", "Maggi 2-Minute Masala Noodles"),
    ("Coca-Cola", "Coca-Cola Original Taste")
]

for b, n in test_items:
    img = find_verified_image(b, n)
    print(f"{b} - {n} => {img}", flush=True)
