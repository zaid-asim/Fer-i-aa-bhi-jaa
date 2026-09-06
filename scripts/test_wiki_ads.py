import urllib.request
import urllib.parse
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context

def search_wiki_commons(query):
    try:
        url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrlimit=3&prop=imageinfo&iiprop=url&format=json"
        req = urllib.request.Request(url, headers={'User-Agent': 'FeriBot/2.0 (contact@feri.in)'})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for pid, page in pages.items():
                title = page.get('title', '')
                ii = page.get('imageinfo', [])
                if ii and 'url' in ii[0]:
                    return title, ii[0]['url']
    except Exception as e:
        return f"Error: {e}", None
    return "None", None

queries = [
    "Amul Butter advertisement",
    "Parle-G advertisement",
    "Coca-Cola advertisement",
    "Pepsi advertisement",
    "Thums Up advertisement",
    "Maggi noodles advertisement",
    "Surf Excel advertisement",
    "Cadbury advertisement",
    "Horlicks advertisement",
    "Dettol advertisement"
]

for q in queries:
    title, url = search_wiki_commons(q)
    print(f"{q} => {title} : {url}", flush=True)
