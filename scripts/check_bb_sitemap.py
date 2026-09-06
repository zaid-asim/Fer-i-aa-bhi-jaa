import urllib.request
import ssl
import gzip
import re

ssl._create_default_https_context = ssl._create_unverified_context

# Check if bigbasket sitemap or robots exists
url = "https://www.bigbasket.com/robots.txt"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        text = resp.read().decode('utf-8', errors='ignore')
        sitemaps = re.findall(r'Sitemap:\s*(https?://[^\s]+)', text)
        print("Sitemaps:", sitemaps)
except Exception as e:
    print("Error:", e)
