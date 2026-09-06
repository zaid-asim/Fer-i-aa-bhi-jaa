import urllib.request
import urllib.parse
import ssl
import json
import time

ssl._create_default_https_context = ssl._create_unverified_context

HEADERS = {'User-Agent': 'FeriGroceryApp/2.0 (demo@feri.in)'}

def search_off_robust(query):
    # Try multiple servers: in.openfoodfacts.org, world.openfoodfacts.org, in.openbeautyfacts.org, in.openproductsfacts.org
    servers = [
        "https://in.openfoodfacts.org",
        "https://world.openfoodfacts.org",
        "https://in.openbeautyfacts.org",
        "https://in.openproductsfacts.org"
    ]
    for base in servers:
        try:
            url = f"{base}/cgi/search.pl?search_terms={urllib.parse.quote(query)}&search_simple=1&action=process&json=1&page_size=3"
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                for p in data.get('products', []):
                    img = p.get('image_front_url') or p.get('image_url')
                    name = p.get('product_name') or p.get('product_name_en') or ''
                    if img:
                        return name, img
        except Exception:
            continue
    return None, None

test_items = [
    "Maggi Masala",
    "Bourbon biscuit",
    "Lay's Magic Masala",
    "Tata Salt",
    "Dabur Honey",
    "KitKat",
    "Dove soap",
    "Dettol",
    "Surf Excel",
    "Vim",
    "Harpic",
    "Clinic Plus",
    "Sunsilk",
    "Patanjali Dant Kanti",
    "Parachute coconut oil"
]

for item in test_items:
    name, img = search_off_robust(item)
    print(f"{item} => {name} : {img}", flush=True)
    time.sleep(1.2)
