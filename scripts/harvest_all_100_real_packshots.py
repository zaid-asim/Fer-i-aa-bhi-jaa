import os
import urllib.request
import urllib.parse
import ssl
import json
import time

ssl._create_default_https_context = ssl._create_unverified_context

OUT_DIR = "images/products"
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {'User-Agent': 'FeriGroceryCatalog/2.0 (contact@feri.in)'}

# 100 Products with targeted queries
PRODUCTS = [
    # PARLE
    ("p1", "Parle-G", ["Parle-G", "Parle G biscuit"]),
    ("p2", "Parle Monaco", ["Parle Monaco", "Monaco biscuit", "Monaco salted"]),
    ("p3", "Parle Krackjack", ["Parle Krackjack", "Krackjack", "Krack jack"]),
    ("p4", "Parle Hide & Seek", ["Hide & Seek", "Hide and Seek chocolate", "Parle Hide Seek"]),
    ("p5", "Frooti", ["Frooti", "Frooti mango"]),

    # BRITANNIA
    ("p6", "Britannia Good Day Butter", ["Good Day butter", "Britannia Good Day", "Good Day cookies"]),
    ("p7", "Britannia Good Day Cashew", ["Good Day cashew", "Britannia cashew cookies"]),
    ("p8", "Britannia Marie Gold", ["Marie Gold", "Britannia Marie", "Marie Gold biscuit"]),
    ("p9", "Britannia Bourbon", ["Britannia Bourbon", "Bourbon biscuit", "Bourbon chocolate"]),
    ("p10", "Britannia NutriChoice", ["NutriChoice", "Britannia Nutrichoice digestive", "Nutrichoice digestive"]),

    # AMUL
    ("p11", "Amul Butter", ["Amul butter pasteurised", "Amul Butter"]),
    ("p12", "Amul Taaza Milk", ["Amul Taaza", "Amul toned milk", "Amul Taaza milk"]),
    ("p13", "Amul Gold Milk", ["Amul Gold", "Amul Gold milk", "Amul full cream"]),
    ("p14", "Amul Cheese", ["Amul cheese", "Amul cheese slices", "Amul processed cheese"]),
    ("p15", "Amul Dahi", ["Amul Masti Dahi", "Amul dahi", "Amul curd"]),
    ("p16", "Amul Ghee", ["Amul ghee", "Amul pure ghee", "Amul cow ghee"]),
    ("p17", "Amul Dark Chocolate", ["Amul dark chocolate", "Amul chocolate"]),

    # COCA-COLA
    ("p18", "Coca-Cola", ["Coca-Cola original", "Coca Cola", "Coke"]),
    ("p19", "Thums Up", ["Thums Up", "Thumbs up cola"]),
    ("p20", "Sprite", ["Sprite", "Sprite lemon lime"]),
    ("p21", "Maaza", ["Maaza", "Maaza mango"]),
    ("p22", "Limca", ["Limca", "Limca lemoni"]),
    ("p23", "Fanta", ["Fanta orange", "Fanta"]),
    ("p24", "Kinley Soda", ["Kinley soda", "Kinley water"]),

    # PEPSICO
    ("p25", "Pepsi", ["Pepsi", "Pepsi cola"]),
    ("p26", "Mountain Dew", ["Mountain Dew", "Mountain dew citrus"]),
    ("p27", "Mirinda", ["Mirinda", "Mirinda orange"]),
    ("p28", "7UP", ["7UP", "7 Up lemon"]),
    ("p29", "Sting", ["Sting energy", "Sting drink"]),
    ("p30", "Lay's Magic Masala", ["Lays India's Magic Masala", "Lays magic masala", "Lays blue"]),
    ("p31", "Lay's Cream & Onion", ["Lays cream and onion", "Lays cream onion", "Lays green"]),
    ("p32", "Kurkure Masala Munch", ["Kurkure Masala Munch", "Kurkure"]),
    ("p33", "Kurkure Chilli Chatka", ["Kurkure chilli", "Kurkure green"]),
    ("p34", "Tropicana Mixed Fruit", ["Tropicana mixed fruit", "Tropicana juice"]),

    # HUL
    ("p35", "Dove Soap", ["Dove beauty bar", "Dove soap", "Dove white"]),
    ("p36", "Pears Soap", ["Pears soap", "Pears pure & gentle", "Pears glycerin"]),
    ("p37", "Lifebuoy Soap", ["Lifebuoy soap", "Lifebuoy total", "Lifebuoy"]),
    ("p38", "Lux Soap", ["Lux soap", "Lux velvet touch"]),
    ("p39", "Sunsilk Shampoo", ["Sunsilk shampoo", "Sunsilk black", "Sunsilk"]),
    ("p40", "Clinic Plus Shampoo", ["Clinic Plus shampoo", "Clinic Plus"]),
    ("p41", "Vaseline Petroleum Jelly", ["Vaseline petroleum jelly", "Vaseline jelly", "Vaseline"]),
    ("p42", "Surf Excel", ["Surf Excel", "Surf Excel detergent", "Surf Excel bar"]),
    ("p43", "Rin Detergent", ["Rin detergent", "Rin soap", "Rin"]),
    ("p44", "Vim Dishwash", ["Vim dishwash", "Vim bar", "Vim gel"]),
    ("p45", "Red Label Tea", ["Red Label tea", "Brooke Bond Red Label", "Red label"]),
    ("p46", "Taj Mahal Tea", ["Taj Mahal tea", "Brooke Bond Taj Mahal"]),
    ("p47", "Bru Coffee", ["Bru coffee", "Bru instant"]),
    ("p48", "Kissan Jam", ["Kissan mixed fruit jam", "Kissan jam"]),

    # DABUR
    ("p49", "Dabur Red Paste", ["Dabur Red paste", "Dabur Red toothpaste", "Dabur red"]),
    ("p50", "Dabur Honey", ["Dabur honey", "Dabur pure honey"]),
    ("p51", "Dabur Chyawanprash", ["Dabur Chyawanprash", "Chyawanprash"]),
    ("p52", "Dabur Amla Hair Oil", ["Dabur Amla hair oil", "Dabur Amla"]),
    ("p53", "Dabur Hajmola", ["Dabur Hajmola", "Hajmola"]),

    # ITC
    ("p54", "Aashirvaad Atta", ["Aashirvaad Superior MP Atta", "Aashirvaad atta", "Aashirvaad"]),
    ("p55", "Dark Fantasy", ["Dark Fantasy choco fills", "Sunfeast Dark Fantasy", "Dark Fantasy"]),
    ("p56", "Mom's Magic", ["Mom's Magic cashew", "Sunfeast Mom's Magic", "Mom's Magic"]),
    ("p57", "Bingo Mad Angles", ["Bingo Mad Angles", "Bingo Tedhe Medhe", "Bingo"]),
    ("p58", "YiPPee! Noodles", ["YiPPee! noodles", "Sunfeast Yippee", "Yippee noodles"]),

    # NESTLE
    ("p59", "Maggi Noodles", ["Maggi 2-Minute", "Maggi noodles", "Maggi masala"]),
    ("p60", "Maggi 4-Pack", ["Maggi masala noodles", "Maggi 4 pack"]),
    ("p61", "Maggi Ketchup", ["Maggi tomato ketchup", "Maggi sauce", "Maggi ketchup"]),
    ("p62", "Nescafe Classic", ["Nescafe classic", "Nescafe coffee", "Nescafe"]),
    ("p63", "KitKat", ["KitKat chocolate", "Kit Kat wafer", "KitKat"]),
    ("p64", "Munch", ["Nestle Munch", "Munch chocolate"]),
    ("p65", "Nestle Everyday", ["Nestle Everyday", "Everyday dairy whitener"]),

    # HALDIRAMS
    ("p66", "Haldiram's Aloo Bhujia", ["Haldiram's Aloo Bhujia", "Aloo Bhujia Haldiram", "Aloo Bhujia"]),
    ("p67", "Haldiram's Khatta Meetha", ["Haldiram's Khatta Meetha", "Khatta Meetha"]),
    ("p68", "Haldiram's Moong Dal", ["Haldiram's Moong Dal", "Moong Dal Haldiram", "Moong Dal namkeen"]),
    ("p69", "Haldiram's Bhujia Sev", ["Haldiram's Bhujia Sev", "Bikaneri Bhujia"]),
    ("p70", "Haldiram's Soan Papdi", ["Haldiram's Soan Papdi", "Soan Papdi"]),

    # TATA
    ("p71", "Tata Salt", ["Tata Salt", "Tata Salt vacuum"]),
    ("p72", "Tata Tea Premium", ["Tata Tea Premium", "Tata Tea"]),
    ("p73", "Tata Tea Gold", ["Tata Tea Gold"]),
    ("p74", "Tata Sampann Toor Dal", ["Tata Sampann Toor Dal", "Tata Sampann dal", "Toor Dal"]),
    ("p75", "Tata Sampann Chana Dal", ["Tata Sampann Chana Dal", "Chana Dal"]),

    # GODREJ & COLGATE
    ("p76", "Cinthol Soap", ["Cinthol soap", "Cinthol original", "Cinthol"]),
    ("p77", "Good Knight", ["Good Knight", "Good Knight refill", "Good knight flash"]),
    ("p78", "Colgate Strong Teeth", ["Colgate Strong Teeth", "Colgate dental cream", "Colgate toothpaste"]),
    ("p79", "Colgate MaxFresh", ["Colgate MaxFresh", "Colgate Max Fresh"]),

    # MARICO
    ("p80", "Parachute Coconut Oil", ["Parachute coconut oil", "Parachute pure coconut oil", "Parachute"]),
    ("p81", "Saffola Gold", ["Saffola Gold", "Saffola oil", "Saffola"]),

    # PATANJALI
    ("p82", "Patanjali Dant Kanti", ["Patanjali Dant Kanti", "Dant Kanti toothpaste", "Dant Kanti"]),
    ("p83", "Patanjali Cow Ghee", ["Patanjali cow ghee", "Patanjali ghee"]),

    # MOTHER DAIRY
    ("p84", "Mother Dairy Milk", ["Mother Dairy milk", "Mother Dairy full cream"]),
    ("p85", "Mother Dairy Curd", ["Mother Dairy curd", "Mother Dairy dahi"]),

    # FORTUNE
    ("p86", "Fortune Sunflower Oil", ["Fortune sunflower oil", "Fortune Sunlite"]),
    ("p87", "Fortune Basmati Rice", ["Fortune basmati rice", "Fortune biryani basmati", "Basmati rice"]),

    # MDH & EVEREST
    ("p88", "MDH Chunky Chat Masala", ["MDH Chunky Chat Masala", "Chunky Chat Masala", "MDH chat masala"]),
    ("p89", "MDH Deggi Mirch", ["MDH Deggi Mirch", "Deggi Mirch", "MDH chilli"]),
    ("p90", "Everest Chicken Masala", ["Everest chicken masala", "Everest masala"]),

    # PARLE AGRO & MISC
    ("p91", "Appy Fizz", ["Appy Fizz", "Appy Fizz sparkling apple"]),
    ("p92", "Bailley Mineral Water", ["Bailley water", "Bailley packaged drinking water"]),
    ("p93", "Funfoods Peanut Butter", ["Funfoods peanut butter", "Dr Oetker peanut butter"]),
    ("p94", "Horlicks", ["Horlicks", "Horlicks classic malt"]),
    ("p95", "Complan", ["Complan", "Complan royale chocolate"]),

    # CLEANING & HYGIENE
    ("p96", "Harpic", ["Harpic", "Harpic power plus", "Harpic toilet cleaner"]),
    ("p97", "Dettol Liquid Handwash", ["Dettol liquid handwash", "Dettol handwash", "Dettol hand wash"]),
    ("p98", "Dettol Antiseptic", ["Dettol antiseptic liquid", "Dettol antiseptic", "Dettol liquid"]),
    ("p99", "Mortein Spray", ["Mortein insect spray", "Mortein aerosol", "Mortein"]),
    ("p100", "Amul Kool", ["Amul Kool", "Amul Kool kesar", "Amul flavoured milk"])
]

