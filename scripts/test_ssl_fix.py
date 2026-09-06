import urllib.request
import urllib.parse
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.bing.com/images/search?q=" + urllib.parse.quote("Parle-G Gold Biscuits packet") + "&first=1"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
        print("Success! Found image matches:", len(matches))
        for m in matches[:5]:
            print(m)
except Exception as e:
    print("Error:", e)
