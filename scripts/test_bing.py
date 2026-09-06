import urllib.request
import urllib.parse
import re
import json

def get_bing_image(query):
    try:
        url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&first=1"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        })
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Look for murl inside iusc
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
            if not matches:
                # also try standard json regex
                matches = re.findall(r'"murl":"(http[^"]+)"', html)
            if matches:
                return matches[0]
    except Exception as e:
        return f"Error: {e}"
    return None

print("Bing image for Parle-G:", get_bing_image("Parle-G Gold Biscuits packet"))
print("Bing image for Amul Butter:", get_bing_image("Amul Butter 100g pack"))
print("Bing image for Coca-Cola:", get_bing_image("Coca Cola bottle 750ml India"))
print("Bing image for Surf Excel:", get_bing_image("Surf Excel Easy Wash 1kg pack"))
print("Bing image for Dettol Soap:", get_bing_image("Dettol Original Soap pack"))
