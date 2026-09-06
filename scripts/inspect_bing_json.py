import urllib.request
import urllib.parse
import ssl
import json
import re

ssl._create_default_https_context = ssl._create_unverified_context

def inspect_bing_structure(query):
    url = "https://www.bing.com/images/search?q=" + urllib.parse.quote(query) + "&first=1"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Look for m='{...}'
            matches = re.findall(r'class="iusc"[^>]*m="([^"]+)"', html)
            print(f"Found {len(matches)} iusc elements for query: {query}")
            for m_raw in matches[:3]:
                # unescape html entities
                clean_json = m_raw.replace('&quot;', '"').replace('&amp;', '&')
                try:
                    data = json.loads(clean_json)
                    print("  Title:", data.get('t', data.get('desc', '')))
                    print("  Murl :", data.get('murl'))
                    print("  Turl :", data.get('turl'))
                except Exception as ex:
                    print("  JSON error:", ex)
    except Exception as e:
        print("Error:", e)

inspect_bing_structure("Surf Excel Easy Wash detergent packet")
inspect_bing_structure("Vim Dishwash Gel bottle 750ml")
inspect_bing_structure("Aashirvaad Atta 10kg")
