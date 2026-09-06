import urllib.request
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.bigbasket.com/ps/?q=Parle-G"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
try:
    with urllib.request.urlopen(req, timeout=8) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        imgs = re.findall(r'https://[^"\'\s]+bbassets\.com[^"\'\s]+', html)
        print("All bbassets links:", len(imgs))
        for img in list(set(imgs))[:10]:
            print("IMG:", img)
        # Also check product links
        pds = re.findall(r'/pd/\d+/[^"\'\s]+', html)
        print("Found product links:", len(pds))
        for p in list(set(pds))[:5]:
            print("PD:", p)
except Exception as e:
    print("Error:", e)
