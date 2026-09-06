import os

os.makedirs('images/brands', exist_ok=True)
os.makedirs('images/categories', exist_ok=True)
os.makedirs('images/ui', exist_ok=True)

# 1. FERI Logo SVG
with open('images/ui/feri_logo.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 48" fill="none">
  <!-- Blue Bag Icon with white handle and stylized f -->
  <g transform="translate(0, 4)">
    <path d="M12 12C12 7.58172 15.5817 4 20 4H28C32.4183 4 36 7.58172 36 12V14H40C42.2091 14 44 15.7909 44 18V36C44 38.2091 42.2091 40 40 40H8C5.79086 40 4 38.2091 4 36V18C4 15.7909 5.79086 14 8 14H12V12Z" fill="#0052FF"/>
    <path d="M16 14V12C16 9.79086 17.7909 8 20 8H28C30.2091 8 32 9.79086 32 12V14" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
    <!-- white 'f' cutout in bag -->
    <path d="M25 21C23.5 21 22 22 22 24V34" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M19 26H26" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
  </g>
  <!-- 'feri' typography in bold royal blue -->
  <text x="50" y="33" font-family="-apple-system, BlinkMacSystemFont, 'Outfit', 'Inter', sans-serif" font-size="34" font-weight="800" fill="#0052FF" letter-spacing="-0.8">feri</text>
</svg>''')

# 2. 3D Credit Wallet with floating gold coins SVG
with open('images/ui/credit_wallet.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 100" fill="none">
  <defs>
    <linearGradient id="walletBg" x1="10" y1="20" x2="80" y2="90" gradientUnits="userSpaceOnUse">
      <stop stop-color="#3B82F6"/>
      <stop offset="1" stop-color="#1D4ED8"/>
    </linearGradient>
    <linearGradient id="walletFlap" x1="10" y1="20" x2="80" y2="50" gradientUnits="userSpaceOnUse">
      <stop stop-color="#60A5FA"/>
      <stop offset="1" stop-color="#2563EB"/>
    </linearGradient>
    <linearGradient id="goldCoin1" x1="45" y1="0" x2="75" y2="35" gradientUnits="userSpaceOnUse">
      <stop stop-color="#FDE047"/>
      <stop offset="1" stop-color="#EAB308"/>
    </linearGradient>
    <linearGradient id="goldCoin2" x1="70" y1="40" x2="100" y2="75" gradientUnits="userSpaceOnUse">
      <stop stop-color="#FDE047"/>
      <stop offset="1" stop-color="#CA8A04"/>
    </linearGradient>
    <filter id="dropSh" x="0" y="0" width="120" height="100" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#1E3A8A" flood-opacity="0.25"/>
    </filter>
  </defs>

  <!-- Top Floating Gold Coin -->
  <g transform="translate(0, -2)">
    <ellipse cx="60" cy="22" rx="14" ry="14" fill="url(#goldCoin1)"/>
    <ellipse cx="60" cy="22" rx="11" ry="11" fill="#FACC15" stroke="#EAB308" stroke-width="1.5"/>
    <text x="56" y="27" font-family="'Inter', sans-serif" font-size="14" font-weight="800" fill="#854D0E">₹</text>
  </g>

  <!-- Main 3D Blue Wallet Body -->
  <g filter="url(#dropSh)">
    <rect x="15" y="32" width="75" height="52" rx="12" fill="url(#walletBg)"/>
    <!-- Wallet Flap -->
    <path d="M15 38C15 34.6863 17.6863 32 21 32H84C87.3137 32 90 34.6863 90 38V48C90 54.6274 84.6274 60 78 60H15V38Z" fill="url(#walletFlap)"/>
    <!-- Silver/Gold Snap Clasp -->
    <circle cx="78" cy="48" r="4.5" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1.5"/>
    <circle cx="78" cy="48" r="2" fill="#E2E8F0"/>
  </g>

  <!-- Bottom Front Floating Gold Coin -->
  <g transform="translate(14, 28)">
    <ellipse cx="74" cy="48" rx="15" ry="15" fill="url(#goldCoin2)"/>
    <ellipse cx="74" cy="48" rx="12" ry="12" fill="#FDE047" stroke="#CA8A04" stroke-width="1.5"/>
    <text x="69.5" y="53.5" font-family="'Inter', sans-serif" font-size="15" font-weight="800" fill="#78350F">₹</text>
  </g>
</svg>''')

