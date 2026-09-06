import urllib.request
import urllib.parse
import json

queries = [
    "Parle-G",
    "Britannia Good Day",
    "Amul Butter",
    "Maggi Noodles",
    "Coca Cola",
    "Haldiram Bhujia",
    "Tata Salt",
    "Lays",
    "Kurkure",
    "Dettol Soap",
    "Colgate Toothpaste",
    "Dove Soap",
    "Surf Excel",
    "Harpic"
]

for q in queries:
    try:
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={urllib.parse.quote(q)}&search_simple=1&action=process&json=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'FeriApp/1.0 (contact@feri.in)'})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode('utf-8'))
            products = data.get('products', [])
            img = None
            for p in products:
                img = p.get('image_front_url') or p.get('image_url')
                if img:
                    break
            print(f"{q}: {img}")
    except Exception as e:
        print(f"{q}: Error {e}")
