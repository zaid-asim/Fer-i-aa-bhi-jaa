import urllib.request
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context

# Only URLs known to work based on our confirmed tests
CONFIRMED_URLS = [
    # Amul Butter - CONFIRMED OK (61523 bytes)
    ("Amul Butter", "https://www.bbassets.com/media/uploads/p/l/104864_8-amul-butter-pasteurised.jpg"),
    # Tata Salt - CONFIRMED OK
    ("Tata Salt", "https://www.bbassets.com/media/uploads/p/l/40081603_6-tata-salt-salt-iodized.jpg"),
    # Parle Marie - CONFIRMED OK (80987 bytes)
    ("Parle Marie", "https://www.bbassets.com/media/uploads/p/l/40204957_3-parle-parle-marie.jpg"),
    # Kurkure Masala - CONFIRMED OK (34734 bytes)
    ("Kurkure", "https://images.openfoodfacts.org/images/products/890/149/136/1026/front_en.51.400.jpg"),
    # Coca-Cola - CONFIRMED OK (9850 bytes)
    ("Coca-Cola", "https://images.openfoodfacts.org/images/products/544/900/005/4227/front_en.563.400.jpg"),
    # Maggi - CONFIRMED OK (196181 bytes)
    ("Maggi", "https://assets.hyperpure.com/data/images/products/cdbb5abf71acf8ac95d399d630364e73.png"),
]

# Test additional OpenFoodFacts URLs using barcodes
# These are actual EAN barcodes for famous Indian products
OFF_BARCODES = {
    "Parle-G Gold": "8901250000487",
    "Britannia Good Day": "8901063026018",
    "Britannia Marie Gold": "8901063027220",
    "Britannia Bourbon": "8901063027237",
    "Amul Taaza Milk": "8901063032071",
    "Amul Gold Milk": "8901063032071",
    "Maggi Masala Noodles": "8901058000394",
    "Nescafe Classic": "7613032030810",
    "KitKat 4 Finger": "7613033575235",
    "Lay's Magic Masala": "8901019148636",
    "Pepsi Cola": "4902102112208",
    "Sprite": "5449000014276",
    "Thums Up": "8901063022010",
    "Mountain Dew": "8964000060003",
    "Mirinda Orange": "7613031750658",
    "Frooti": "8902294100031",
    "Maaza": "5449000214263",
    "Tropicana Mixed": "8901030845154",
    "Dove Soap": "6281006481607",
    "Lifebuoy Total": "8710908492310",
    "Lux Soap": "8710908533198",
    "Sunsilk Shampoo": "8710908022432",
    "Surf Excel Easy Wash": "8710819007206",
    "Vim Dishwash": "8901030784414",
    "Bru Coffee": "8901030002039",
    "Red Label Tea": "8901030000011",
    "Tata Tea Premium": "8901207010125",
    "Dabur Honey": "8901207010200",
    "Dabur Red Paste": "8901207016014",
    "Colgate StrongTeeth": "8901224008897",
    "Aashirvaad Atta": "8902080088500",
    "Parachute Coconut Oil": "8901012025107",
    "Fortune Sunflower Oil": "8901122001004",
}

def check_off_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'FeriApp/1.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get('status') == 1:
                product = data.get('product', {})
                img = product.get('image_front_url') or product.get('image_url')
                return img, product.get('product_name_en') or product.get('product_name')
    except Exception as e:
        pass
    return None, None

print("Testing OpenFoodFacts barcode API...\n")
for name, barcode in list(OFF_BARCODES.items())[:15]:
    img, pname = check_off_barcode(barcode)
    print(f"{name}: img={img}, name={pname}", flush=True)
