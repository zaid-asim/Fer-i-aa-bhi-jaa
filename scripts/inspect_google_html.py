import urllib.request
import urllib.parse
import re

url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote("Parle-G Gold Biscuits")
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})
with urllib.request.urlopen(req, timeout=5) as resp:
    html = resp.read().decode('latin1', errors='ignore')
    # Find any http or https strings that end in jpg/png/webp or contain gstatic
    all_imgs = re.findall(r'https://[^"\'\s<>]+\.(?:jpg|png|jpeg|webp)', html)
    print("Found jpg/png images:", len(all_imgs))
    for img in all_imgs[:10]:
        print("IMG:", img)
    
    gstatics = re.findall(r'https://encrypted-tbn0\.gstatic\.com/images\?q=[^"\'\s<>\\]+', html)
    print("Found gstatic:", len(gstatics))
    for g in gstatics[:5]:
        print("GSTATIC:", g)
