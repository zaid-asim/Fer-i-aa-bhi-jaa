import urllib.request
import urllib.parse
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context

def search_wikimedia(query):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&pithumbsize=600&titles={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'FeriBot/1.0 (contact@feri.in)'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for pid, page in pages.items():
                if 'thumbnail' in page:
                    return page['thumbnail']['source']
    except Exception as e:
        return f"Error: {e}"
    return None

test_titles = [
    "Parle-G",
    "Frooti",
    "Good Day (biscuit)",
    "Amul",
    "Coca-Cola",
    "Thums Up",
    "Sprite (drink)",
    "Maaza",
    "Limca",
    "Fanta",
    "Pepsi",
    "Mountain Dew",
    "7 Up",
    "Kurkure",
    "Lay's",
    "Dove (brand)",
    "Lifebuoy (soap)",
    "Lux (soap)",
    "Surf Excel",
    "Maggi",
    "Kit Kat",
    "Horlicks",
    "Complan",
    "Dettol"
]

for t in test_titles:
    img = search_wikimedia(t)
    print(f"{t} => {img}", flush=True)
