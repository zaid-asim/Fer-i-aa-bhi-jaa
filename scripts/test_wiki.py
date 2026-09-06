import urllib.request
import urllib.parse
import json

def get_wiki_image(title):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&format=json&pithumbsize=500"
        req = urllib.request.Request(url, headers={'User-Agent': 'FeriECommerceApp/1.0 (contact@feriapp.in)'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data['query']['pages']
            for pid, pdata in pages.items():
                if 'thumbnail' in pdata:
                    return pdata['thumbnail']['source']
    except Exception as e:
        return str(e)
    return None

test_wiki = [
    "Parle-G",
    "Frooti",
    "Thums Up",
    "Maaza",
    "Amul",
    "Maggi",
    "Kurkure",
    "Limca",
    "Bournvita",
    "Hajmola",
    "Chyawanprash"
]

for t in test_wiki:
    print(t, "->", get_wiki_image(t))
