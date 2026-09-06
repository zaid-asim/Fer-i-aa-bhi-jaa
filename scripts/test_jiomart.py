import urllib.request
import urllib.parse
import ssl
import json
import re

ssl._create_default_https_context = ssl._create_unverified_context

def search_jiomart(query):
    url = f"https://www.jiomart.com/catalogsearch/result?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    })
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Look for product images
            # JioMart images usually start with https://www.jiomart.com/images/product/original/ or /original/
            imgs = re.findall(r'https://www\.jiomart\.com/images/product/[^"\'\s]+\.jpg', html)
            print(f"JioMart '{query}' found {len(imgs)} images:")
            for img in set(imgs[:3]):
                print("  ", img)
    except Exception as e:
        print(f"JioMart '{query}' error: {e}")

search_jiomart("Parle G")
search_jiomart("Surf Excel")
search_jiomart("Amul Butter")
search_jiomart("Maggi")
