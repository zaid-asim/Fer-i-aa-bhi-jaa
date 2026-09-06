import urllib.request
import urllib.parse
import re

url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote("Parle-G Gold Biscuits amazon india")
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print("Length:", len(html))
        # Find links
        links = re.findall(r'href="([^"]+)"', html)
        print("Found links:", len(links))
        for l in links[:10]:
            print("Link:", l)
except Exception as e:
    print("Error:", e)
