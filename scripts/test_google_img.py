import urllib.request
import urllib.parse
import re

def search_google_image(query):
    try:
        url = f"https://www.google.com/search?tbm=isch&q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('latin1', errors='ignore')
            # Extract image URLs from Google Images HTML
            # Google images embed preview images in src="https://encrypted-tbn0.gstatic.com/images?q=tbn:..."
            tbns = re.findall(r'src="(https://encrypted-tbn0\.gstatic\.com/images\?q=tbn:[^"]+)"', html)
            if tbns:
                return tbns[0]
            # or try unescaped
            tbns2 = re.findall(r'(https://encrypted-tbn0\.gstatic\.com/images\?q=tbn:[^"\\]+)', html)
            if tbns2:
                return tbns2[0]
            # or original image urls: ["http...", width, height]
            orig = re.findall(r'\["(https://[^"]+\.(?:jpg|png|jpeg))",\d+,\d+\]', html)
            if orig:
                return orig[0]
            return "No match, html length: " + str(len(html))
    except Exception as e:
        return f"Error: {e}"

print("Google image for Parle-G:", search_google_image("Parle-G Gold Biscuits"))
print("Google image for Amul Butter:", search_google_image("Amul Butter packet"))
print("Google image for Coca Cola:", search_google_image("Coca Cola bottle India"))
print("Google image for Surf Excel:", search_google_image("Surf Excel Easy Wash powder"))
print("Google image for Dove Soap:", search_google_image("Dove Cream Beauty Bar soap"))
