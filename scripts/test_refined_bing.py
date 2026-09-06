import urllib.request
import urllib.parse
import re

def get_bing_image(query):
    try:
        url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&first=1"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        })
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
            if not matches:
                matches = re.findall(r'"murl":"(http[^"]+)"', html)
            # Prioritize amazon, flipkart, bigbasket, blinkit, jiomart, or clean product domains
            clean_matches = []
            for m in matches:
                m_low = m.lower()
                if any(ext in m_low for ext in ['.jpg', '.jpeg', '.png', '.webp']) and not any(bad in m_low for bad in ['wallpaper', 'hotel', 'car', 'coin', 'iconfinder', 'desktop']):
                    clean_matches.append(m)
            if clean_matches:
                return clean_matches[0]
            if matches:
                return matches[0]
    except Exception as e:
        return f"Error: {e}"
    return None

test_items = [
    "Amul Butter packet packaging",
    "Coca Cola 750ml bottle beverage",
    "Surf Excel detergent powder packet",
    "Maggi noodles packet Nestle",
    "Britannia Good Day Cashew biscuits packet",
    "Tata Tea Premium chai packet",
    "Haldiram Bhujia Sev packet",
    "Dove Beauty Bar soap pack",
    "Head and Shoulders shampoo bottle",
    "Dabur Red Paste toothpaste box"
]

for item in test_items:
    img = get_bing_image(item)
    print(f"{item} -> {img}")