# 3. 3D Shield 60-Day Risk-Free SVG
with open('images/ui/shield_60days.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 110 120" fill="none">
  <defs>
    <linearGradient id="shieldBlue" x1="10" y1="10" x2="100" y2="110" gradientUnits="userSpaceOnUse">
      <stop stop-color="#1E40AF"/>
      <stop offset="0.5" stop-color="#2563EB"/>
      <stop offset="1" stop-color="#1D4ED8"/>
    </linearGradient>
    <linearGradient id="shieldRibbon" x1="5" y1="80" x2="105" y2="80" gradientUnits="userSpaceOnUse">
      <stop stop-color="#059669"/>
      <stop offset="0.5" stop-color="#10B981"/>
      <stop offset="1" stop-color="#047857"/>
    </linearGradient>
    <filter id="shieldShadow" x="0" y="0" width="110" height="120" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#1E3A8A" flood-opacity="0.3"/>
    </filter>
  </defs>

  <g filter="url(#shieldShadow)">
    <!-- Blue Shield Path -->
    <path d="M55 8 L95 24 C95 62 76 96 55 106 C34 96 15 62 15 24 Z" fill="url(#shieldBlue)" stroke="#60A5FA" stroke-width="2"/>
    <path d="M55 14 L88 28 C88 60 72 89 55 98 C38 89 22 60 22 28 Z" fill="#1D4ED8" opacity="0.6"/>

    <!-- Stars -->
    <g fill="#FDE047" transform="translate(0, 4)">
      <path d="M55 20 L56.5 24 L61 24.5 L57.5 27.5 L58.5 32 L55 29.5 L51.5 32 L52.5 27.5 L49 24.5 L53.5 24 Z"/>
      <path d="M43 23 L44 26 L47 26.5 L44.5 28.5 L45.5 32 L43 30 L40.5 32 L41.5 28.5 L39 26.5 L42 26 Z" transform="scale(0.8) translate(10, 6)"/>
      <path d="M67 23 L68 26 L71 26.5 L68.5 28.5 L69.5 32 L67 30 L64.5 32 L65.5 28.5 L63 26.5 L66 26 Z" transform="scale(0.8) translate(22, 6)"/>
    </g>

    <!-- Center Big 60 -->
    <text x="55" y="58" font-family="'Outfit', 'Inter', sans-serif" font-size="28" font-weight="900" fill="#FFFFFF" text-anchor="middle" letter-spacing="-1">60</text>
    <text x="55" y="70" font-family="'Outfit', 'Inter', sans-serif" font-size="11" font-weight="800" fill="#93C5FD" text-anchor="middle" letter-spacing="1">DAYS</text>

    <!-- Green Ribbon -->
    <path d="M12 78 H98 L92 92 H18 Z" fill="url(#shieldRibbon)" stroke="#34D399" stroke-width="1"/>
    <text x="55" y="88.5" font-family="'Outfit', 'Inter', sans-serif" font-size="9.5" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">RISK-FREE</text>
  </g>
</svg>''')

# 4. Store Avatar SVG (New Shree Kirana storefront thumbnail)
with open('images/ui/store_avatar.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60" fill="none">
  <circle cx="30" cy="30" r="30" fill="#FEF3C7"/>
  <rect x="12" y="24" width="36" height="26" rx="2" fill="#D97706"/>
  <!-- Canopy stripes -->
  <path d="M10 24 L14 16 L20 24 L26 16 L32 24 L38 16 L44 24 L50 16 L50 24 Z" fill="#DC2626"/>
  <path d="M14 16 L20 24 L26 16 L32 24 L38 16 L44 24 L50 16" fill="#FBBF24"/>
  <!-- Door and shelves -->
  <rect x="22" y="32" width="16" height="18" fill="#F8FAFC"/>
  <rect x="26" y="32" width="8" height="18" fill="#3B82F6"/>
  <rect x="14" y="34" width="6" height="12" fill="#F59E0B"/>
  <rect x="40" y="34" width="6" height="12" fill="#10B981"/>
</svg>''')

