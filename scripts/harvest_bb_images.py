import urllib.request
import ssl
import re
import json
import time

ssl._create_default_https_context = ssl._create_unverified_context

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-IN,en;q=0.9'
}

# Known BigBasket product page URLs for our 100 FMCG items
# Format: (id, name, brand, category, bb_url)
BB_PRODUCTS = [
    # ── PARLE ──────────────────────────────────────────────────
    ("p1",  "Parle-G Gold Biscuits", "Parle", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40078765/parle-g-gold-biscuits-200-g-1-kg/"),
    ("p2",  "Parle Monaco Classic Salted", "Parle", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082547/parle-monaco-classic-salted-crackers-200-g/"),
    ("p3",  "Parle Krackjack Cracker", "Parle", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082459/parle-krackjack-original-sweet-salty-crackers-200-g/"),
    ("p4",  "Parle Hide & Seek Chocolate Chip", "Parle", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082485/parle-hide-seek-chocolate-chip-cookies-300-g/"),
    ("p5",  "Parle Frooti Mango Drink", "Parle", "Beverages", "https://www.bigbasket.com/pd/40061453/frooti-mango-drink-600-ml/"),

    # ── BRITANNIA ───────────────────────────────────────────────
    ("p6",  "Britannia Good Day Butter Cookies", "Britannia", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082546/britannia-good-day-butter-cookies-400-g/"),
    ("p7",  "Britannia Good Day Cashew Cookies", "Britannia", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082548/britannia-good-day-cashew-cookies-600-g/"),
    ("p8",  "Britannia Marie Gold Biscuits", "Britannia", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082540/britannia-marie-gold-biscuits-600-g/"),
    ("p9",  "Britannia Bourbon Cream Biscuits", "Britannia", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082550/britannia-bourbon-cream-biscuits-600-g/"),
    ("p10", "Britannia Jim Jam Cream Biscuits", "Britannia", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082555/britannia-jim-jam-cream-biscuits-300-g/"),
    ("p11", "Britannia NutriChoice Digestive", "Britannia", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082564/britannia-nutrichoice-digestive-biscuits-400-g/"),
    ("p12", "Britannia Little Hearts Biscuits", "Britannia", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082557/britannia-little-hearts-biscuits-400-g/"),
    ("p13", "Britannia 50-50 Sweet & Salty Biscuits", "Britannia", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082553/britannia-50-50-sweet-salty-crackers-400-g/"),

    # ── AMUL ────────────────────────────────────────────────────
    ("p14", "Amul Butter Pasteurised", "Amul", "Dairy & Breakfast", "https://www.bigbasket.com/pd/104864/amul-butter-pasteurised-500-g/"),
    ("p15", "Amul Taaza Toned Milk 1L", "Amul", "Dairy & Breakfast", "https://www.bigbasket.com/pd/40082637/amul-taaza-toned-milk-1-l/"),
    ("p16", "Amul Gold Full Cream Milk", "Amul", "Dairy & Breakfast", "https://www.bigbasket.com/pd/40082642/amul-gold-full-cream-milk-1-l/"),
    ("p17", "Amul Processed Cheese Slices", "Amul", "Dairy & Breakfast", "https://www.bigbasket.com/pd/104758/amul-processed-cheese-slices-200-g/"),
    ("p18", "Amul Masti Dahi", "Amul", "Dairy & Breakfast", "https://www.bigbasket.com/pd/242671/amul-masti-dahi-1-kg/"),
    ("p19", "Amul Pure Ghee", "Amul", "Dairy & Breakfast", "https://www.bigbasket.com/pd/104860/amul-pure-ghee-500-ml/"),
    ("p20", "Amul Kool Koko Milk", "Amul", "Beverages", "https://www.bigbasket.com/pd/40082612/amul-kool-koko-flavoured-milk-200-ml/"),
    ("p21", "Amul Dark Chocolate", "Amul", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40130827/amul-dark-chocolate-150-g/"),

    # ── COCA-COLA ───────────────────────────────────────────────
    ("p22", "Coca-Cola Original Taste", "Coca-Cola", "Beverages", "https://www.bigbasket.com/pd/40118753/coca-cola-original-taste-750-ml/"),
    ("p23", "Thums Up Sparkling Water", "Coca-Cola", "Beverages", "https://www.bigbasket.com/pd/40204958/thums-up-sparkling-cola-750-ml/"),
    ("p24", "Sprite Clear Lime Drink", "Coca-Cola", "Beverages", "https://www.bigbasket.com/pd/40118754/sprite-clear-lime-750-ml/"),
    ("p25", "Maaza Mango Drink", "Coca-Cola", "Beverages", "https://www.bigbasket.com/pd/40073924/maaza-mango-drink-600-ml/"),
    ("p26", "Limca Lime n Lemoni", "Coca-Cola", "Beverages", "https://www.bigbasket.com/pd/40118756/limca-lime-n-lemoni-750-ml/"),
    ("p27", "Fanta Orange Drink", "Coca-Cola", "Beverages", "https://www.bigbasket.com/pd/40118757/fanta-orange-750-ml/"),
    ("p28", "Kinley Soda Water", "Coca-Cola", "Beverages", "https://www.bigbasket.com/pd/40202434/kinley-soda-water-750-ml/"),

    # ── PEPSICO ─────────────────────────────────────────────────
    ("p29", "Pepsi Cola", "PepsiCo", "Beverages", "https://www.bigbasket.com/pd/40118763/pepsi-cola-750-ml/"),
    ("p30", "Mountain Dew Citrus Rush", "PepsiCo", "Beverages", "https://www.bigbasket.com/pd/40118764/mountain-dew-citrus-rush-750-ml/"),
    ("p31", "Mirinda Orange", "PepsiCo", "Beverages", "https://www.bigbasket.com/pd/40118765/mirinda-orange-750-ml/"),
    ("p32", "7Up Lemon Lime", "PepsiCo", "Beverages", "https://www.bigbasket.com/pd/40118766/7up-750-ml/"),
    ("p33", "Sting Berry Blast Energy Drink", "PepsiCo", "Beverages", "https://www.bigbasket.com/pd/40249895/sting-berry-blast-250-ml/"),
    ("p34", "Lay's Magic Masala", "PepsiCo", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082521/lay-s-magic-masala-chips-78-g/"),
    ("p35", "Lay's Cream & Onion", "PepsiCo", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082522/lay-s-cream-onion-chips-78-g/"),
    ("p36", "Kurkure Masala Munch", "PepsiCo", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082515/kurkure-masala-munch-105-g/"),
    ("p37", "Kurkure Chilli Chatka", "PepsiCo", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082516/kurkure-chilli-chatka-105-g/"),
    ("p38", "Tropicana Mixed Fruit Juice", "PepsiCo", "Beverages", "https://www.bigbasket.com/pd/40082604/tropicana-mixed-fruit-juice-1-l/"),

    # ── HUL ─────────────────────────────────────────────────────
    ("p39", "Dove Cream Beauty Bathing Bar", "HUL", "Personal Care", "https://www.bigbasket.com/pd/225738/dove-cream-beauty-bathing-bar-100-g/"),
    ("p40", "Pears Soft & Fresh Bathing Bar", "HUL", "Personal Care", "https://www.bigbasket.com/pd/225748/pears-soft-fresh-bathing-bar-125-g/"),
    ("p41", "Lifebuoy Total Protect Soap", "HUL", "Personal Care", "https://www.bigbasket.com/pd/225746/lifebuoy-total-10-germ-protection-soap-125-g/"),
    ("p42", "Lux Velvet Touch Soap", "HUL", "Personal Care", "https://www.bigbasket.com/pd/225742/lux-velvet-touch-bathing-soap-125-g/"),
    ("p43", "Sunsilk Lusciously Thick Shampoo", "HUL", "Personal Care", "https://www.bigbasket.com/pd/225760/sunsilk-lusciously-thick-long-shampoo-340-ml/"),
    ("p44", "Clinic Plus Strong & Long Shampoo", "HUL", "Personal Care", "https://www.bigbasket.com/pd/225757/clinic-plus-strength-shine-shampoo-340-ml/"),
    ("p45", "Vaseline Original Pure Petroleum Jelly", "HUL", "Personal Care", "https://www.bigbasket.com/pd/225779/vaseline-original-pure-petroleum-jelly-250-ml/"),
    ("p46", "Surf Excel Easy Wash Detergent", "HUL", "Cleaning & Household", "https://www.bigbasket.com/pd/225808/surf-excel-easy-wash-detergent-powder-2-kg/"),
    ("p47", "Rin Advanced Detergent Powder", "HUL", "Cleaning & Household", "https://www.bigbasket.com/pd/225812/rin-advanced-power-white-detergent-powder-1-5-kg/"),
    ("p48", "Vim Dishwash Liquid", "HUL", "Cleaning & Household", "https://www.bigbasket.com/pd/225818/vim-dishwash-liquid-gel-with-lemon-750-ml/"),
    ("p49", "Brooke Bond Red Label Tea", "HUL", "Beverages", "https://www.bigbasket.com/pd/40082688/brooke-bond-red-label-tea-500-g/"),
    ("p50", "Brooke Bond Taj Mahal Tea", "HUL", "Beverages", "https://www.bigbasket.com/pd/40082690/brooke-bond-taj-mahal-tea-500-g/"),
    ("p51", "Bru Instant Coffee", "HUL", "Beverages", "https://www.bigbasket.com/pd/40082697/bru-instant-coffee-200-g/"),
    ("p52", "Kissan Mixed Fruit Jam", "HUL", "Dairy & Breakfast", "https://www.bigbasket.com/pd/40082702/kissan-mixed-fruit-jam-500-g/"),

    # ── DABUR ───────────────────────────────────────────────────
    ("p53", "Dabur Red Paste", "Dabur", "Personal Care", "https://www.bigbasket.com/pd/225768/dabur-red-paste-300-g/"),
    ("p54", "Dabur Meswak Toothpaste", "Dabur", "Personal Care", "https://www.bigbasket.com/pd/225769/dabur-meswak-100-g/"),
    ("p55", "Dabur Honey", "Dabur", "Groceries & Staples", "https://www.bigbasket.com/pd/40082720/dabur-honey-500-g/"),
    ("p56", "Dabur Chyawanprash", "Dabur", "Groceries & Staples", "https://www.bigbasket.com/pd/40082724/dabur-chyawanprash-1-kg/"),
    ("p57", "Dabur Amla Hair Oil", "Dabur", "Personal Care", "https://www.bigbasket.com/pd/225770/dabur-amla-hair-oil-300-ml/"),
    ("p58", "Dabur Gulabari Rose Water", "Dabur", "Personal Care", "https://www.bigbasket.com/pd/225771/dabur-gulabari-rose-water-250-ml/"),
    ("p59", "Dabur Hajmola Regular", "Dabur", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082730/dabur-hajmola-regular-120-tabs/"),

    # ── ITC ─────────────────────────────────────────────────────
    ("p60", "Aashirvaad Superior MP Atta", "ITC", "Groceries & Staples", "https://www.bigbasket.com/pd/40082660/aashirvaad-superior-mp-atta-10-kg/"),
    ("p61", "Sunfeast Dark Fantasy Choco Fills", "ITC", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082580/sunfeast-dark-fantasy-choco-fills-75-g/"),
    ("p62", "Sunfeast Mom's Magic Butter Biscuits", "ITC", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082583/sunfeast-mom-s-magic-butter-cashew-biscuits-600-g/"),
    ("p63", "Bingo Mad Angles Achaari Masti", "ITC", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082530/bingo-mad-angles-achaari-masti-130-g/"),
    ("p64", "Sunfeast YiPPee! Masala Noodles", "ITC", "Groceries & Staples", "https://www.bigbasket.com/pd/40082665/sunfeast-yippee-power-up-masala-noodles-320-g/"),

    # ── NESTLE ──────────────────────────────────────────────────
    ("p65", "Maggi 2-Minute Masala Noodles", "Nestle", "Groceries & Staples", "https://www.bigbasket.com/pd/40082670/maggi-2-minute-masala-noodles-70-g/"),
    ("p66", "Maggi 2-Minute Noodles 4-Pack", "Nestle", "Groceries & Staples", "https://www.bigbasket.com/pd/40082671/maggi-2-minute-masala-noodles-4-x-70-g/"),
    ("p67", "Maggi Tomato Ketchup", "Nestle", "Groceries & Staples", "https://www.bigbasket.com/pd/40082673/maggi-tomato-ketchup-1-kg/"),
    ("p68", "Nescafe Classic Coffee", "Nestle", "Beverages", "https://www.bigbasket.com/pd/40082695/nescafe-classic-100-g/"),
    ("p69", "KitKat 4-Finger Chocolate", "Nestle", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082565/kit-kat-4-finger-chocolate-wafer-bar-41-5-g/"),
    ("p70", "Munch Crispy Chocolate", "Nestle", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082566/munch-crunchy-chocolate-40-g/"),
    ("p71", "Nestle Everyday Dairy Whitener", "Nestle", "Dairy & Breakfast", "https://www.bigbasket.com/pd/40082648/nestle-everyday-dairy-whitener-1-kg/"),

    # ── HALDIRAMS ───────────────────────────────────────────────
    ("p72", "Haldiram's Aloo Bhujia", "Haldiram's", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082504/haldiram-s-aloo-bhujia-400-g/"),
    ("p73", "Haldiram's Bhujia Sev", "Haldiram's", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082505/haldiram-s-bhujia-sev-400-g/"),
    ("p74", "Haldiram's Khatta Meetha Mix", "Haldiram's", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082506/haldiram-s-khatta-meetha-400-g/"),
    ("p75", "Haldiram's Moong Dal Namkeen", "Haldiram's", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082509/haldiram-s-moong-dal-400-g/"),
    ("p76", "Haldiram's Soan Papdi", "Haldiram's", "Snacks & Biscuits", "https://www.bigbasket.com/pd/40082510/haldiram-s-soan-papdi-250-g/"),

    # ── TATA ────────────────────────────────────────────────────
    ("p77", "Tata Salt Iodized", "Tata", "Groceries & Staples", "https://www.bigbasket.com/pd/40081603/tata-salt-vacuum-evaporated-iodised-salt-1-kg/"),
    ("p78", "Tata Salt Lite Low Sodium", "Tata", "Groceries & Staples", "https://www.bigbasket.com/pd/40143500/tata-salt-lite-low-sodium-salt-1-kg/"),
    ("p79", "Tata Tea Premium", "Tata", "Beverages", "https://www.bigbasket.com/pd/40082684/tata-tea-premium-500-g/"),
    ("p80", "Tata Tea Gold", "Tata", "Beverages", "https://www.bigbasket.com/pd/40082685/tata-tea-gold-250-g/"),
    ("p81", "Tata Sampann Toor Dal", "Tata", "Groceries & Staples", "https://www.bigbasket.com/pd/40203256/tata-sampann-toor-dal-1-kg/"),
    ("p82", "Tata Sampann Chana Dal", "Tata", "Groceries & Staples", "https://www.bigbasket.com/pd/40203257/tata-sampann-chana-dal-1-kg/"),

    # ── GODREJ & COLGATE ────────────────────────────────────────
    ("p83", "Cinthol Original Soap", "Godrej", "Personal Care", "https://www.bigbasket.com/pd/225744/cinthol-original-soap-100-g/"),
    ("p84", "Good Knight Power Chips", "Godrej", "Cleaning & Household", "https://www.bigbasket.com/pd/40082830/good-knight-power-chips-mosquito-repellent-chips/"),
    ("p85", "Colgate StrongTeeth Toothpaste", "Colgate", "Personal Care", "https://www.bigbasket.com/pd/225766/colgate-strong-teeth-toothpaste-500-g/"),
    ("p86", "Colgate MaxFresh Spicy Fresh", "Colgate", "Personal Care", "https://www.bigbasket.com/pd/225767/colgate-maxfresh-spicy-fresh-toothpaste-150-g/"),

    # ── MOTHER DAIRY ─────────────────────────────────────────────
    ("p87", "Mother Dairy Cow Milk", "Mother Dairy", "Dairy & Breakfast", "https://www.bigbasket.com/pd/40082643/mother-dairy-cow-milk-500-ml/"),
    ("p88", "Mother Dairy Classic Curd", "Mother Dairy", "Dairy & Breakfast", "https://www.bigbasket.com/pd/1202758/mother-dairy-classic-curd-400-g/"),

    # ── MARICO ──────────────────────────────────────────────────
    ("p89", "Parachute Coconut Oil", "Marico", "Personal Care", "https://www.bigbasket.com/pd/225775/parachute-100-coconut-oil-600-ml/"),
    ("p90", "Saffola Gold Oil", "Marico", "Groceries & Staples", "https://www.bigbasket.com/pd/40082664/saffola-gold-refined-oil-1-l/"),

    # ── PATANJALI ───────────────────────────────────────────────
    ("p91", "Patanjali Dant Kanti Toothpaste", "Patanjali", "Personal Care", "https://www.bigbasket.com/pd/40082755/patanjali-dant-kanti-dental-cream-200-g/"),
    ("p92", "Patanjali Cow Ghee", "Patanjali", "Dairy & Breakfast", "https://www.bigbasket.com/pd/40082758/patanjali-cow-ghee-1-l/"),

    # ── DR OETKER / FUN FOODS ───────────────────────────────────
    ("p93", "Funfoods Peanut Butter Crunchy", "Dr Oetker", "Dairy & Breakfast", "https://www.bigbasket.com/pd/40082707/funfoods-by-dr-oetker-peanut-butter-crunchy-925-g/"),

    # ── FORTUNE ─────────────────────────────────────────────────
    ("p94", "Fortune Sunlite Refined Sunflower Oil", "Fortune", "Groceries & Staples", "https://www.bigbasket.com/pd/40082661/fortune-sunlite-refined-sunflower-oil-1-l/"),
    ("p95", "Fortune Basmati Rice", "Fortune", "Groceries & Staples", "https://www.bigbasket.com/pd/40082663/fortune-biryani-special-basmati-rice-5-kg/"),

    # ── PARLE AGRO ──────────────────────────────────────────────
    ("p96", "Appy Fizz Sparkling Juice", "Parle Agro", "Beverages", "https://www.bigbasket.com/pd/40082608/appy-fizz-sparkling-apple-juice-drink-750-ml/"),
    ("p97", "Bailley Packaged Drinking Water", "Parle Agro", "Beverages", "https://www.bigbasket.com/pd/40082620/bailley-packaged-drinking-water-1-l/"),

    # ── MDH ─────────────────────────────────────────────────────
    ("p98", "MDH Chunky Chat Masala", "MDH", "Groceries & Staples", "https://www.bigbasket.com/pd/40082738/mdh-chunky-chat-masala-100-g/"),
    ("p99", "MDH Garam Masala", "MDH", "Groceries & Staples", "https://www.bigbasket.com/pd/40082739/mdh-deggi-mirch-100-g/"),
    ("p100", "Everest Chicken Masala", "Everest", "Groceries & Staples", "https://www.bigbasket.com/pd/40082742/everest-chicken-masala-50-g/"),
]

def get_og_image(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=7) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Try og:image first
            m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](https?://[^"\']+)["\']', html)
            if m:
                return m.group(1).strip()
            # Try twitter:image
            m2 = re.search(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\'](https?://[^"\']+)["\']', html)
            if m2:
                return m2.group(1).strip()
            # Try first bbassets upload
            m3 = re.search(r'https://www\.bbassets\.com/media/uploads/p/l/[^"\'\s]+', html)
            if m3:
                return m3.group(0).strip()
    except Exception as e:
        pass
    return None

def verify_image(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=4) as resp:
            return resp.status == 200
    except:
        return False

print("Starting product image harvest from BigBasket...")
results = []

for pid, name, brand, category, bb_url in BB_PRODUCTS:
    img = get_og_image(bb_url)
    if img and verify_image(img):
        status = "OK"
    else:
        img = None
        status = "FAIL"
    results.append({
        "id": pid,
        "name": name,
        "brand": brand,
        "category": category,
        "bb_url": bb_url,
        "image": img,
        "status": status
    })
    print(f"[{status}] {brand} - {name}: {img}", flush=True)
    time.sleep(0.8)  # rate limit

# Save results
with open("scripts/harvested_images.json", "w") as f:
    json.dump(results, f, indent=2)

ok_count = sum(1 for r in results if r["status"] == "OK")
print(f"\n\nDone! {ok_count}/{len(results)} images verified OK")
print("Saved to scripts/harvested_images.json")
