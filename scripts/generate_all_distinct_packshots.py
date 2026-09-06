import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "images/products"
os.makedirs(OUT_DIR, exist_ok=True)

# 100 Distinct Product Packshot Definitions
# (id, name, brand, category, pack_type, primary_color, accent_color, badge, icon_type, subtitle)
PACKSHOTS = [
    # ─── PARLE ────────────────────────────────────────────────────────
    ("p1", "Parle-G Gold Biscuits", "PARLE", "Snacks & Biscuits", "box", "#D97706", "#DC2626", "800g • Gluco Energy", "biscuit", "Original Gluco Biscuits"),
    ("p2", "Parle Monaco Crackers", "PARLE", "Snacks & Biscuits", "box", "#15803D", "#EAB308", "200g • Light & Crispy", "cracker", "Classic Salted Crackers"),
    ("p3", "Parle Krackjack Crackers", "PARLE", "Snacks & Biscuits", "box", "#047857", "#DC2626", "200g • Sweet & Salty", "cracker", "Original Dual Flavour"),
    ("p4", "Parle Hide & Seek Cookies", "PARLE", "Snacks & Biscuits", "box", "#451A03", "#D97706", "300g • Real Choco Chips", "choco", "Chocolate Chip Indulgence"),
    ("p5", "Frooti Mango Drink", "PARLE AGRO", "Beverages", "bottle", "#EAB308", "#15803D", "600ml • Real Mango", "drink", "Fresh Mango Delight"),

    # ─── BRITANNIA ────────────────────────────────────────────────────
    ("p6", "Good Day Butter Cookies", "BRITANNIA", "Snacks & Biscuits", "box", "#CA8A04", "#2563EB", "400g • Rich Butter", "cookie", "Melt in Mouth Butter"),
    ("p7", "Good Day Cashew Cookies", "BRITANNIA", "Snacks & Biscuits", "box", "#7E22CE", "#EAB308", "600g • Real Roasted Cashew", "nut", "Rich Cashew Delight"),
    ("p8", "Britannia Marie Gold", "BRITANNIA", "Snacks & Biscuits", "box", "#C2410C", "#D97706", "600g • 10 Essential Vitamins", "tea_biscuit", "Tea Time Classic"),
    ("p9", "Britannia Bourbon", "BRITANNIA", "Snacks & Biscuits", "box", "#3E1F0F", "#DC2626", "600g • Dark Choco Cream", "choco_bar", "Original Choco Sandwich"),
    ("p10", "NutriChoice Digestive", "BRITANNIA", "Snacks & Biscuits", "box", "#15803D", "#A16207", "400g • High Fibre Wheat", "leaf", "100% Whole Wheat"),

    # ─── AMUL ─────────────────────────────────────────────────────────
    # p11 (Amul Butter) is already the verified official packshot, KEEP IT!
    ("p12", "Amul Taaza Toned Milk", "AMUL", "Dairy & Breakfast", "pouch", "#2563EB", "#1E40AF", "1L • 3.0% Fat", "milk_drop", "Homogenised Toned Milk"),
    ("p13", "Amul Gold Full Cream", "AMUL", "Dairy & Breakfast", "pouch", "#DC2626", "#B91C1C", "1L • 6.0% Fat Cream", "milk_drop", "Full Cream Fresh Milk"),
    ("p14", "Amul Processed Cheese", "AMUL", "Dairy & Breakfast", "box", "#D97706", "#B45309", "200g • 10 Wrapped Slices", "cheese", "Rich Dairy Cheese Slices"),
    ("p15", "Amul Masti Dahi Curd", "AMUL", "Dairy & Breakfast", "tub", "#059669", "#047857", "1kg • Natural Probiotics", "curd", "Thick & Creamy Dahi"),
    ("p16", "Amul Pure Cow Ghee", "AMUL", "Dairy & Breakfast", "tin", "#B45309", "#78350F", "500ml • Traditional Aroma", "ghee", "Granular Clarified Butter"),
    ("p17", "Amul 55% Dark Chocolate", "AMUL", "Snacks & Biscuits", "box", "#1C1917", "#D97706", "150g • 55% Pure Cocoa", "choco_bar", "Single Origin Cocoa Bar"),

    # ─── COCA-COLA ────────────────────────────────────────────────────
    ("p18", "Coca-Cola Original Taste", "COCA-COLA", "Beverages", "bottle", "#DC2626", "#B91C1C", "750ml • Sparkling Cola", "bottle_icon", "Original Uplifting Taste"),
    ("p19", "Thums Up Toofani Cola", "THUMS UP", "Beverages", "bottle", "#1E3A8A", "#DC2626", "750ml • Strong Fizzy Cola", "thunder", "Taste the Thunder"),
    ("p20", "Sprite Clear Lime", "SPRITE", "Beverages", "bottle", "#059669", "#10B981", "750ml • Crisp Lemon Lime", "lime", "100% Clear Refreshment"),
    ("p21", "Maaza Mango Beverage", "MAAZA", "Beverages", "bottle", "#D97706", "#15803D", "600ml • Alphonso Mango", "mango", "Asli Mango Ka Mazaa"),
    ("p22", "Limca Lime 'n' Lemoni", "LIMCA", "Beverages", "bottle", "#0D9488", "#059669", "750ml • Zesty Cloudy Lime", "lime", "Original Lemon Fizz"),
    ("p23", "Fanta Orange Sparkling", "FANTA", "Beverages", "bottle", "#EA580C", "#FBBF24", "750ml • Bold Orange Soda", "orange", "Fruity Orange Blast"),
    ("p24", "Kinley Club Soda Water", "KINLEY", "Beverages", "bottle", "#0284C7", "#0369A1", "750ml • Extra Carbonation", "fizz", "Pure Sparkling Soda"),

    # ─── PEPSICO ──────────────────────────────────────────────────────
    ("p25", "Pepsi Cola Refreshing", "PEPSI", "Beverages", "bottle", "#1E40AF", "#DC2626", "750ml • Bold Sparkling", "bottle_icon", "Bold Cola Experience"),
    ("p26", "Mountain Dew Citrus", "MOUNTAIN DEW", "Beverages", "bottle", "#65A30D", "#4D7C0F", "750ml • Neon Citrus Rush", "lightning", "Darr Ke Aage Jeet Hai"),
    ("p27", "Mirinda Orange Soda", "MIRINDA", "Beverages", "bottle", "#F97316", "#EA580C", "750ml • Tangy Orange", "orange", "Vibrant Tangy Fizz"),
    ("p28", "7UP Lemon Lime Soda", "7UP", "Beverages", "bottle", "#16A34A", "#DC2626", "750ml • Clear Lime Fresh", "lime", "Natural Lemon & Lime"),
    ("p29", "Sting Berry Blast Energy", "STING", "Beverages", "bottle", "#E11D48", "#BE123C", "250ml • High Caffeine", "lightning", "Electrifying Energy"),
    ("p30", "Lay's Magic Masala", "LAY'S", "Snacks & Biscuits", "pouch", "#1D4ED8", "#DC2626", "78g • Indian Spices", "chips", "India's Magic Masala"),
    ("p31", "Lay's Cream & Onion", "LAY'S", "Snacks & Biscuits", "pouch", "#16A34A", "#059669", "78g • American Sour Cream", "chips", "Smooth Cream & Onion"),
    ("p32", "Kurkure Masala Munch", "KURKURE", "Snacks & Biscuits", "pouch", "#EA580C", "#DC2626", "105g • Tedha Crunchy Puffs", "curls", "Original Chatpata Crunch"),
    ("p33", "Kurkure Chilli Chatka", "KURKURE", "Snacks & Biscuits", "pouch", "#15803D", "#DC2626", "105g • Spicy Tangy Chilli", "curls", "Fiery Red Chilli Kick"),
    ("p34", "Tropicana Mixed Fruit", "TROPICANA", "Beverages", "carton", "#D97706", "#DC2626", "1L • 100% Real Juice", "fruit", "No Added Preservatives"),

    # ─── HUL ──────────────────────────────────────────────────────────
    ("p35", "Dove Cream Beauty Bar", "DOVE", "Personal Care", "bar", "#0284C7", "#D97706", "100g • 1/4 Moisturiser", "dove_icon", "Gentle Cleansing Formula"),
    ("p36", "Pears Pure & Gentle Soap", "PEARS", "Personal Care", "bar", "#D97706", "#B45309", "125g • 98% Pure Glycerin", "glycerin", "Soft & Translucent Glow"),
    ("p37", "Lifebuoy Total Protect", "LIFEBUOY", "Personal Care", "bar", "#DC2626", "#991B1B", "125g • 99.9% Germ Shield", "shield", "Activ Silver Formula"),
    ("p38", "Lux Velvet Touch Jasmine", "LUX", "Personal Care", "bar", "#DB2777", "#9D174D", "125g • Jasmine & Almond Oil", "flower", "Velvety Soft Fragrance"),
    ("p39", "Sunsilk Thick & Long", "SUNSILK", "Personal Care", "bottle", "#1E293B", "#DB2777", "340ml • Keratin Yoghurt", "hair", "2x Thicker Looking Hair"),
    ("p40", "Clinic Plus Strong & Long", "CLINIC PLUS", "Personal Care", "bottle", "#0284C7", "#0369A1", "340ml • Milk Protein Care", "hair", "Strengthens From Roots"),
    ("p41", "Vaseline Petroleum Jelly", "VASELINE", "Personal Care", "tub", "#0284C7", "#D97706", "250ml • 100% Triple Purified", "jelly", "Locks in Deep Moisture"),
    ("p42", "Surf Excel Easy Wash", "SURF EXCEL", "Cleaning & Household", "pouch", "#1E40AF", "#E11D48", "2kg • Stain Blaster Particles", "sparkle", "Superior Stain Removal"),
    ("p43", "Rin Advanced Detergent", "RIN", "Cleaning & Household", "pouch", "#2563EB", "#EAB308", "1.5kg • Dazzling Whites", "lightning", "Bright Clean Technology"),
    ("p44", "Vim Dishwash Gel Lemon", "VIM", "Cleaning & Household", "bottle", "#EAB308", "#16A34A", "750ml • 100 Lemons Power", "lemon", "Grease Dissolve in 1 Swipe"),
    ("p45", "Red Label Natural Care", "BROOKE BOND", "Beverages", "box", "#B91C1C", "#D97706", "500g • 5 Ayurvedic Herbs", "tea_leaf", "Swad Apnepan Ka"),
    ("p46", "Taj Mahal Gourmet Tea", "TAJ MAHAL", "Beverages", "box", "#1E3A8A", "#D97706", "500g • Precious Flavour Buds", "tea_leaf", "Wah Taj Signature Taste"),
    ("p47", "Bru Instant Pure Coffee", "BRU", "Beverages", "jar", "#78350F", "#B45309", "200g • Roasted Chicory Blend", "coffee", "Rich Coffee Bean Aroma"),
    ("p48", "Kissan Mixed Fruit Jam", "KISSAN", "Dairy & Breakfast", "jar", "#DC2626", "#15803D", "500g • 8 Real Fruits Mix", "fruit", "Real Sweet Fruit Spread"),

    # ─── DABUR ────────────────────────────────────────────────────────
    ("p49", "Dabur Red Toothpaste", "DABUR", "Personal Care", "tube", "#DC2626", "#78350F", "300g • 13 Potent Herbs", "tooth", "Ayurvedic Dental Shield"),
    ("p50", "Dabur 100% Pure Honey", "DABUR", "Groceries & Staples", "jar", "#D97706", "#B45309", "500g • NMR Tested Pure", "honeycomb", "Natural Immunity Booster"),
    ("p51", "Dabur Chyawanprash", "DABUR", "Groceries & Staples", "jar", "#78350F", "#DC2626", "1kg • 40+ Natural Herbs", "herb", "2x Immunity Clinically Proven"),
    ("p52", "Dabur Amla Hair Oil", "DABUR", "Personal Care", "bottle", "#15803D", "#166534", "300ml • Pure Indian Gooseberry", "leaf", "Deep Roots & Black Shine"),
    ("p53", "Dabur Hajmola Regular", "DABUR", "Snacks & Biscuits", "bottle", "#6B21A8", "#581C87", "120 tabs • Chatpata Digestive", "pill", "Traditional Digestive Spices"),

    # ─── ITC ──────────────────────────────────────────────────────────
    ("p54", "Aashirvaad Sharbati Atta", "AASHIRVAAD", "Groceries & Staples", "sack", "#B45309", "#D97706", "10kg • MP Golden Sharbati", "wheat", "0% Maida, 100% Whole Wheat"),
    ("p55", "Dark Fantasy Choco Fills", "SUNFEAST", "Snacks & Biscuits", "box", "#1C1917", "#D97706", "75g • Molten Choco Core", "choco", "Pure Molten Indulgence"),
    ("p56", "Mom's Magic Cashew Butter", "SUNFEAST", "Snacks & Biscuits", "box", "#D97706", "#B45309", "600g • Roasted Cashews", "cookie", "Rich Home Baked Flavour"),
    ("p57", "Bingo Mad Angles Achaari", "BINGO", "Snacks & Biscuits", "pouch", "#7C3AED", "#EAB308", "130g • Triangle Spiced Crisps", "triangle", "Zesty Mango Pickle Punch"),
    ("p58", "YiPPee! Magic Masala", "SUNFEAST", "Groceries & Staples", "pouch", "#EA580C", "#2563EB", "320g • Long Non-Sticky Noodles", "noodles", "Appetizing Veggie Touch"),

    # ─── NESTLE ───────────────────────────────────────────────────────
    ("p59", "Maggi 2-Minute Noodles", "MAGGI", "Groceries & Staples", "pouch", "#EAB308", "#DC2626", "70g • Tastemaker Inside", "noodles", "Signature Roasted Masala"),
    ("p60", "Maggi Noodles Value 4-Pack", "MAGGI", "Groceries & Staples", "pouch", "#EAB308", "#B91C1C", "4×70g • Family Saver Pack", "noodles", "Classic Comfort Food"),
    ("p61", "Maggi Rich Tomato Sauce", "MAGGI", "Groceries & Staples", "bottle", "#DC2626", "#15803D", "1kg • Sun-Ripened Tomatoes", "tomato", "Thick & Tangy Squeeze"),
    ("p62", "Nescafe Classic Coffee", "NESCAFE", "Beverages", "jar", "#3E1F0F", "#DC2626", "100g • 100% Pure Robusta", "coffee", "Signature Red Cup Aroma"),
    ("p63", "KitKat 4 Finger Chocolate", "KITKAT", "Snacks & Biscuits", "bar", "#DC2626", "#3E1F0F", "41.5g • Crisp Layered Wafer", "choco_bar", "Have a Break, Have a KitKat"),
    ("p64", "Munch Crunchy Chocolate", "MUNCH", "Snacks & Biscuits", "bar", "#EAB308", "#7C3AED", "40g • Maximum Crunch Wafer", "choco_bar", "Light & Crunchy Delight"),
    ("p65", "Everyday Dairy Whitener", "NESTLE", "Dairy & Breakfast", "pouch", "#1E40AF", "#3B82F6", "1kg • Spray Dried Milk", "milk_drop", "Thick & Rich Homely Chai"),

    # ─── HALDIRAMS ────────────────────────────────────────────────────
    ("p66", "Haldiram's Aloo Bhujia", "HALDIRAM'S", "Snacks & Biscuits", "pouch", "#15803D", "#EAB308", "400g • Crispy Potato Mint", "namkeen", "India's No.1 Spiced Bhujia"),
    ("p67", "Haldiram's Khatta Meetha", "HALDIRAM'S", "Snacks & Biscuits", "pouch", "#EA580C", "#CA8A04", "400g • Sweet & Sour Mix", "namkeen", "Rice Flakes, Peas & Peanuts"),
    ("p68", "Haldiram's Moong Dal", "HALDIRAM'S", "Snacks & Biscuits", "pouch", "#EAB308", "#CA8A04", "400g • Salted Split Lentils", "lentil", "Protein Rich Light Crunch"),
    ("p69", "Haldiram's Bhujia Sev", "HALDIRAM'S", "Snacks & Biscuits", "pouch", "#B91C1C", "#EAB308", "400g • Bikaneri Moth Flour", "namkeen", "Spicy Black Pepper Kick"),
    ("p70", "Haldiram's Soan Papdi", "HALDIRAM'S", "Snacks & Biscuits", "box", "#D97706", "#78350F", "250g • Flaky Almond Dessert", "sweet", "Delicate Royal Pistachio"),

    # ─── TATA ─────────────────────────────────────────────────────────
    # p71 (Tata Salt) is already the verified official packshot, KEEP IT!
    ("p72", "Tata Tea Premium", "TATA TEA", "Beverages", "pouch", "#15803D", "#EAB308", "500g • Badi & Choti Patti", "tea_leaf", "Desh Ki Chai Blend"),
    ("p73", "Tata Tea Gold Fine Leaf", "TATA TEA", "Beverages", "pouch", "#CA8A04", "#1E293B", "250g • 15% Long Leaves", "tea_leaf", "Exquisite Amber Liquor"),
    ("p74", "Tata Sampann Toor Dal", "TATA SAMPANN", "Groceries & Staples", "pouch", "#D97706", "#B45309", "1kg • Unpolished Pigeon Peas", "dal", "High Dietary Fibre Protein"),
    ("p75", "Tata Sampann Chana Dal", "TATA SAMPANN", "Groceries & Staples", "pouch", "#CA8A04", "#78350F", "1kg • Unpolished Bengal Gram", "dal", "Authentic Earthy Flavour"),

    # ─── GODREJ & COLGATE ─────────────────────────────────────────────
    ("p76", "Cinthol Original Soap", "CINTHOL", "Personal Care", "bar", "#DC2626", "#B91C1C", "100g • High 79% TFM", "shield", "Doctor Recommended Deodorant"),
    ("p77", "Good Knight Gold Flash", "GOOD KNIGHT", "Cleaning & Household", "box", "#1E293B", "#DC2626", "Machine + 45ml • Flash Mode", "flash", "Automatic Mosquito Defense"),
    ("p78", "Colgate Strong Teeth", "COLGATE", "Personal Care", "tube", "#DC2626", "#2563EB", "500g • Amino Shakti Formula", "tooth", "2x Stronger Enamel Calcium"),
    ("p79", "Colgate MaxFresh Spicy Red", "COLGATE", "Personal Care", "tube", "#DC2626", "#0284C7", "150g • Cooling Crystals", "ice", "Intense Fresh Breath Burst"),

    # ─── MARICO ───────────────────────────────────────────────────────
    ("p80", "Parachute Pure Coconut Oil", "PARACHUTE", "Personal Care", "bottle", "#0369A1", "#0284C7", "600ml • 100% Edible Copra", "coconut", "Triple Filtered Pure Oil"),
    ("p81", "Saffola Gold Blended Oil", "SAFFOLA", "Groceries & Staples", "bottle", "#EAB308", "#DC2626", "1L • LOSORB Technology", "heart", "Heart Pro Oryzanol Blend"),

    # ─── PATANJALI ────────────────────────────────────────────────────
    ("p82", "Patanjali Dant Kanti Paste", "PATANJALI", "Personal Care", "tube", "#15803D", "#D97706", "200g • Akarkara & Neem", "herb", "Complete Herbal Dental Care"),
    ("p83", "Patanjali Pure Cow Ghee", "PATANJALI", "Dairy & Breakfast", "tin", "#D97706", "#15803D", "1L • Indigenous Desi Cow", "ghee", "Ayurvedic Clarified Butter"),

    # ─── MOTHER DAIRY ─────────────────────────────────────────────────
    ("p84", "Mother Dairy Full Cream", "MOTHER DAIRY", "Dairy & Breakfast", "pouch", "#1D4ED8", "#2563EB", "500ml • Pasteurised Fresh", "milk_drop", "Rich Froth for Daily Chai"),
    ("p85", "Mother Dairy Creamy Curd", "MOTHER DAIRY", "Dairy & Breakfast", "tub", "#0284C7", "#1D4ED8", "400g • Smooth Set Curd", "curd", "Cooling Gut-Friendly Dahi"),

    # ─── FORTUNE ──────────────────────────────────────────────────────
    ("p86", "Fortune Sunflower Oil", "FORTUNE", "Groceries & Staples", "bottle", "#EAB308", "#CA8A04", "1L • Enriched with Vit A & D", "sunflower", "Light Healthy Cooking Oil"),
    ("p87", "Fortune Biryani Basmati", "FORTUNE", "Groceries & Staples", "sack", "#1E3A8A", "#D97706", "5kg • Extra Long Aged Grains", "rice", "Royal Aromatic Basmati"),

    # ─── MDH & EVEREST ────────────────────────────────────────────────
    ("p88", "MDH Chunky Chat Masala", "MDH", "Groceries & Staples", "box", "#DC2626", "#B91C1C", "100g • Asli Masale Sach Sach", "spice", "Tangy Dry Mango Seasoning"),
    ("p89", "MDH Deggi Mirch Powder", "MDH", "Groceries & Staples", "box", "#991B1B", "#DC2626", "100g • Natural Kashmiri Red", "spice", "Vibrant Colour & Mild Heat"),
    ("p90", "Everest Chicken Masala", "EVEREST", "Groceries & Staples", "box", "#B91C1C", "#D97706", "50g • Coarse Ground Spice", "spice", "Rich & Thick Curry Gravy"),

    # ─── PARLE AGRO ───────────────────────────────────────────────────
    ("p91", "Appy Fizz Sparkling Apple", "APPY FIZZ", "Beverages", "bottle", "#1C1917", "#D97706", "750ml • Champagne Apple Juice", "apple", "Crisp Sparkling Apple Kick"),
    ("p92", "Bailley Mineral Water", "BAILLEY", "Beverages", "bottle", "#0284C7", "#0369A1", "1L • 50-Step Purification", "water_drop", "Fortified with Minerals"),

    # ─── HEALTH DRINKS & SPREADS ──────────────────────────────────────
    ("p93", "Funfoods Crunchy Peanut", "FUNFOODS", "Dairy & Breakfast", "jar", "#78350F", "#B45309", "925g • 26g Plant Protein", "peanut", "91% Roasted Peanut Chunks"),
    ("p94", "Horlicks Classic Malt Drink", "HORLICKS", "Beverages", "bottle", "#1E40AF", "#EA580C", "500g • Clinically Proven", "wheat", "Taller, Stronger, Sharper"),
    ("p95", "Complan Royale Chocolate", "COMPLAN", "Beverages", "box", "#D97706", "#3E1F0F", "500g • 34 Vital Nutrients", "milk_drop", "100% First Class Protein"),

    # ─── HOME & HYGIENE ───────────────────────────────────────────────
    ("p96", "Harpic Power Plus Cleaner", "HARPIC", "Cleaning & Household", "bottle", "#1E3A8A", "#DC2626", "1L • 10x Stain Removal", "shield", "Destroys 99.9% Toilet Germs"),
    ("p97", "Dettol Liquid Handwash", "DETTOL", "Personal Care", "bottle", "#15803D", "#047857", "200ml • 100 Germ Protection", "cross", "Original Pine Hand Shield"),
    ("p98", "Dettol Antiseptic Liquid", "DETTOL", "Personal Care", "bottle", "#D97706", "#B45309", "250ml • Proven Antiseptic", "cross", "Golden First Aid Standard"),
    ("p99", "Mortein Fast Knockdown", "MORTEIN", "Cleaning & Household", "bottle", "#DC2626", "#991B1B", "625ml • Instant Mosquito Kill", "target", "Fast Action Aerosol Spray"),
    ("p100", "Amul Kool Kesar Almond", "AMUL KOOL", "Beverages", "bottle", "#CA8A04", "#B45309", "200ml • Saffron & Almonds", "drink", "Chilled Royal Nut Milk")
]

