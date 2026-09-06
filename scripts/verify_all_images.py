import urllib.request
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

with open('js/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all images
img_urls = re.findall(r'"image":\s*"([^"]+)"', content)
print(f"Total product images to test: {len(img_urls)}")

tested = 0
failed = 0
for idx, url in enumerate(img_urls):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status != 200:
                print(f"Failed [{idx}]: {url} -> status {resp.status}")
                failed += 1
    except Exception as e:
        print(f"Error [{idx}]: {url} -> {e}")
        failed += 1
    tested += 1

print(f"Done testing. Tested: {tested}, Failed: {failed}, Success: {tested - failed}")
