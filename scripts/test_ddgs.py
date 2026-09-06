from duckduckgo_search import DDGS

try:
    with DDGS() as ddgs:
        results = list(ddgs.images("Parle-G Gold Biscuits", max_results=3))
        print("Success:")
        for r in results:
            print(r['image'])
except Exception as e:
    print("Error:", e)
