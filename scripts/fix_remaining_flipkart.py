import os
import re
import urllib.request
import urllib.parse
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

OUT_DIR = "images/products"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-IN,en;q=0.9'
}

ITEMS_TO_FIX = [
    ("p26", "Mountain Dew 750ml"),
    ("p44", "Vim Gel Lemon Dishwash 750ml"),
    ("p57", "Bingo Mad Angles Achaari Masti"),
    ("p58", "Yippee Magic Masala Noodles"),
    ("p85", "Mother Dairy Dahi 400g")
]

for pid, query in ITEMS_TO_FIX:
    out_file = f"{OUT_DIR}/{pid}.jpg"
    url = f"https://www.flipkart.com/search?q={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            imgs = re.findall(r'https://rukminim\d*\.flixcart\.com/image/[^"\'\s<>\\]+', html)
            if imgs:
                chosen_url = re.sub(r'/image/\d+/\d+/', '/image/832/832/', imgs[0])
                img_req = urllib.request.Request(chosen_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(img_req, timeout=8) as img_resp:
                    content = img_resp.read()
                    if len(content) > 5000:
                        with open(out_file, 'wb') as f:
                            f.write(content)
                        print(f"[{pid}] FIXED: {query} ({len(content)} bytes)")
    except Exception as e:
        print(f"[{pid}] ERROR: {e}")

print("Fixed batch complete!")
