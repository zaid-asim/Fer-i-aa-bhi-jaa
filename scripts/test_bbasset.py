import urllib.request

url = "https://www.bbassets.com/media/uploads/p/l/104864_8-amul-butter-pasteurised.jpg"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        print("Status:", resp.status, "Content-Length:", len(resp.read()))
except Exception as e:
    print("Error:", e)
