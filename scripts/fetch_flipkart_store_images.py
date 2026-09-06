import os
import sys
import re
import urllib.request
import urllib.parse
import ssl
import time
from concurrent.futures import ThreadPoolExecutor

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssl._create_default_https_context = ssl._create_unverified_context

OUT_DIR = "images/products"
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-IN,en;q=0.9'
}

PRODUCTS = [
    ("p1", "Parle-G Gold Biscuits"),
    ("p2", "Parle Monaco Classic Regular Salted Biscuits"),
    ("p3", "Parle Krackjack Sweet & Salty Crackers"),
    ("p4", "Parle Hide & Seek Chocolate Chip Cookies"),
    ("p5", "Frooti Fresh 'N' Juicy Mango Drink"),
    ("p6", "Britannia Good Day Butter Cookies"),
    ("p7", "Britannia Good Day Cashew Cookies"),
    ("p8", "Britannia Marie Gold Crisp Tea Biscuits"),
    ("p9", "Britannia Bourbon Chocolate Cream Biscuits"),
    ("p10", "Britannia NutriChoice Digestive High Fibre"),
    ("p11", "Amul Pasteurised Butter 500g"),
    ("p12", "Amul Taaza Homogenised Toned Milk"),
    ("p13", "Amul Gold Homogenised Standardised Milk"),
    ("p14", "Amul Processed Cheese Slices"),
    ("p15", "Amul Masti Dahi Pouch"),
    ("p16", "Amul Pure Cow Ghee 1L Tin"),
    ("p17", "Amul Dark Chocolate 55% Cocoa"),
    ("p18", "Coca-Cola Original Taste 750ml Bottle"),
    ("p19", "Thums Up Charged Strong Cola 750ml"),
    ("p20", "Sprite Lime Flavoured Soft Drink"),
    ("p21", "Maaza Mango Drink 600ml Bottle"),
    ("p22", "Limca Lime 'N' Lemoni Soft Drink"),
    ("p23", "Fanta Orange Flavour Sparkling Drink"),
    ("p24", "Kinley Extra Strong Club Soda 750ml"),
    ("p25", "Pepsi Cola Carbonated Soft Drink 750ml"),
    ("p26", "Mountain Dew Darr Ke Aage Jeet Hai"),
    ("p27", "Mirinda Orange Flavour Soft Drink"),
    ("p28", "7UP Lemon Lime Carbonated Drink"),
    ("p29", "Sting Energy Drink Gold Rush Bottle"),
    ("p30", "Lay's India's Magic Masala Potato Chips"),
    ("p31", "Lay's American Style Cream & Onion Chips"),
    ("p32", "Kurkure Masala Munch Crispy Snacks"),
    ("p33", "Kurkure Green Chutney Style Snacks"),
    ("p34", "Tropicana 100% Mixed Fruit Delight Juice"),
    ("p35", "Dove Cream Beauty Bathing Bar Soap"),
    ("p36", "Pears Pure & Gentle Glycerine Soap"),
    ("p37", "Lifebuoy Total 10 Germ Protection Soap"),
    ("p38", "Lux Velvet Glow Jasmine & Almond Oil Soap"),
    ("p39", "Sunsilk Black Shine Shampoo"),
    ("p40", "Clinic Plus Strong & Long Health Shampoo"),
    ("p41", "Vaseline Original Pure Skin Jelly"),
    ("p42", "Surf Excel Quick Wash Detergent Powder"),
    ("p43", "Rin Advanced Detergent Bar"),
    ("p44", "Vim Dishwash Gel Lemon 750ml Bottle"),
    ("p45", "Brooke Bond Red Label Strong CTC Tea"),
    ("p46", "Brooke Bond Taj Mahal Gourmet Tea"),
    ("p47", "Bru Instant Coffee Chicory Mix Jar"),
    ("p48", "Kissan 100% Real Mixed Fruit Jam"),
    ("p49", "Dabur Red Ayurvedic Toothpaste"),
    ("p50", "Dabur 100% Pure Squeezy Honey"),
    ("p51", "Dabur Chyawanprash Immunity Booster 1kg"),
    ("p52", "Dabur Amla Nourishing Hair Oil"),
    ("p53", "Dabur Regular Digestive Tablets"),
    ("p54", "Aashirvaad Shuddh Chakki Whole Wheat Atta"),
    ("p55", "Sunfeast Dark Fantasy Choco Fills Cookies"),
    ("p56", "Sunfeast Mom's Magic Cashew & Almond Biscuits"),
    ("p57", "Bingo! Mad Angles Achaari M मस्ती"),
    ("p58", "Sunfeast YiPPee! Magic Masala Noodles"),
    ("p59", "Maggi 2-Minute Masala Instant Noodles"),
    ("p60", "Maggi 2-Minute Noodles Family Saver 4-Pack"),
    ("p61", "Maggi Rich Tomato Ketchup Bottle"),
    ("p62", "Nescafe Classic Pure Instant Coffee Jar"),
    ("p63", "Nestle KitKat 4-Finger Crisp Wafer"),
    ("p64", "Nestle Munch Crunchy Wafer Bar"),
    ("p65", "Nestle Everyday Dairy Whitener Milk Powder"),
    ("p66", "Haldiram's Nagpur Aloo Bhujia Namkeen"),
    ("p67", "Haldiram's Khatta Meetha Sweet & Sour Mixture"),
    ("p68", "Haldiram's Salted Crunchy Moong Dal"),
    ("p69", "Haldiram's Bikaneri Bhujia Sev"),
    ("p70", "Haldiram's Premium Desi Ghee Soan Papdi"),
    ("p71", "Tata Salt Vacuum Evaporated Iodised Salt"),
    ("p72", "Tata Tea Premium Desh Ki Chai"),
    ("p73", "Tata Tea Gold Rich Taste & Aroma"),
    ("p74", "Tata Sampann Unpolished High Protein Toor Dal"),
    ("p75", "Tata Sampann Unpolished Chana Dal"),
    ("p76", "Godrej Cinthol Original Deodorant Bath Soap"),
    ("p77", "Good Knight Gold Flash Liquid Mosquito Refill"),
    ("p78", "Colgate Strong Teeth Dental Cream Toothpaste"),
    ("p79", "Colgate MaxFresh Peppermint Ice Gel Toothpaste"),
    ("p80", "Parachute 100% Pure Coconut Hair Oil"),
    ("p81", "Saffola Gold Pro Healthy Heart Blended Oil"),
    ("p82", "Patanjali Dant Kanti Ayurvedic Toothpaste"),
    ("p83", "Patanjali Pure Desi Cow Ghee 1L"),
    ("p84", "Mother Dairy Fresh Full Cream Milk Pouch"),
    ("p85", "Mother Dairy Classic Creamy Dahi Cup"),
    ("p86", "Fortune Sunlite Refined Sunflower Cooking Oil"),
    ("p87", "Fortune Biryani Special Basmati Rice 5kg"),
    ("p88", "MDH Chunky Chat Masala Seasoning"),
    ("p89", "MDH Deggi Mirch Natural Red Chilli Powder"),
    ("p90", "Everest Chicken Curry Special Masala"),
    ("p91", "Appy Fizz Sparkling Apple Juice Drink"),
    ("p92", "Bailley Packaged Drinking Mineral Water 1L"),
    ("p93", "Dr. Oetker FunFoods Creamy Peanut Butter"),
    ("p94", "Horlicks Classic Malt Health Drink Refill"),
    ("p95", "Complan Royale Chocolate Health Drink Refill"),
    ("p96", "Harpic Power Plus 10X Max Clean Toilet Cleaner"),
    ("p97", "Dettol Original Germ Protection Liquid Handwash"),
    ("p98", "Dettol Antiseptic First Aid Liquid 550ml"),
    ("p99", "Mortein Powergard All Insect Killer Spray"),
    ("p100", "Amul Kool Kesar Flavoured Milk Can")
]

