import json, os, re

with open('js/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

prod_matches = re.findall(r'\{\s*id:\s*"([^"]+)",\s*name:\s*"([^"]+)",\s*brand:\s*"([^"]+)",\s*category:\s*"([^"]+)",\s*price:\s*(\d+),\s*mrp:\s*(\d+).*?image:\s*"([^"]+)"', content, re.DOTALL)

for pid, name, brand, cat, price, mrp, img in prod_matches:
    print(f"{pid}: {name} ({brand}) - {cat} - Rs.{price} / MRP Rs.{mrp}")
