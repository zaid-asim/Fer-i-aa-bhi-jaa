import urllib.request
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://www.flipkart.com/search?q=Vim+Lemon+Dishwash+Bar'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')

# find all img tags with alt containing vim
matches = re.findall(r'<img[^>]+alt="([^"]*vim[^"]*)"[^>]+src="([^"]+)"', html, re.IGNORECASE)
print("Alt matches:", len(matches))
for alt, src in matches[:3]:
    print(alt, "=>", src)
    if 'rukminim' in src:
        # download
        high_res = re.sub(r'/image/\d+/\d+/', '/image/832/832/', src)
        with open('images/products/p44.jpg', 'wb') as f:
            f.write(urllib.request.urlopen(urllib.request.Request(high_res, headers={'User-Agent': 'Mozilla/5.0'})).read())
        print("Downloaded Vim to p44.jpg!")
        break
