import urllib.request
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.bigbasket.com/pd/40081603/tata-salt-vacuum-evaporated-iodised-salt-1-kg/"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        imgs = re.findall(r'https://www\.bbassets\.com/media/uploads/p/l/[^"\'\s]+', html)
        print("Found bbassets images:", len(imgs))
        for img in set(imgs):
            print("IMG:", img)
except Exception as e:
    print("Error:", e)
