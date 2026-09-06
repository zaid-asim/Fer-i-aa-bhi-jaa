import json

# 100 Major Indian brand products
indian_products = [
    # Snacks & Biscuits
    ("Parle-G Gold Biscuits", "Parle", "Snacks & Biscuits", 50, 60, "1 kg", ["biscuits", "tea", "snack"]),
    ("Britannia Good Day Cashew", "Britannia", "Snacks & Biscuits", 35, 40, "200 g", ["biscuits", "snack", "sweet"]),
    ("Britannia Marie Gold", "Britannia", "Snacks & Biscuits", 30, 35, "250 g", ["biscuits", "tea", "healthy"]),
    ("Sunfeast Dark Fantasy Choco Fills", "Sunfeast", "Snacks & Biscuits", 38, 40, "75 g", ["biscuits", "chocolate", "sweet"]),
    ("Haldiram's Bhujia Sev", "Haldiram's", "Snacks & Biscuits", 100, 110, "400 g", ["namkeen", "spicy", "snack"]),
    ("Haldiram's Moong Dal", "Haldiram's", "Snacks & Biscuits", 55, 60, "200 g", ["namkeen", "snack"]),
    ("Haldiram's Aloo Bhujia", "Haldiram's", "Snacks & Biscuits", 105, 115, "400 g", ["namkeen", "spicy", "snack"]),
    ("Lays India's Magic Masala", "Lays", "Snacks & Biscuits", 20, 20, "50 g", ["chips", "potato", "snack"]),
    ("Lays American Style Cream & Onion", "Lays", "Snacks & Biscuits", 20, 20, "50 g", ["chips", "potato", "snack"]),
    ("Kurkure Masala Munch", "Kurkure", "Snacks & Biscuits", 20, 20, "90 g", ["chips", "spicy", "snack"]),
    ("Bingo Mad Angles Tomato Madness", "Bingo", "Snacks & Biscuits", 20, 20, "70 g", ["chips", "snack"]),
    ("Parle Monaco Biscuits", "Parle", "Snacks & Biscuits", 15, 20, "75 g", ["biscuits", "salty", "snack"]),
    ("Britannia Bourbon", "Britannia", "Snacks & Biscuits", 30, 35, "150 g", ["biscuits", "chocolate", "sweet"]),
    ("Unibic Choco Chip Cookies", "Unibic", "Snacks & Biscuits", 60, 75, "150 g", ["biscuits", "cookies", "chocolate"]),
    ("Balaji Wafers Cream & Onion", "Balaji", "Snacks & Biscuits", 10, 10, "30 g", ["chips", "potato", "snack"]),

    # Beverages
    ("Coca-Cola Original Taste", "Coca-Cola", "Beverages", 40, 40, "750 ml", ["cold drink", "soda", "cola"]),
    ("Thumbs Up Soft Drink", "Coca-Cola", "Beverages", 40, 40, "750 ml", ["cold drink", "soda", "strong"]),
    ("Sprite Clear Beverage", "Coca-Cola", "Beverages", 40, 40, "750 ml", ["cold drink", "soda", "lemon"]),
    ("Maaza Mango Drink", "Coca-Cola", "Beverages", 45, 50, "600 ml", ["juice", "mango", "sweet"]),
    ("Pepsi Soft Drink", "PepsiCo", "Beverages", 40, 40, "750 ml", ["cold drink", "soda", "cola"]),
    ("Mountain Dew", "PepsiCo", "Beverages", 40, 40, "750 ml", ["cold drink", "soda"]),
    ("Mirinda Orange", "PepsiCo", "Beverages", 40, 40, "750 ml", ["cold drink", "soda", "orange"]),
    ("Slice Mango Drink", "PepsiCo", "Beverages", 45, 50, "600 ml", ["juice", "mango", "sweet"]),
    ("Frooti Mango Drink", "Parle", "Beverages", 65, 70, "1 L", ["juice", "mango", "sweet"]),
    ("Paper Boat Aamras", "Paper Boat", "Beverages", 35, 40, "250 ml", ["juice", "mango", "traditional"]),
    ("Red Bull Energy Drink", "Red Bull", "Beverages", 115, 125, "250 ml", ["energy", "caffeine"]),
    ("Sting Energy Drink", "PepsiCo", "Beverages", 20, 20, "250 ml", ["energy", "caffeine"]),
    ("Taj Mahal Tea", "Brooke Bond", "Beverages", 350, 380, "500 g", ["tea", "chai", "hot"]),
    ("Red Label Tea", "Brooke Bond", "Beverages", 250, 270, "500 g", ["tea", "chai", "hot"]),
    ("Tata Tea Premium", "Tata", "Beverages", 240, 260, "500 g", ["tea", "chai", "hot"]),
    ("Nescafe Classic Instant Coffee", "Nestle", "Beverages", 150, 160, "50 g", ["coffee", "hot", "caffeine"]),
    ("Bru Instant Coffee", "HUL", "Beverages", 140, 150, "50 g", ["coffee", "hot", "caffeine"]),

    # Dairy & Breakfast
    ("Amul Taaza Toned Milk", "Amul", "Dairy & Breakfast", 65, 68, "1 L", ["milk", "dairy", "fresh"]),
    ("Amul Butter Pasteurised", "Amul", "Dairy & Breakfast", 55, 58, "100 g", ["butter", "dairy", "spread"]),
    ("Amul Cheese Slices", "Amul", "Dairy & Breakfast", 130, 140, "200 g", ["cheese", "dairy"]),
    ("Amul Masti Dahi", "Amul", "Dairy & Breakfast", 35, 35, "400 g", ["curd", "dahi", "dairy"]),
    ("Mother Dairy Cow Milk", "Mother Dairy", "Dairy & Breakfast", 55, 55, "1 L", ["milk", "dairy", "fresh"]),
    ("Mother Dairy Classic Dahi", "Mother Dairy", "Dairy & Breakfast", 35, 35, "400 g", ["curd", "dahi", "dairy"]),
    ("Britannia Cheese Block", "Britannia", "Dairy & Breakfast", 125, 135, "200 g", ["cheese", "dairy"]),
    ("Kellogg's Corn Flakes", "Kellogg's", "Dairy & Breakfast", 160, 180, "475 g", ["cereal", "breakfast", "healthy"]),
    ("Kellogg's Chocos", "Kellogg's", "Dairy & Breakfast", 170, 190, "390 g", ["cereal", "breakfast", "chocolate"]),
    ("Saffola Oats", "Saffola", "Dairy & Breakfast", 150, 175, "1 kg", ["oats", "breakfast", "healthy"]),
    ("Quaker Oats", "Quaker", "Dairy & Breakfast", 165, 190, "1 kg", ["oats", "breakfast", "healthy"]),
    ("Bagrry's Muesli", "Bagrry's", "Dairy & Breakfast", 250, 290, "400 g", ["muesli", "breakfast", "healthy"]),
    ("MTR Poha", "MTR", "Dairy & Breakfast", 50, 60, "500 g", ["poha", "breakfast", "indian"]),
    ("Kissan Mixed Fruit Jam", "HUL", "Dairy & Breakfast", 155, 170, "500 g", ["jam", "spread", "sweet"]),
    ("Nutella Hazelnut Spread", "Ferrero", "Dairy & Breakfast", 350, 385, "350 g", ["spread", "chocolate", "sweet"]),

    # Groceries & Staples
    ("Aashirvaad Shudh Chakki Atta", "ITC", "Groceries & Staples", 230, 260, "5 kg", ["atta", "flour", "wheat"]),
    ("Fortune Sunlite Sunflower Oil", "Fortune", "Groceries & Staples", 145, 160, "1 L", ["oil", "cooking", "sunflower"]),
    ("Saffola Gold Cooking Oil", "Saffola", "Groceries & Staples", 185, 210, "1 L", ["oil", "cooking", "healthy"]),
    ("Dhara Mustard Oil", "Dhara", "Groceries & Staples", 160, 180, "1 L", ["oil", "cooking", "mustard"]),
    ("India Gate Basmati Rice", "India Gate", "Groceries & Staples", 450, 500, "5 kg", ["rice", "basmati", "grain"]),
    ("Kohinoor Basmati Rice", "Kohinoor", "Groceries & Staples", 420, 480, "5 kg", ["rice", "basmati", "grain"]),
    ("Tata Salt", "Tata", "Groceries & Staples", 25, 28, "1 kg", ["salt", "spice", "essential"]),
    ("Catch Coriander Powder", "Catch", "Groceries & Staples", 75, 85, "100 g", ["spice", "masala"]),
    ("Everest Garam Masala", "Everest", "Groceries & Staples", 80, 90, "100 g", ["spice", "masala"]),
    ("MDH Chana Masala", "MDH", "Groceries & Staples", 70, 80, "100 g", ["spice", "masala"]),
    ("Maggi 2-Minute Noodles", "Nestle", "Groceries & Staples", 14, 15, "70 g", ["noodles", "snack", "instant"]),
    ("YiPPee! Magic Masala Noodles", "ITC", "Groceries & Staples", 14, 15, "70 g", ["noodles", "snack", "instant"]),
    ("Ching's Secret Schezwan Chutney", "Ching's", "Groceries & Staples", 85, 95, "250 g", ["chutney", "sauce", "spicy"]),
    ("Kissan Fresh Tomato Ketchup", "HUL", "Groceries & Staples", 130, 145, "950 g", ["sauce", "ketchup", "tomato"]),
    ("Maggi Rich Tomato Ketchup", "Nestle", "Groceries & Staples", 135, 150, "1 kg", ["sauce", "ketchup", "tomato"]),

    # Personal Care
    ("Dove Cream Beauty Bathing Bar", "HUL", "Personal Care", 55, 60, "100 g", ["soap", "bath", "beauty"]),
    ("Pears Pure & Gentle Soap", "HUL", "Personal Care", 50, 55, "125 g", ["soap", "bath", "glycerin"]),
    ("Lifebuoy Total 10 Soap", "HUL", "Personal Care", 35, 38, "125 g", ["soap", "bath", "hygiene"]),
    ("Dettol Original Soap", "Reckitt", "Personal Care", 40, 45, "125 g", ["soap", "bath", "hygiene"]),
    ("Cinthol Original Soap", "Godrej", "Personal Care", 42, 48, "100 g", ["soap", "bath", "fresh"]),
    ("Sunsilk Stunning Black Shine Shampoo", "HUL", "Personal Care", 180, 200, "340 ml", ["shampoo", "hair", "beauty"]),
    ("Clinic Plus Strong & Long Shampoo", "HUL", "Personal Care", 150, 165, "340 ml", ["shampoo", "hair"]),
    ("Head & Shoulders Anti-Dandruff", "P&G", "Personal Care", 195, 220, "340 ml", ["shampoo", "hair", "dandruff"]),
    ("Pantene Advanced Hair Fall Solution", "P&G", "Personal Care", 190, 215, "340 ml", ["shampoo", "hair"]),
    ("Himalaya Purifying Neem Face Wash", "Himalaya", "Personal Care", 140, 160, "150 ml", ["facewash", "skincare", "neem"]),
    ("Garnier Men Power White Face Wash", "Garnier", "Personal Care", 170, 190, "100 g", ["facewash", "skincare", "men"]),
    ("Pond's White Beauty Face Wash", "HUL", "Personal Care", 135, 155, "100 g", ["facewash", "skincare", "beauty"]),
    ("Fair & Lovely Advanced Multi Vitamin", "HUL", "Personal Care", 120, 135, "50 g", ["cream", "skincare", "beauty"]),
    ("Nivea Soft Light Moisturiser", "Nivea", "Personal Care", 160, 185, "100 ml", ["cream", "skincare", "moisturizer"]),
    ("Vaseline Intensive Care Body Lotion", "HUL", "Personal Care", 250, 285, "400 ml", ["lotion", "skincare", "body"]),
    ("Colgate Strong Teeth Toothpaste", "Colgate", "Personal Care", 110, 125, "200 g", ["toothpaste", "oral", "teeth"]),
    ("Close Up Ever Fresh Toothpaste", "HUL", "Personal Care", 95, 110, "150 g", ["toothpaste", "oral", "fresh"]),
    ("Pepsodent Germi Check Toothpaste", "HUL", "Personal Care", 100, 115, "150 g", ["toothpaste", "oral", "teeth"]),
    ("Sensodyne Fresh Gel Toothpaste", "GSK", "Personal Care", 165, 180, "75 g", ["toothpaste", "oral", "sensitive"]),
    ("Dabur Red Paste", "Dabur", "Personal Care", 105, 120, "200 g", ["toothpaste", "oral", "ayurvedic"]),

    # Cleaning & Household
    ("Surf Excel Easy Wash Detergent", "HUL", "Cleaning & Household", 120, 135, "1 kg", ["detergent", "washing", "clothes"]),
    ("Rin Detergent Powder", "HUL", "Cleaning & Household", 85, 95, "1 kg", ["detergent", "washing", "clothes"]),
    ("Tide Plus Extra Power Detergent", "P&G", "Cleaning & Household", 110, 125, "1 kg", ["detergent", "washing", "clothes"]),
    ("Ariel Matic Front Load Detergent", "P&G", "Cleaning & Household", 250, 285, "1 kg", ["detergent", "washing", "clothes"]),
    ("Vim Dishwash Bar", "HUL", "Cleaning & Household", 25, 30, "300 g", ["dishwash", "kitchen", "cleaning"]),
    ("Vim Drop Dishwash Gel", "HUL", "Cleaning & Household", 105, 120, "500 ml", ["dishwash", "kitchen", "cleaning"]),
    ("Pril Dishwash Liquid", "Jyothy Labs", "Cleaning & Household", 100, 115, "425 ml", ["dishwash", "kitchen", "cleaning"]),
    ("Harpic Power Plus Toilet Cleaner", "Reckitt", "Cleaning & Household", 165, 185, "1 L", ["cleaner", "toilet", "hygiene"]),
    ("Lizol Floor Cleaner Citrus", "Reckitt", "Cleaning & Household", 175, 195, "1 L", ["cleaner", "floor", "hygiene"]),
    ("Colin Glass & Surface Cleaner", "Reckitt", "Cleaning & Household", 95, 105, "500 ml", ["cleaner", "glass", "surface"]),
    ("Comfort Fabric Conditioner", "HUL", "Cleaning & Household", 210, 235, "860 ml", ["fabric", "conditioner", "clothes"]),
    ("Odonil Room Freshener Block", "Dabur", "Cleaning & Household", 45, 50, "50 g", ["freshener", "room", "fragrance"]),
    ("Godrej aer pocket Bathroom Fragrance", "Godrej", "Cleaning & Household", 55, 60, "10 g", ["freshener", "bathroom", "fragrance"]),
    ("All Out Ultra Mosquito Repellent Refill", "SC Johnson", "Cleaning & Household", 75, 85, "45 ml", ["repellent", "mosquito", "home"]),
    ("Good Knight Gold Flash Refill", "Godrej", "Cleaning & Household", 80, 90, "45 ml", ["repellent", "mosquito", "home"])
]

