import urllib.request
import json

try:
    url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms=Parle-G&search_simple=1&action=process&json=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode('utf-8'))
        products = data.get('products', [])
        print("Found products:", len(products))
        if products:
            print("Image URL:", products[0].get('image_front_url') or products[0].get('image_url'))
except Exception as e:
    print("Error:", e)
