import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://raw.githubusercontent.com/AbhishekPardhi/Document-Retrieval/main/BigBasketProducts.csv"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        header = resp.readline().decode('utf-8', errors='ignore')
        print("Header:", header)
        for i in range(5):
            line = resp.readline().decode('utf-8', errors='ignore')
            print(f"Row {i+1}:", line[:150])
except Exception as e:
    print("Error:", e)
