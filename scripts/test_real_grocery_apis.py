import urllib.request
import urllib.parse
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Test 1: BigBasket internal search API
def test_bb_search(query):
    try:
        url = f"https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            tabs = data.get('tabs', [])
            for tab in tabs:
                product_info = tab.get('product_info', {})
                products = product_info.get('products', [])
                if products:
                    p = products[0]
                    # Check images
                    images = p.get('images', [])
                    desc = p.get('p_desc', '')
                    brand = p.get('p_brand_name', '')
                    img_url = images[0].get('l') if images else None
                    return f"SUCCESS: {brand} - {desc} => {img_url}"
    except Exception as e:
        return f"Error: {e}"
    return "No products found"

# Test 2: JioMart search API
def test_jiomart_search(query):
    try:
        url = f"https://www.jiomart.com/catalogsearch/result?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=6) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            import re
            m = re.findall(r'https://www\.jiomart\.com/images/product/original/[^"\'\s<>]+\.(?:jpg|png|jpeg)', html)
            if m:
                return f"SUCCESS JIOMART: {m[0]}"
    except Exception as e:
        return f"JioMart Error: {e}"
    return "JioMart not found"

queries = ["Parle-G Gold", "Britannia Good Day", "Surf Excel Easy Wash", "Vim Dishwash Gel", "Maggi 2-Minute", "Coca Cola 750ml"]

for q in queries:
    print("BB:", q, "=>", test_bb_search(q))
    print("JM:", q, "=>", test_jiomart_search(q))
