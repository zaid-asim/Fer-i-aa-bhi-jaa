import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url1 = "https://assets.hyperpure.com/data/images/products/cdbb5abf71acf8ac95d399d630364e73.png"
url2 = "https://assets.unileversolutions.com/v1/62941798.jpg"

for u in [url1, url2]:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(u, "-> Status:", resp.status, "Length:", len(resp.read()))
    except Exception as e:
        print(u, "-> Error:", e)