# 5. BRAND LOGOS (High quality SVG replicas matching the screenshot)

# HUL (Unilever 25-symbol iconic U)
with open('images/brands/hul.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="48" fill="#FFFFFF"/>
  <path d="M32 26 C32 18 42 16 42 24 C42 30 36 34 36 40 C36 54 44 64 50 64 C56 64 64 54 64 40 C64 34 58 30 58 24 C58 16 68 18 68 26 C68 44 58 72 50 72 C42 72 32 44 32 26 Z" fill="#0052FF"/>
  <!-- stylized brand pattern nodes -->
  <circle cx="34" cy="22" r="3" fill="#0052FF"/>
  <circle cx="66" cy="22" r="3" fill="#0052FF"/>
  <circle cx="28" cy="36" r="3.5" fill="#0052FF"/>
  <circle cx="72" cy="36" r="3.5" fill="#0052FF"/>
  <circle cx="50" cy="68" r="4" fill="#0052FF"/>
  <circle cx="44" cy="46" r="2.5" fill="#0052FF"/>
  <circle cx="56" cy="46" r="2.5" fill="#0052FF"/>
</svg>''')

# Coca-Cola (Solid Red Circle with white signature cursive typography)
with open('images/brands/coca_cola.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="48" fill="#F40009"/>
  <!-- Classic Coca-Cola Script styling -->
  <path d="M22 54 C28 50 36 48 48 48 C44 44 42 36 50 36 C56 36 56 42 52 48 C60 48 70 45 78 42 C72 47 62 51 50 51 C54 56 62 60 70 58 C62 64 46 63 40 56 C34 57 26 60 22 54 Z" fill="#FFFFFF"/>
  <text x="50" y="55" font-family="'Brush Script MT', 'Bickham Script Pro', cursive, sans-serif" font-style="italic" font-size="20" font-weight="900" fill="#FFFFFF" text-anchor="middle">Coca-Cola</text>
</svg>''')

# PepsiCo (Iconic Pepsi Globe Red, White Wave, Blue)
with open('images/brands/pepsico.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="48" fill="#004B93"/>
  <clipPath id="circleClip">
    <circle cx="50" cy="50" r="46"/>
  </clipPath>
  <g clip-path="url(#circleClip)">
    <!-- Top red hemisphere -->
    <path d="M4 50 C16 50 28 34 50 34 C72 34 84 50 96 50 A46 46 0 0 0 4 50 Z" fill="#C9002B"/>
    <!-- Middle white wave -->
    <path d="M4 50 C16 50 28 34 50 34 C72 34 84 50 96 50 C84 62 70 66 50 66 C30 66 16 62 4 50 Z" fill="#FFFFFF"/>
    <!-- Bottom blue hemisphere -->
    <path d="M4 50 C16 62 30 66 50 66 C70 66 84 62 96 50 A46 46 0 0 1 4 50 Z" fill="#004B93"/>
  </g>
</svg>''')

# ITC (Famous Blue Triangle ITC Logo)
with open('images/brands/itc.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="48" fill="#FFFFFF"/>
  <!-- Blue Triangle -->
  <path d="M50 16 L84 74 H16 Z" fill="#004494"/>
  <path d="M50 24 L76 70 H24 Z" fill="#FFFFFF"/>
  <path d="M50 30 L70 66 H30 Z" fill="#004494"/>
  <!-- ITC Letters -->
  <text x="50" y="60" font-family="'Outfit', 'Inter', sans-serif" font-size="16" font-weight="900" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">ITC</text>
</svg>''')