# Build JSON Data
app_data = {
    "brands": list(set([p[1] for p in indian_products])),
    "products": []
}

for idx, p in enumerate(indian_products):
    name, brand, category, price, mrp, unit, tags = p
    query = f"{brand} {name} product packaging isolated white background studio lighting"
    # Using Pollinations AI directly with URL encoding
    img_url = f"https://image.pollinations.ai/prompt/{query.replace(' ', '%20')}?width=300&height=300&nologo=true"
    
    discount = round(((mrp - price) / mrp) * 100) if mrp > price else 0
    rating = round(3.5 + (idx % 15) * 0.1, 1) # Pseudo-random rating 3.5 - 4.9
    
    product = {
        "id": str(idx + 1),
        "name": name,
        "brand": brand,
        "category": category,
        "price": price,
        "mrp": mrp,
        "discount": discount,
        "rating": str(rating),
        "reviewCount": 100 + (idx * 17) % 5000,
        "unit": unit,
        "inStock": True,
        "tags": tags,
        "image": img_url,
        "images": [img_url, img_url, img_url],
        "description": f"Buy {name} by {brand} online at best prices. High quality {category.lower()} product guaranteed to meet your everyday needs."
    }
    app_data["products"].append(product)

print("Finished building data. Writing data.js...")

js_content = f"""/* ══════════════════════════════════════════════
   FERI — Static Seed Data
   Generated with Major Indian Brands & AI Photorealistic Images
   ══════════════════════════════════════════════ */

const AppData = {json.dumps(app_data, indent=2)};

// Ensure uniqueness of brands array
AppData.brands = [...new Set(AppData.brands)];

// Helper to get products
AppData.getProducts = (options = {{}}) => {{
  let res = [...AppData.products];
  if (options.category) res = res.filter(p => p.category === options.category);
  if (options.brand) res = res.filter(p => p.brand === options.brand);
  if (options.query) {{
    const q = options.query.toLowerCase();
    res = res.filter(p => p.name.toLowerCase().includes(q) || p.brand.toLowerCase().includes(q) || p.tags.some(t => t.includes(q)));
  }}
  if (options.sort) {{
    if (options.sort === 'price_asc') res.sort((a, b) => a.price - b.price);
    else if (options.sort === 'price_desc') res.sort((a, b) => b.price - a.price);
    else if (options.sort === 'rating') res.sort((a, b) => b.rating - a.rating);
  }}
  
  if (options.limit) res = res.slice(0, options.limit);
  return res;
}};

AppData.getProductById = (id) => {{
  return AppData.products.find(p => p.id === id);
}};

console.log(`Loaded ${{AppData.products.length}} products with real Indian brands.`);
"""

with open('js/data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Done! data.js has been completely rewritten.")
