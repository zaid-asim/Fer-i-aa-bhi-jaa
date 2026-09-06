import urllib.request
import urllib.parse
import ssl
import json
import re

ssl._create_default_https_context = ssl._create_unverified_context

def test_flipkart(query):
    url = f"https://www.flipkart.com/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9'
    })
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Look for rukminim images
            imgs = re.findall(r'https://rukminim\d*\.flixcart\.com/image/[^"\'\s<>]+', html)
            print(f"Flipkart '{query}' found {len(imgs)} images:")
            for img in set(imgs[:3]):
                print("  ", img)
    except Exception as e:
        print(f"Flipkart '{query}' error: {e}")

test_flipkart("Parle-G Gold Biscuits")
test_flipkart("Surf Excel Quick Wash")
test_flipkart("Amul Butter 500g")
test_flipkart("Maggi 2-Minute Masala Noodles")