def fetch_flipkart_image(item):
    pid, title = item
    out_file = f"{OUT_DIR}/{pid}.jpg"
    
    # Query Flipkart
    url = f"https://www.flipkart.com/search?q={urllib.parse.quote(title)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract rukminim links
            imgs = re.findall(r'https://rukminim\d*\.flixcart\.com/image/[^"\'\s<>\\]+', html)
            # Filter for product packshots (avoid icons, banners, payment logos)
            valid_imgs = [img for img in imgs if ('cookie-biscuit' in img or 'noodle' in img or 'soap' in img or 'shampoo' in img or 'detergent' in img or 'edible-oil' in img or 'tea' in img or 'coffee' in img or 'soft-drink' in img or 'ghee' in img or 'dairy' in img or 'toothpaste' in img or 'namkeen' in img or 'jam' in img or 'pulses' in img or 'rice' in img or 'spice' in img or 'xif0q' in img or 'original' in img)]
            
            chosen_url = valid_imgs[0] if valid_imgs else (imgs[0] if imgs else None)
            if chosen_url:
                # Upgrade image resolution from 128/128 or 612/612 to 832/832
                chosen_url = re.sub(r'/image/\d+/\d+/', '/image/832/832/', chosen_url)
                # Download image
                img_req = urllib.request.Request(chosen_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(img_req, timeout=8) as img_resp:
                    content = img_resp.read()
                    if len(content) > 5000:
                        with open(out_file, 'wb') as f:
                            f.write(content)
                        return pid, title, True, len(content)
    except Exception as e:
        return pid, title, False, str(e)
    return pid, title, False, "No image found"

print(f"Starting Flipkart real store image harvester for {len(PRODUCTS)} products...", flush=True)

success = 0
with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(fetch_flipkart_image, PRODUCTS)
    for pid, title, ok, detail in results:
        if ok:
            print(f"[{pid}] STORE OK: {title} ({detail} bytes)", flush=True)
            success += 1
        else:
            print(f"[{pid}] FAILED: {title} => {detail}", flush=True)

print(f"\nALL DONE: {success} / {len(PRODUCTS)} formal store images downloaded!", flush=True)
