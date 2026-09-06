import os

os.makedirs('images/categories', exist_ok=True)

# 1. Grocery: Brown grocery paper bag with fresh veggies
with open('images/categories/cat_grocery.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <!-- Soft pastel circle bg -->
  <circle cx="50" cy="50" r="46" fill="#FEF3C7"/>
  <!-- Veggies peaking out -->
  <!-- Green leafy celery/lettuce -->
  <path d="M36 40 C32 28 40 22 46 28 C48 24 56 26 56 34" fill="#22C55E"/>
  <path d="M40 38 C42 26 52 24 54 32" fill="#16A34A"/>
  <!-- Orange Carrots -->
  <path d="M50 36 L58 20 L63 24 L56 38 Z" fill="#F97316"/>
  <path d="M57 20 L58 14 M60 21 L63 15 M62 23 L66 18" stroke="#22C55E" stroke-width="2" stroke-linecap="round"/>
  <!-- Red Tomato -->
  <circle cx="64" cy="40" r="8" fill="#EF4444"/>
  <path d="M64 32 L64 30 M62 31 L66 31" stroke="#15803D" stroke-width="1.5" stroke-linecap="round"/>
  <!-- Brown Paper Grocery Bag -->
  <path d="M30 42 L34 80 H66 L70 42 Z" fill="#D97706"/>
  <path d="M30 42 L32 46 H68 L70 42 Z" fill="#B45309"/>
  <!-- Bag fold lines -->
  <path d="M50 46 V80" stroke="#B45309" stroke-width="1.5" stroke-dasharray="2 2"/>
</svg>''')

# 2. Beverages: Coke bottle & Orange soda bottle
with open('images/categories/cat_beverages.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="46" fill="#E0F2FE"/>
  <!-- Red Cola Bottle -->
  <g transform="translate(32, 22)">
    <!-- Cap -->
    <rect x="7" y="0" width="8" height="5" rx="1" fill="#DC2626"/>
    <path d="M9 5 L9 12 L4 22 L4 56 C4 59 7 60 11 60 C15 60 18 59 18 56 L18 22 L13 12 L13 5 Z" fill="#991B1B"/>
    <!-- Red label -->
    <rect x="4" y="28" width="14" height="18" fill="#DC2626"/>
    <path d="M6 37 C9 35 13 39 16 36" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>
  </g>
  <!-- Orange Drink Bottle (Fanta/Mirinda) -->
  <g transform="translate(50, 26)">
    <rect x="7" y="0" width="8" height="5" rx="1" fill="#EA580C"/>
    <path d="M9 5 L9 12 L4 20 L4 52 C4 55 7 56 11 56 C15 56 18 55 18 52 L18 20 L13 12 L13 5 Z" fill="#F97316"/>
    <!-- Orange label -->
    <rect x="4" y="24" width="14" height="16" fill="#EA580C"/>
    <circle cx="11" cy="32" r="4" fill="#FDE047"/>
  </g>
</svg>''')

# 3. Snacks: Lay's Yellow Chips Bag
with open('images/categories/cat_snacks.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="46" fill="#FEF9C3"/>
  <!-- Lay's Yellow Pillow Pouch -->
  <g transform="translate(28, 20)">
    <!-- Serrated Top -->
    <path d="M4 8 L6 6 L8 8 L10 6 L12 8 L14 6 L16 8 L18 6 L20 8 L22 6 L24 8 L26 6 L28 8 L30 6 L32 8 L34 6 L36 8 L38 6 L40 8 V12 H4 V8 Z" fill="#EAB308"/>
    <!-- Bag Body -->
    <path d="M4 12 C2 30 2 45 4 58 H40 C42 45 42 30 40 12 Z" fill="#FACC15"/>
    <!-- Serrated Bottom -->
    <path d="M4 58 L6 60 L8 58 L10 60 L12 58 L14 60 L16 58 L18 60 L20 58 L22 60 L24 58 L26 60 L28 58 L30 60 L32 58 L34 60 L36 58 L38 60 L40 58 V56 H4 V58 Z" fill="#EAB308"/>
    <!-- Center Red Banner & Sun Logo -->
    <ellipse cx="22" cy="34" rx="14" ry="14" fill="#DC2626"/>
    <ellipse cx="22" cy="34" rx="10" ry="10" fill="#FACC15"/>
    <text x="22" y="37" font-family="'Outfit', sans-serif" font-size="7" font-weight="900" fill="#DC2626" text-anchor="middle">Lay's</text>
    <!-- Crispy chips graphic -->
    <ellipse cx="22" cy="48" rx="8" ry="4" fill="#FDE047" stroke="#EAB308"/>
  </g>
</svg>''')

# 4. Personal Care: Dove White Shampoo Bottle with Blue Accent
with open('images/categories/cat_personal_care.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="46" fill="#EFF6FF"/>
  <!-- Dove style elegant white bottle -->
  <g transform="translate(36, 18)">
    <!-- Blue Cap -->
    <path d="M10 0 C10 0 14 0 18 0 C20 0 20 5 20 5 H8 C8 5 8 0 10 0 Z" fill="#2563EB"/>
    <!-- Bottle Shape -->
    <path d="M8 6 H20 L24 20 C27 34 27 48 23 58 C21 62 17 64 14 64 C11 64 7 62 5 58 C1 48 1 34 4 20 Z" fill="#FFFFFF" stroke="#DBEAFE" stroke-width="1.5"/>
    <!-- Gold Bird Emblem -->
    <path d="M14 22 C16 20 20 22 21 24 C19 25 17 24 14 26 C13 25 12 23 14 22 Z" fill="#D97706"/>
    <!-- Blue Typography Wave -->
    <path d="M7 36 C10 34 18 34 21 36" stroke="#2563EB" stroke-width="1.5" stroke-linecap="round"/>
    <line x1="9" y1="42" x2="19" y2="42" stroke="#94A3B8" stroke-width="1"/>
    <line x1="11" y1="46" x2="17" y2="46" stroke="#94A3B8" stroke-width="1"/>
  </g>
</svg>''')

