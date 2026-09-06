import urllib.request
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://in.openfoodfacts.org/api/v2/search?countries_tags_en=india&page_size=100&fields=code,product_name,brands,categories,image_front_url,image_url"
req = urllib.request.Request(url, headers={'User-Agent': 'FeriECommerce/1.0 (feri@store.in)'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        products = data.get('products', [])
        print("Total products fetched from OpenFoodFacts India:", len(products))
        count = 0
        for p in products:
            img = p.get('image_front_url') or p.get('image_url')
            name = p.get('product_name')
            brand = p.get('brands')
            if img and name and brand:
                count += 1
                if count <= 15:
                    print(f"[{count}] {brand} - {name}: {img}")
        print("Total valid products with images:", count)
except Exception as e:
    print("Error:", e)
