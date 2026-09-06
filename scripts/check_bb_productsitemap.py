import urllib.request
import ssl
import gzip
import re

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.bigbasket.com/sitemap/productsitemap1.xml"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read()
        try:
            content = gzip.decompress(content).decode('utf-8', errors='ignore')
        except:
            content = content.decode('utf-8', errors='ignore')
        print("Sitemap 1 length:", len(content))
        urls = re.findall(r'<loc>(.*?)</loc>', content)
        print("Total product URLs in sitemap 1:", len(urls))
        for u in urls[:10]:
            print("URL:", u)
        # Check image tags in sitemap: <image:loc>...</image:loc>
        img_locs = re.findall(r'<image:loc>(.*?)</image:loc>', content)
        print("Total image tags in sitemap:", len(img_locs))
        for img in img_locs[:5]:
            print("IMG:", img)
except Exception as e:
    print("Error:", e)