# 5. Home Care: Surf Excel Detergent Pouch
with open('images/categories/cat_home_care.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="46" fill="#F3E8FF"/>
  <!-- Surf Excel Pouch -->
  <g transform="translate(30, 20)">
    <!-- Top seal with handle -->
    <path d="M4 6 H36 V12 H4 Z" fill="#1E40AF"/>
    <rect x="14" y="2" width="12" height="4" rx="2" fill="#E2E8F0"/>
    <!-- Pouch Body (Blue / Pink splash) -->
    <path d="M4 12 C3 30 3 46 6 58 H34 C37 46 37 30 36 12 Z" fill="#1D4ED8"/>
    <!-- Stains burst emblem (orange/pink/green) -->
    <circle cx="20" cy="34" r="11" fill="#FFFFFF"/>
    <path d="M20 25 L22 30 L27 28 L24 33 L29 35 L24 37 L26 42 L21 39 L19 44 L18 39 L13 41 L16 36 L11 34 L16 32 L14 27 L19 29 Z" fill="#EC4899"/>
    <!-- Surf Excel text -->
    <text x="20" y="37" font-family="'Outfit', sans-serif" font-size="6" font-weight="900" fill="#1E40AF" text-anchor="middle">Surf</text>
    <rect x="8" y="46" width="24" height="4" rx="2" fill="#10B981"/>
  </g>
</svg>''')

# 6. Dairy & Breakfast: Milk Pouch & Bowl with cereal
with open('images/categories/cat_dairy.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="46" fill="#E0F2FE"/>
  <!-- Milk Pouch on Left -->
  <g transform="translate(24, 24)">
    <rect x="0" y="0" width="24" height="42" rx="3" fill="#FFFFFF" stroke="#93C5FD" stroke-width="1.5"/>
    <rect x="0" y="8" width="24" height="12" fill="#3B82F6"/>
    <text x="12" y="17" font-family="'Outfit', sans-serif" font-size="7" font-weight="800" fill="#FFFFFF" text-anchor="middle">MILK</text>
    <ellipse cx="12" cy="30" rx="6" ry="4" fill="#DBEAFE"/>
  </g>
  <!-- Bowl with cereal/butter on Right -->
  <g transform="translate(44, 42)">
    <ellipse cx="20" cy="18" rx="18" ry="8" fill="#F59E0B"/>
    <path d="M2 18 C2 28 10 34 20 34 C30 34 38 28 38 18 Z" fill="#D97706"/>
    <ellipse cx="20" cy="18" rx="15" ry="6" fill="#FEF3C7"/>
    <!-- Spoon -->
    <path d="M28 8 L36 0 L39 3 L31 11 Z" fill="#94A3B8"/>
  </g>
</svg>''')