def render_packshot(pid, name, brand, category, pack_type, primary, accent, badge, icon_type, subtitle):
    # Keep verified official packshots untouched!
    out_file = os.path.join(OUT_DIR, f"{pid}.jpg")
    if pid in ["p11", "p71"]:
        if os.path.exists(out_file) and os.path.getsize(out_file) > 10000:
            print(f"Skipping {pid} ({name}) - keeping verified official photo")
            return

    img = Image.new("RGB", (600, 600), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    # Soft studio backdrop glow
    for r in range(270, 0, -15):
        shade = 240 + int((r/270)*15)
        draw.ellipse([300 - r, 300 - r, 300 + r, 300 + r], fill=(shade, shade + 3, 252))

    # Soft ground contact shadow
    for i in range(12):
        sw = 170 + i * 8
        sh = 18 + i * 2
        draw.ellipse([300 - sw, 515 - sh, 300 + sw, 515 + sh], fill=(215 - i*2, 220 - i*2, 230 - i*2))

    # Geometry per pack_type
    if pack_type == "bottle":
        # Cap
        draw.rounded_rectangle([272, 75, 328, 105], radius=5, fill=accent)
        draw.rectangle([275, 105, 325, 120], fill=primary)
        # Neck
        draw.polygon([(275, 120), (325, 120), (355, 175), (245, 175)], fill=primary)
        # Body
        draw.rounded_rectangle([210, 170, 390, 505], radius=32, fill=primary)
        # Left 3D gloss reflection
        draw.rounded_rectangle([222, 185, 238, 490], radius=8, fill=(255, 255, 255, 90))
        # Label container
        draw.rounded_rectangle([225, 225, 375, 455], radius=14, fill="#FFFFFF")
        lb = [225, 225, 375, 455]
    elif pack_type in ["pouch", "sack"]:
        # Top crimp seal
        draw.polygon([(185, 95), (415, 95), (400, 125), (200, 125)], fill=accent)
        # Body
        draw.rounded_rectangle([190, 115, 410, 505], radius=22, fill=primary)
        # Left shadow fold
        draw.polygon([(190, 115), (212, 135), (212, 485), (190, 505)], fill=(0, 0, 0, 35))
        # Label container
        draw.rounded_rectangle([210, 155, 390, 475], radius=14, fill="#FFFFFF")
        lb = [210, 155, 390, 475]
    elif pack_type in ["jar", "tub"]:
        # Threaded lid
        draw.rounded_rectangle([215, 130, 385, 175], radius=12, fill=accent)
        draw.rectangle([225, 170, 375, 185], fill=(0, 0, 0, 25))
        # Jar body
        draw.rounded_rectangle([210, 180, 390, 495], radius=28, fill=primary)
        # Label container
        draw.rounded_rectangle([225, 225, 375, 455], radius=12, fill="#FFFFFF")
        lb = [225, 225, 375, 455]
    elif pack_type == "tube":
        # Screw cap at bottom
        draw.rounded_rectangle([265, 470, 335, 515], radius=6, fill=accent)
        # Tube body
        draw.polygon([(215, 105), (385, 105), (355, 470), (245, 470)], fill=primary)
        # Top crimp seal
        draw.rectangle([210, 90, 390, 108], fill=accent)
        # Center label
        draw.rounded_rectangle([235, 145, 365, 435], radius=10, fill="#FFFFFF")
        lb = [235, 145, 365, 435]
    elif pack_type == "bar":
        # Soap/Choco bar shape
        draw.rounded_rectangle([180, 150, 420, 465], radius=24, fill=primary)
        draw.rounded_rectangle([190, 160, 410, 455], radius=20, fill="#FFFFFF")
        lb = [190, 160, 410, 455]
    else: # box, carton, tin
        draw.rounded_rectangle([185, 115, 415, 500], radius=16, fill=primary)
        draw.rectangle([195, 125, 405, 142], fill=accent)
        draw.rounded_rectangle([200, 155, 400, 485], radius=12, fill="#FFFFFF")
        lb = [200, 155, 400, 485]

    # Draw Brand Ribbon
    draw.rounded_rectangle([lb[0] + 12, lb[1] + 14, lb[2] - 12, lb[1] + 58], radius=8, fill=accent)
    draw.text((300, lb[1] + 36), brand[:16], fill="#FFFFFF", anchor="mm", font_size=20)

    # Product Name
    # Split name into two lines if long
    words = name.split()
    if len(words) > 3:
        line1 = " ".join(words[:3])
        line2 = " ".join(words[3:])
        draw.text((300, lb[1] + 88), line1, fill="#0F172A", anchor="mm", font_size=18)
        draw.text((300, lb[1] + 112), line2, fill="#0F172A", anchor="mm", font_size=16)
        sub_y = lb[1] + 138
    else:
        draw.text((300, lb[1] + 95), name, fill="#0F172A", anchor="mm", font_size=19)
        sub_y = lb[1] + 124

    draw.text((300, sub_y), subtitle[:28], fill="#64748B", anchor="mm", font_size=13)

    # Bottom Badge Pill with net weight & claim
    clean_badge = badge.replace("•", "-")
    draw.rounded_rectangle([lb[0] + 12, lb[3] - 38, lb[2] - 12, lb[3] - 12], radius=13, fill=accent)
    draw.text((300, lb[3] - 25), clean_badge[:30], fill="#FFFFFF", anchor="mm", font_size=12)

    # Graphic Center Circle with distinctive brand accent
    cy = (sub_y + lb[3] - 38) // 2
    draw.ellipse([268, cy - 30, 332, cy + 30], fill=primary)
    draw.ellipse([274, cy - 24, 326, cy + 24], fill=accent)

    img.save(out_file, "JPEG", quality=94)
    print(f"Generated {pid}.jpg: {brand} - {name}")

for p in PACKSHOTS:
    render_packshot(*p)

print("\nALL 100 PACKSHOTS FINISHED GENERATING SUCCESSFULLY!")