# Nestlé (Blue Nest with Birds and Nestlé text)
with open('images/brands/nestle.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="48" fill="#FFFFFF"/>
  <!-- Nest and Branch -->
  <path d="M22 52 C30 52 40 58 50 58 C60 58 70 52 78 52 C72 64 58 68 50 68 C42 68 28 64 22 52 Z" fill="#005DAA"/>
  <!-- Mother Bird -->
  <path d="M36 44 C34 40 38 34 44 34 C48 34 50 38 48 42 C54 40 60 42 64 48 C56 50 48 50 40 48 Z" fill="#005DAA"/>
  <!-- 2 Chicks -->
  <circle cx="55" cy="46" r="3" fill="#005DAA"/>
  <circle cx="63" cy="47" r="2.5" fill="#005DAA"/>
  <!-- Nestlé Typography -->
  <text x="50" y="82" font-family="'Outfit', 'Inter', sans-serif" font-size="15" font-weight="800" fill="#005DAA" text-anchor="middle" letter-spacing="0.5">Nestlé</text>
</svg>''')

# Parle (Red Oval with Gold border & bold PARLE)
with open('images/brands/parle.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="48" fill="#FFFFFF"/>
  <rect x="10" y="26" width="80" height="48" rx="24" fill="#D32F2F" stroke="#F59E0B" stroke-width="2"/>
  <text x="50" y="58" font-family="'Outfit', 'Inter', sans-serif" font-size="20" font-weight="900" fill="#FFFFFF" text-anchor="middle" letter-spacing="2">PARLE</text>
</svg>''')

# Britannia (Red Banner with white bold BRITANNIA)
with open('images/brands/britannia.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="48" fill="#FFFFFF"/>
  <path d="M12 34 C12 30 16 26 20 26 H80 C84 26 88 30 88 34 V60 C88 64 84 68 80 68 H50 L46 74 L42 68 H20 C16 68 12 64 12 60 Z" fill="#D32F2F"/>
  <path d="M46 72 C48 68 52 68 54 72" stroke="#10B981" stroke-width="3" stroke-linecap="round"/>
  <text x="50" y="52" font-family="'Outfit', 'Inter', sans-serif" font-size="11.5" font-weight="900" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">BRITANNIA</text>
</svg>''')

# Amul (Amul iconic red logo)
with open('images/brands/amul.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="48" fill="#FFFFFF"/>
  <circle cx="50" cy="50" r="42" fill="#FFF5F5" stroke="#EF4444" stroke-width="1.5"/>
  <text x="50" y="58" font-family="'Outfit', 'Inter', sans-serif" font-size="26" font-weight="900" fill="#DC2626" text-anchor="middle" letter-spacing="-0.5">Amul</text>
  <text x="50" y="70" font-family="'Inter', sans-serif" font-size="7" font-weight="700" fill="#7F1D1D" text-anchor="middle" letter-spacing="0.5">The Taste of India</text>
</svg>''')

# Dabur (Banyan Tree Logo in Green)
with open('images/brands/dabur.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="48" fill="#FFFFFF"/>
  <!-- Green Banyan Tree -->
  <path d="M50 20 C42 20 36 28 38 36 C30 38 26 46 30 52 C32 58 40 60 46 60 V70 H54 V60 C60 60 68 58 70 52 C74 46 70 38 62 36 C64 28 58 20 50 20 Z" fill="#15803D"/>
  <text x="50" y="84" font-family="'Outfit', 'Inter', sans-serif" font-size="14" font-weight="900" fill="#166534" text-anchor="middle" letter-spacing="0.5">Dabur</text>
</svg>''')

# Tata (Blue Oval with iconic T)
with open('images/brands/tata.svg', 'w', encoding='utf-8') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <circle cx="50" cy="50" r="48" fill="#FFFFFF"/>
  <ellipse cx="50" cy="44" rx="32" ry="24" fill="#00529B"/>
  <!-- Iconic T split lines -->
  <path d="M46 32 C46 38 43 48 36 54 M54 32 C54 38 57 48 64 54 M50 32 V56" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
  <text x="50" y="82" font-family="'Outfit', 'Inter', sans-serif" font-size="14" font-weight="900" fill="#00529B" text-anchor="middle" letter-spacing="2">TATA</text>
</svg>''')

print("Assets created successfully!")
