import urllib.request
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.bigbasket.com/ps/?q=Parle-G"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
})
try:
    with urllib.request.urlopen(req, timeout=8) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        imgs = re.findall(r'https://www\.bbassets\.com/media/uploads/p/l/[^"\'\s]+', html)
        print("Found bbassets images on search page:", len(imgs))
        for img in set(imgs)[:5]:
            print("IMG:", img)
except Exception as e:
    print("Error:", e)