KNOWN_VERIFIED = {
    "p11": "https://www.bbassets.com/media/uploads/p/l/104864_8-amul-butter-pasteurised.jpg",
    "p71": "https://www.bbassets.com/media/uploads/p/l/40081603_6-tata-salt-salt-iodized.jpg",
    "p1": "https://images.openfoodfacts.org/images/products/890/171/913/4845/front_en.11.400.jpg",
    "p6": "https://images.openfoodfacts.org/images/products/890/106/302/6018/front_en.3.400.jpg",
    "p7": "https://images.openfoodfacts.org/images/products/890/106/309/3522/front_en.28.400.jpg",
    "p8": "https://images.openfoodfacts.org/images/products/890/106/316/2914/front_en.3.400.jpg",
    "p9": "https://images.openfoodfacts.org/images/products/890/106/313/9329/front_en.14.400.jpg",
    "p18": "https://images.openfoodfacts.org/images/products/544/900/005/4227/front_en.563.400.jpg",
    "p20": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Sprite_lemon_lime_1.jpg/960px-Sprite_lemon_lime_1.jpg",
    "p22": "https://images.openfoodfacts.org/images/products/890/176/401/2204/front_en.3.400.jpg",
    "p25": "https://images.openfoodfacts.org/images/products/490/210/211/2208/front_en.4.400.jpg",
    "p30": "https://images.openfoodfacts.org/images/products/890/149/150/3020/front_en.35.400.jpg",
    "p32": "https://images.openfoodfacts.org/images/products/890/149/136/1026/front_en.51.400.jpg",
    "p50": "https://images.openfoodfacts.org/images/products/890/120/702/5365/front_en.14.400.jpg",
    "p54": "https://images.openfoodfacts.org/images/products/890/172/501/6838/front_en.7.400.jpg",
    "p59": "https://images.openfoodfacts.org/images/products/000/008/908/0153/front_en.8.400.jpg",
    "p62": "https://images.openfoodfacts.org/images/products/000/008/900/9758/front_en.3.400.jpg",
    "p80": "https://images.openbeautyfacts.org/images/products/890/108/815/0729/front_en.3.400.jpg",
    "p96": "https://images.openproductsfacts.org/images/products/890/139/615/2002/front_en.21.400.jpg",
    "p97": "https://images.openbeautyfacts.org/images/products/890/139/632/4584/front_en.9.400.jpg"
}

