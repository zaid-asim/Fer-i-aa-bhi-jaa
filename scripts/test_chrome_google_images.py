import subprocess
import re
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def search_google_image_chrome(query):
    url = f"https://www.google.com/search?tbm=isch&q={urllib.parse.quote(query)}"
    cmd = [CHROME_PATH, "--headless=new", "--disable-gpu", "--dump-dom", url]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=12, encoding="utf-8", errors="ignore")
        html = proc.stdout
        # Find gstatic thumbnail links
        gstatics = re.findall(r'https://encrypted-tbn0\.gstatic\.com/images\?q=[^"\'\s<>\\]+', html)
        if gstatics:
            return gstatics[0]
        # Also check data:image/jpeg;base64,...
        base64_imgs = re.findall(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', html)
        if base64_imgs:
            return f"BASE64: {len(base64_imgs[0])} bytes"
    except Exception as e:
        return f"Error: {e}"
    return "None"

queries = [
    "Parle-G Gold Biscuits packet",
    "Britannia Good Day Butter Cookies",
    "Surf Excel Easy Wash 2kg",
    "Vim Dishwash Gel Lemon 750ml",
    "Aashirvaad Superior MP Atta 10kg",
    "Thums Up Toofani Cola 750ml bottle"
]

import urllib.parse
for q in queries:
    res = search_google_image_chrome(q)
    print(f"{q} => {res[:80]}", flush=True)
