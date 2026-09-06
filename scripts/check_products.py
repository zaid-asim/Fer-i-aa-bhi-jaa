import json
import os
import re

DATA_FILE = "js/data.js"
with open(DATA_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Extract products array from data.js
match = re.search(r'window\.PRODUCTS\s*=\s*(\[.*?\]);', content, re.DOTALL)
if not match:
    # Try alternative matching
    match = re.search(r'const products\s*=\s*(\[.*?\]);', content, re.DOTALL)

print("Match found:", bool(match))
if match:
    raw_js = match.group(1)
    # Simple check on images/products/p*.jpg
    valid_products = []
    removed_products = []
    for i in range(1, 101):
        img_path = f"images/products/p{i}.jpg"
        if os.path.exists(img_path) and os.path.getsize(img_path) > 5000:
            valid_products.append(f"p{i}")
        else:
            removed_products.append(f"p{i}")
    print(f"Valid products count: {len(valid_products)}")
    print(f"Removed products (no image or <5KB): {removed_products}")
