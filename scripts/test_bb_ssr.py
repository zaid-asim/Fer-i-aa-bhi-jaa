import urllib.request
import ssl
import json
import re

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.bigbasket.com/ps/?q=Parle-G"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
try:
    with urllib.request.urlopen(req, timeout=8) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
        if m:
            data = json.loads(m.group(1))
            ssr = data.get('props', {}).get('pageProps', {}).get('SSRData', {})
            print("SSRData keys:", list(ssr.keys()) if isinstance(ssr, dict) else type(ssr))
            # find all image or product fields
            def find_keys(obj, path=""):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if any(term in k.lower() for term in ['image', 'product', 'item', 'sku', 'url']):
                            print(f"Found {path}.{k}: {type(v)}")
                        find_keys(v, path + "." + k)
                elif isinstance(obj, list) and obj:
                    find_keys(obj[0], path + "[0]")
            find_keys(ssr, "ssr")
except Exception as e:
    print("Error:", e)