# 7. Biscuits & Cookies: Parle-G Biscuit Packet
with open('images/categories/cat_biscuits.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="46" fill="#FFEDD5"/>
  <!-- Parle-G Yellow/White pack -->
  <g transform="translate(24, 28)">
    <rect x="0" y="0" width="52" height="36" rx="4" fill="#FACC15" stroke="#EAB308" stroke-width="1.5"/>
    <!-- Red & White diagonal strip -->
    <path d="M0 0 L16 0 L0 16 Z" fill="#DC2626"/>
    <path d="M36 36 L52 36 L52 20 Z" fill="#DC2626"/>
    <!-- Parle-G baby illustration outline -->
    <circle cx="16" cy="18" r="9" fill="#FFFFFF"/>
    <circle cx="16" cy="18" r="7" fill="#FEF08A"/>
    <!-- Parle-G Bold typography -->
    <text x="34" y="19" font-family="'Outfit', sans-serif" font-size="11" font-weight="900" fill="#B91C1C" text-anchor="middle">Parle-G</text>
    <text x="34" y="27" font-family="'Inter', sans-serif" font-size="5" font-weight="700" fill="#854D0E" text-anchor="middle">Original Gluco</text>
  </g>
</svg>''')

# 8. Pooja & Essentials: Brass Diya & Agarbatti
with open('images/categories/cat_pooja.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="46" fill="#FFF7ED"/>
  <!-- Agarbatti pack & sticks -->
  <g transform="translate(48, 22)">
    <line x1="2" y1="2" x2="20" y2="40" stroke="#78350F" stroke-width="1.5" stroke-linecap="round"/>
    <line x1="8" y1="0" x2="24" y2="40" stroke="#78350F" stroke-width="1.5" stroke-linecap="round"/>
    <line x1="14" y1="4" x2="28" y2="40" stroke="#78350F" stroke-width="1.5" stroke-linecap="round"/>
    <!-- Glowing orange tips -->
    <circle cx="2" cy="2" r="1.5" fill="#EF4444"/>
    <circle cx="8" cy="0" r="1.5" fill="#EF4444"/>
    <circle cx="14" cy="4" r="1.5" fill="#EF4444"/>
  </g>
  <!-- Brass Diya / Oil lamp -->
  <g transform="translate(26, 40)">
    <!-- Oil lamp base -->
    <path d="M4 22 C4 28 14 32 24 32 C34 32 44 28 44 22 L38 20 C32 22 16 22 10 20 Z" fill="#D97706"/>
    <ellipse cx="24" cy="20" rx="16" ry="4" fill="#F59E0B"/>
    <rect x="22" y="32" width="4" height="6" fill="#B45309"/>
    <ellipse cx="24" cy="38" rx="8" ry="3" fill="#D97706"/>
    <!-- Golden Flame -->
    <path d="M24 6 C28 12 28 18 24 20 C20 18 20 12 24 6 Z" fill="#FACC15"/>
    <path d="M24 10 C26 13 26 17 24 18 C22 17 22 13 24 10 Z" fill="#EA580C"/>
  </g>
</svg>''')

# 9. Stationery: Cup holding colorful pencils & pens
with open('images/categories/cat_stationery.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="46" fill="#E0F7FA"/>
  <!-- Pencils protruding -->
  <g transform="translate(32, 18)">
    <!-- Blue pencil -->
    <path d="M6 16 L10 0 L14 16 Z" fill="#FDE047"/>
    <polygon points="10,0 8,8 12,8" fill="#1E293B"/>
    <rect x="6" y="16" width="8" height="26" fill="#2563EB"/>
    <!-- Red pencil -->
    <path d="M18 12 L22 -4 L26 12 Z" fill="#FDE047"/>
    <polygon points="22,-4 20,4 24,4" fill="#1E293B"/>
    <rect x="18" y="12" width="8" height="30" fill="#DC2626"/>
    <!-- Green pencil -->
    <path d="M28 18 L31 4 L35 18 Z" fill="#FDE047"/>
    <polygon points="31,4 29,10 33,10" fill="#1E293B"/>
    <rect x="28" y="18" width="7" height="24" fill="#16A34A"/>
    <!-- Yellow Ruler -->
    <rect x="1" y="8" width="5" height="34" fill="#EAB308" transform="rotate(-15 1 8)"/>
  </g>
  <!-- Holder Cup -->
  <g transform="translate(35, 46)">
    <path d="M2 0 L6 32 H24 L28 0 Z" fill="#0284C7"/>
    <ellipse cx="15" cy="0" rx="13" ry="3" fill="#38BDF8"/>
  </g>
</svg>''')

# 10. More Categories: Three blue dots
with open('images/categories/cat_more.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="46" fill="#EFF6FF"/>
  <!-- Three royal blue dots -->
  <circle cx="32" cy="50" r="4.5" fill="#0052FF"/>
  <circle cx="50" cy="50" r="4.5" fill="#0052FF"/>
  <circle cx="68" cy="50" r="4.5" fill="#0052FF"/>
</svg>''')

print("All 10 category SVGs generated successfully!")
