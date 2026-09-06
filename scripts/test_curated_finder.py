import urllib.request
import urllib.parse
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

TRUSTED_DOMAINS = [
    'bbassets.com',
    'bigbasket.com',
    'hyperpure.com',
    'unileversolutions.com',
    'ubuy.co.in',
    'imimg.com',
    'jiomart.com',
    'grofers.com',
    'blinkit.com',
    'media-amazon.com',
    'walmartimages.com',
    'openfoodfacts.org'
]

def find_verified_packshot(brand, product):
    query = f'"{brand}" "{product}" packaging'
    try:
        url = "https://www.bing.com/images/search?q=" + urllib.parse.quote(query) + "&first=1"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=6) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
            if not matches:
                matches = re.findall(r'"murl":"(http[^"]+)"', html)
            
            # Step 1: Prioritize trusted grocery CDNs
            for m in matches:
                m_low = m.lower()
                if any(td in m_low for td in TRUSTED_DOMAINS):
                    # Verify HTTP 200
                    try:
                        t_req = urllib.request.Request(m, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(t_req, timeout=3) as r:
                            if r.status == 200:
                                return m, "trusted"
                    except:
                        pass
            
            # Step 2: Fallback to any clean product image
            for m in matches:
                m_low = m.lower()
                if any(ext in m_low for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                    if not any(bad in m_low for bad in ['wallpaper', 'car', 'hotel', 'portrait', 'meme', 'actor', 'vector', 'silhouette']):
                        try:
                            t_req = urllib.request.Request(m, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(t_req, timeout=3) as r:
                                if r.status == 200:
                                    return m, "fallback"
                        except:
                            pass
    except Exception as e:
        return None, str(e)
    return None, "none"

test_items = [
    ("Parle", "Parle-G Gold"),
    ("Britannia", "Good Day Cashew"),
    ("Amul", "Butter"),
    ("Coca-Cola", "Coca-Cola Original"),
    ("PepsiCo", "Lay's Magic Masala"),
    ("PepsiCo", "Kurkure Masala Munch"),
    ("Nestle", "Maggi 2-Minute Noodles"),
    ("HUL", "Surf Excel Easy Wash"),
    ("HUL", "Dove Cream Beauty"),
    ("Tata", "Tata Salt")
]

for b, p in test_items:
    url, src = find_verified_packshot(b, p)
    print(f"[{src}] {b} {p} => {url}")
