import urllib.request
import urllib.parse
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context

def search_openfoodfacts(query):
    try:
        url = f"https://in.openfoodfacts.org/cgi/search.pl?search_terms={urllib.parse.quote(query)}&search_simple=1&action=process&json=1&page_size=3"
        req = urllib.request.Request(url, headers={'User-Agent': 'FeriCatalog/1.0 (contact@feri.in)'})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            products = data.get('products', [])
            for p in products:
                img = p.get('image_front_url') or p.get('image_url')
                name = p.get('product_name') or p.get('product_name_en')
                if img and name:
                    return f"{name} => {img}"
    except Exception as e:
        return f"Error: {e}"
    return "Not found"

queries = [
    "Parle-G",
    "Britannia Good Day",
    "Britannia Marie Gold",
    "Britannia Bourbon",
    "Amul Butter",
    "Amul Milk",
    "Amul Cheese",
    "Maggi Masala Noodles",
    "Nescafe Classic",
    "KitKat",
    "Lay's Magic Masala",
    "Kurkure Masala Munch",
    "Tata Salt",
    "Red Label Tea",
    "Dabur Honey",
    "Aashirvaad Atta",
    "Surf Excel",
    "Vim",
    "Dettol"
]

for q in queries:
    res = search_openfoodfacts(q)
    print(f"OFF: {q} => {res}", flush=True)
