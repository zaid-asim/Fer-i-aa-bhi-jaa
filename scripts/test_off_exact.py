import urllib.request
import urllib.parse
import json
import time

def search_off_exact(brand, product):
    try:
        query = f"{brand} {product}"
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={urllib.parse.quote(query)}&search_simple=1&action=process&json=1&page_size=5&fields=product_name,brands,image_front_small_url,image_front_url,image_url"
        req = urllib.request.Request(url, headers={'User-Agent': 'FeriECommerceApp - Android/Web - Version 1.0 (info@feriapp.in)'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for p in data.get('products', []):
                img = p.get('image_front_url') or p.get('image_front_small_url') or p.get('image_url')
                if img:
                    return img, p.get('product_name')
    except Exception as e:
        return None, str(e)
    return None, "Not found"

items = [
    ("Parle", "Parle-G"),
    ("Britannia", "Good Day"),
    ("Britannia", "Marie Gold"),
    ("Amul", "Butter"),
    ("Amul", "Cheese"),
    ("Amul", "Milk"),
    ("Nestle", "Maggi"),
    ("Coca-Cola", "Coca-Cola"),
    ("PepsiCo", "Lay's"),
    ("PepsiCo", "Kurkure"),
    ("Tata", "Salt"),
    ("Tata", "Tea"),
    ("Haldiram's", "Bhujia"),
    ("ITC", "Aashirvaad Atta")
]

for b, p in items:
    img, name = search_off_exact(b, p)
    print(f"{b} - {p} -> {name}: {img}")
    time.sleep(1)
