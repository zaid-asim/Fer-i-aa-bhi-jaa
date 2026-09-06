import urllib.request
import urllib.parse
import ssl
import json
import re
import time

ssl._create_default_https_context = ssl._create_unverified_context

def check_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                length = int(resp.headers.get('Content-Length', 0))
                return True, length
    except:
        pass
    return False, 0

# Test the known verified ones
known_urls = {
    "Amul Butter": "https://www.bbassets.com/media/uploads/p/l/104864_8-amul-butter-pasteurised.jpg",
    "Tata Salt": "https://www.bbassets.com/media/uploads/p/l/40081603_6-tata-salt-salt-iodized.jpg",
    "Parle-G Gold": "https://images-cdn.ubuy.co.in/633af64dba25b806c73693ea-parle-g-gold-biscuits-1-kg-10-pack-of.jpg",
    "Parle Marie": "https://www.bbassets.com/media/uploads/p/l/40204957_3-parle-parle-marie.jpg",
    "Britannia Marie Gold": "https://images.openfoodfacts.org/images/products/890/106/316/2914/front_en.3.400.jpg",
    "Coca-Cola Original": "https://images.openfoodfacts.org/images/products/544/900/005/4227/front_en.563.400.jpg",
    "Kurkure Masala Munch": "https://images.openfoodfacts.org/images/products/890/149/136/1026/front_en.51.400.jpg",
    "Maggi 2-Minute Noodles": "https://assets.hyperpure.com/data/images/products/cdbb5abf71acf8ac95d399d630364e73.png",
    "Dove Beauty Bar": "https://assets.unileversolutions.com/v1/62941798.jpg"
}

for name, u in known_urls.items():
    ok, l = check_url(u)
    print(f"{name}: {'OK' if ok else 'FAIL'} ({l} bytes)", flush=True)
