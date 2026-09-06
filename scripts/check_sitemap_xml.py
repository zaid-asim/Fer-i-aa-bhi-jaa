import urllib.request
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.bigbasket.com/sitemap.xml"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print("Sitemap length:", len(content))
        locs = re.findall(r'<loc>(.*?)</loc>', content)
        print("Found locs:", len(locs))
        for l in locs[:10]:
            print(l)
except Exception as e:
    print("Error:", e)