def search_product(queries):
    servers = [
        "https://in.openfoodfacts.org",
        "https://world.openfoodfacts.org",
        "https://in.openbeautyfacts.org",
        "https://in.openproductsfacts.org",
        "https://world.openbeautyfacts.org",
        "https://world.openproductsfacts.org"
    ]
    for q in queries:
        for base in servers:
            try:
                url = f"{base}/cgi/search.pl?search_terms={urllib.parse.quote(q)}&search_simple=1&action=process&json=1&page_size=2"
                req = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=4) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    for p in data.get('products', []):
                        img = p.get('image_front_url') or p.get('image_url')
                        name = p.get('product_name') or p.get('product_name_en')
                        if img:
                            return img, name
            except Exception:
                pass
            time.sleep(0.3)
    return None, None

def download_file(url, out_path):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read()
            if len(content) > 3000:
                with open(out_path, 'wb') as f:
                    f.write(content)
                return True
    except Exception:
        pass
    return False

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

success_count = 0
for pid, title, queries in PRODUCTS:
    out_file = f"{OUT_DIR}/{pid}.jpg"
    
    # Only skip p1 to p35 (which were already verified as real photos) and p71
    if pid in ["p71"] or (pid[1:].isdigit() and int(pid[1:]) <= 35 and pid not in ["p20", "p25"]):
        if os.path.exists(out_file) and os.path.getsize(out_file) > 8000:
            print(f"[{pid}] VERIFIED REAL PHOTO: {title} ({os.path.getsize(out_file)} bytes)", flush=True)
            success_count += 1
            continue

    # Priority 1: Known verified direct link
    if pid in KNOWN_VERIFIED:
        if download_file(KNOWN_VERIFIED[pid], out_file):
            print(f"[{pid}] VERIFIED: {title} ({os.path.getsize(out_file)} bytes)", flush=True)
            success_count += 1
            continue
            
    # Priority 2: Real-time search across OpenFacts
    img_url, real_name = search_product(queries)
    if img_url and download_file(img_url, out_file):
        safe_name = str(real_name).encode('ascii', 'replace').decode('ascii')
        print(f"[{pid}] REAL SEARCH: {title} => {safe_name} ({os.path.getsize(out_file)} bytes)", flush=True)
        success_count += 1
    else:
        print(f"[{pid}] FAILED SEARCH: {title}", flush=True)
    
    time.sleep(0.3)

print(f"\nFINISHED: {success_count} / {len(PRODUCTS)} real images downloaded!")
