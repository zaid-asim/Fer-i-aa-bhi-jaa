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
            print("Next.js keys:", list(data.keys()))
            props = data.get('props', {}).get('pageProps', {})
            print("pageProps keys:", list(props.keys()))
            # find any images in the json string
            raw_json = json.dumps(data)
            imgs = re.findall(r'https://www\.bbassets\.com/media/uploads/p/[^"\'\s]+', raw_json)
            print("Found product images in NEXT_DATA:", len(imgs))
            for img in list(set(imgs))[:5]:
                print("IMG:", img)
        else:
            print("No NEXT_DATA found")
except Exception as e:
    print("Error:", e)
