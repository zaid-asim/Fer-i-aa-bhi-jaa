/* ══════════════════════════════════════════════
   FERI — Main Application Logic
   ══════════════════════════════════════════════ */

const App = (() => {
  const $content = document.getElementById('pageContent');
  
  // ── Utils ──────────────────────────────────────
  function formatMoney(amount) {
    return '₹' + amount.toLocaleString('en-IN');
  }

  function getStars(rating) {
    const full = Math.floor(rating);
    const hasHalf = rating - full >= 0.5;
    let html = '';
    for(let i=0; i<5; i++) {
      if(i < full) html += '<i class="fas fa-star star"></i>';
      else if(i === full && hasHalf) html += '<i class="fas fa-star-half-alt star"></i>';
      else html += '<i class="far fa-star star empty"></i>';
    }
    return html;
  }

  // ── UI Updaters ────────────────────────────────
  function updateBadges() {
    const count = Store.getCartCount();
    const cartBadge = document.getElementById('cartBadge');
    const bnavCartBadge = document.getElementById('bnavCartBadge');
    if (cartBadge) {
      cartBadge.textContent = count;
      cartBadge.style.display = count > 0 ? 'flex' : 'none';
    }
    if (bnavCartBadge) {
      bnavCartBadge.textContent = count;
      bnavCartBadge.style.display = count > 0 ? 'flex' : 'none';
    }

    const state = Store.get();
    const wCount = (state && state.wishlist) ? state.wishlist.length : 0;
    const wBadge = document.getElementById('wishlistBadge');
    if (wBadge) {
      wBadge.textContent = wCount;
      wBadge.style.display = wCount > 0 ? 'flex' : 'none';
    }
  }

  // ── Theme Management ───────────────────────────
  function applyTheme() {
    const isDark = Store.get().user.preferences.dark;
    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
    const icon = document.getElementById('themeIcon');
    if (icon) {
      icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    }
  }

  window.toggleTheme = function() {
    playSound('toggle');
    const current = Store.get().user.preferences.dark;
    Store.updatePreference('dark', !current);
    applyTheme();
  };

  // ── Top Nav Management ─────────────────────────
  function setTopNav(title = null, showSearch = true) {
    const homeNavBar = document.getElementById('homeNavBar');
    const detailNavBar = document.getElementById('detailNavBar');
    const backBtn = document.getElementById('navBack');
    const pageTitle = document.getElementById('pageTitle');
    
    if (title) {
      if (homeNavBar) homeNavBar.style.display = 'none';
      if (detailNavBar) detailNavBar.style.display = 'flex';
      if (pageTitle) pageTitle.textContent = title;
      if (backBtn) backBtn.onclick = () => { playSound('nav'); window.history.back(); };
    } else {
      if (homeNavBar) homeNavBar.style.display = 'flex';
      if (detailNavBar) detailNavBar.style.display = 'none';
    }
  }

  // ── Toast System ───────────────────────────────
  window.showToast = function(title, msg = '', type = 'success') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'fa-check-circle';
    if(type === 'error') icon = 'fa-exclamation-circle';
    if(type === 'info') icon = 'fa-info-circle';
    
    toast.innerHTML = `
      <div class="toast-icon"><i class="fas ${icon}"></i></div>
      <div class="toast-body">
        <div class="toast-title">${title}</div>
        ${msg ? `<div class="toast-msg">${msg}</div>` : ''}
      </div>
      <div class="toast-close" onclick="this.parentElement.classList.add('out'); setTimeout(() => this.parentElement.remove(), 300);"><i class="fas fa-times"></i></div>
    `;
    
    container.appendChild(toast);
    playSound('notification');
    
    setTimeout(() => {
      if(toast.parentElement) {
        toast.classList.add('out');
        setTimeout(() => toast.remove(), 300);
      }
    }, 3000);
  };

  // ── Shared Renderers ───────────────────────────
  function renderProductCard(p) {
    const isWished = Store.isInWishlist(p.id);
    const hasDiscount = p.discount > 0;
    
    return `
      <div class="product-card reveal" onclick="navigateTo('/product/${p.id}'); playSound('click')">
        <div class="product-card-img-wrap">
          ${hasDiscount ? `<div class="product-card-discount">${p.discount}% OFF</div>` : ''}
          <button class="product-card-wishlist ${isWished ? 'active' : ''}" onclick="event.stopPropagation(); toggleWishlistEvent('${p.id}', this)" aria-label="Wishlist" data-nosound="true">
            <i class="${isWished ? 'fas' : 'far'} fa-heart"></i>
          </button>
          <img data-src="${p.image}" class="lazy-img" alt="${p.name}">
          ${!p.inStock ? `<div class="out-of-stock-overlay">Out of Stock</div>` : ''}
        </div>
        <div class="product-card-body">
          <div class="product-brand">${p.brand}</div>
          <div class="product-name">${p.name}</div>
          <div class="product-unit">${p.unit}</div>
          <div class="stars">
            ${getStars(p.rating)} <span class="rating-text">(${p.reviewCount || p.ratingCount || 100})</span>
          </div>
        </div>
        <div class="product-card-footer">
          <div class="price-block">
            <span class="price-current">${formatMoney(p.price)}</span>
            ${hasDiscount ? `<span class="price-mrp">${formatMoney(p.mrp)}</span>` : ''}
          </div>
          <button class="btn-icon btn-primary" onclick="event.stopPropagation(); addToCartEvent('${p.id}', this)" ${!p.inStock ? 'disabled' : ''} aria-label="Add to cart" data-nosound="true">
            <i class="fas fa-plus"></i>
          </button>
        </div>
      </div>
    `;
  }

  // Global event handlers for product cards
  window.addToCartEvent = function(id, btnEl) {
    playSound('addToCart');
    Store.addToCart(id, 1);
    popBadge(document.getElementById('bnavCartBadge'));
    showToast('Added to Cart', '', 'success');
    
    // Add ripple directly to the button
    const ripple = document.createElement('span');
    ripple.className = 'ripple-effect';
    ripple.style.left = '20px';
    ripple.style.top = '20px';
    btnEl.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  };

  window.toggleWishlistEvent = function(id, btnEl) {
    playSound('wishlist');
    const isAdded = Store.toggleWishlist(id);
    const icon = btnEl.querySelector('i');
    if (isAdded) {
      btnEl.classList.add('active');
      icon.className = 'fas fa-heart animate-bouncein';
      showToast('Added to Wishlist');
    } else {
      btnEl.classList.remove('active');
      icon.className = 'far fa-heart';
      showToast('Removed from Wishlist', '', 'info');
    }
  };

  window.addToCartDirect = function(id) {
    playSound('addToCart');
    Store.addToCart(id, 1);
    const badge = document.getElementById('bnavCartBadge');
    if (badge) popBadge(badge);
    showToast('Added to Cart', 'Item added to your shopping bag', 'success');
  };

  window.repeatOrderEvent = function(orderId) {
    playSound('orderSuccess');
    ['p21', 'p59', 'p20', 'p32'].forEach(id => Store.addToCart(id, 2));
    showToast('Order Re-added!', '12 items from Order #' + orderId + ' added to cart', 'success');
    setTimeout(() => navigateTo('/cart'), 700);
  };

  // ── Pages ──────────────────────────────────────

  const Pages = {
    
    // 🏠 HOME
    home: () => {
      setTopNav(null, true);
      
      const dealsList = [
        { id: "p86", name: "Fortune Sunlite Refined Oil 1L", brand: "Fortune", price: 135, mrp: 159, discount: 15, image: "images/products/p86.jpg" },
        { id: "p54", name: "Aashirvaad Atta 5kg", brand: "ITC", price: 249, mrp: 279, discount: 10, image: "images/products/p54.jpg" },
        { id: "p72", name: "Tata Tea Premium 1kg", brand: "Tata", price: 435, mrp: 475, discount: 8, image: "images/products/p72.jpg" },
        { id: "p6", name: "Britannia Good Day Cookies", brand: "Britannia", price: 55, mrp: 60, discount: 12, image: "images/products/p6.jpg" },
        { id: "p11", name: "Amul Butter Pasteurised", brand: "Amul", price: 259, mrp: 270, discount: 10, image: "images/products/p11.jpg" },
        { id: "p42", name: "Surf Excel Easy Wash 1kg", brand: "HUL", price: 315, mrp: 360, discount: 15, image: "images/products/p42.jpg" },
        { id: "p60", name: "Maggi Masala Noodles 4-Pack", brand: "Nestle", price: 55, mrp: 60, discount: 10, image: "images/products/p60.jpg" },
        { id: "p30", name: "Lay's Magic Masala Chips", brand: "PepsiCo", price: 30, mrp: 35, discount: 15, image: "images/products/p30.jpg" }
      ];

      const categoriesList = [
        { name: "Grocery", icon: "images/categories/cat_grocery.svg", bg: "#FEF3C7" },
        { name: "Beverages", icon: "images/categories/cat_beverages.svg", bg: "#E0F2FE" },
        { name: "Snacks", icon: "images/categories/cat_snacks.svg", bg: "#FEF9C3" },
        { name: "Personal Care", icon: "images/categories/cat_personal_care.svg", bg: "#EFF6FF" },
        { name: "Home Care", icon: "images/categories/cat_home_care.svg", bg: "#F3E8FF" },
        { name: "Dairy & Breakfast", icon: "images/categories/cat_dairy.svg", bg: "#E0F2FE" },
        { name: "Biscuits & Cookies", icon: "images/categories/cat_biscuits.svg", bg: "#FFEDD5" },
        { name: "Pooja & Essentials", icon: "images/categories/cat_pooja.svg", bg: "#FFF7ED" },
        { name: "Stationery", icon: "images/categories/cat_stationery.svg", bg: "#E0F7FA" },
        { name: "More Categories", icon: "images/categories/cat_more.svg", bg: "#EFF6FF" }
      ];

      const brandsList = [
        { name: "HUL", logo: "images/brands/hul.svg", count: "1,250+ Products", pill: "5% OFF", pillType: "green" },
        { name: "Coca-Cola", logo: "images/brands/coca_cola.svg", count: "980+ Products", pill: "New Launch", pillType: "red" },
        { name: "PepsiCo", logo: "images/brands/pepsico.svg", count: "1,100+ Products", pill: "5% OFF", pillType: "green" },
        { name: "ITC", logo: "images/brands/itc.svg", count: "850+ Products", pill: null },
        { name: "Nestle", logo: "images/brands/nestle.svg", count: "920+ Products", pill: "New Launch", pillType: "red" },
        { name: "Parle", logo: "images/brands/parle.svg", count: "1,100+ Products", pill: "5% OFF", pillType: "green" },
        { name: "Britannia", logo: "images/brands/britannia.svg", count: "1,050+ Products", pill: null },
        { name: "Amul", logo: "images/brands/amul.svg", count: "850+ Products", pill: "5% OFF", pillType: "green" },
        { name: "Dabur", logo: "images/brands/dabur.svg", count: "720+ Products", pill: null },
        { name: "Tata", logo: "images/brands/tata.svg", count: "960+ Products", pill: "5% OFF", pillType: "green" }
      ];

      let html = `
        <div class="home-page-screen">
          
          <!-- 1. Search Bar -->
          <div class="home-search-wrap">
            <div class="search-pill-container" onclick="navigateTo('/search'); playSound('click')">
              <i class="fas fa-search search-icon-left"></i>
              <div class="search-placeholder-text">Search products, brands or categories</div>
              <button class="barcode-scan-btn" onclick="event.stopPropagation(); showToast('Barcode Scanner', 'Ready to scan FMCG pack barcodes', 'info'); playSound('click')" aria-label="Scan barcode">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0052FF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 7V5a2 2 0 0 1 2-2h2"/>
                  <path d="M17 3h2a2 2 0 0 1 2 2v2"/>
                  <path d="M21 17v2a2 2 0 0 1-2 2h-2"/>
                  <path d="M7 21H5a2 2 0 0 1-2-2v-2"/>
                  <circle cx="12" cy="12" r="1.5" fill="#0052FF"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- 2. Available Credit Banner Card -->
          <div class="credit-banner-card">
            <div class="credit-left-col">
              <span class="credit-sub-label">Available Credit</span>
              <div class="credit-amount-title">₹50,000</div>
              <div class="credit-limit-text">of ₹50,000</div>
              <a href="#/profile" class="credit-details-link" onclick="playSound('click')">
                View Details <i class="fas fa-chevron-right text-xs"></i>
              </a>
            </div>

            <div class="credit-center-graphic">
              <img src="images/ui/credit_wallet.svg" alt="Credit Wallet" class="credit-wallet-img">
            </div>

            <div class="credit-right-col">
              <div class="credit-stat-item">
                <span class="stat-muted">Used</span>
                <span class="stat-val">₹0</span>
              </div>
              <div class="credit-stat-item">
                <span class="stat-muted">Remaining</span>
                <span class="stat-val">₹50,000</span>
              </div>
              <button class="shop-credit-btn" onclick="showToast('Credit Applied', '₹50,000 credit limit ready for checkout', 'success'); playSound('click'); navigateTo('/products');">
                Shop on Credit
              </button>
            </div>
          </div>

          <!-- 3. Shop by Category -->
          <div class="home-section-container">
            <div class="home-section-heading">
              <h3 class="section-title-main">Shop by Category</h3>
              <a href="#/search" class="section-view-all-link" onclick="playSound('click')">View All</a>
            </div>

            <div class="category-grid-10">
              ${categoriesList.map(cat => `
                <div class="category-grid-item" onclick="navigateTo('/products?category=' + encodeURIComponent('${cat.name}')); playSound('click')">
                  <div class="category-circle-avatar" style="background: ${cat.bg}">
                    <img src="${cat.icon}" alt="${cat.name}" class="category-icon-img">
                  </div>
                  <span class="category-label-text">${cat.name}</span>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- 4. Shop by Brand (Highlighted in screenshot) -->
          <div class="home-section-container brand-section-box">
            <div class="home-section-heading">
              <h3 class="section-title-main">Shop by Brand</h3>
              <a href="#/brands" class="section-view-all-link" onclick="playSound('click')">View All</a>
            </div>

            <div class="brand-horizontal-scroll-wrap">
              <div class="brand-hscroll" id="brandHScroll">
                ${brandsList.map(b => `
                  <div class="brand-card-item" onclick="navigateTo('/products?brand=' + encodeURIComponent('${b.name}')); playSound('click')">
                    <div class="brand-logo-circle">
                      <img src="${b.logo}" alt="${b.name}" class="brand-logo-img">
                    </div>
                    <div class="brand-name-title">${b.name}</div>
                    <div class="brand-product-count">${b.count}</div>
                    ${b.pill ? `
                      <div class="brand-promo-pill ${b.pillType === 'red' ? 'pill-red' : 'pill-green'}">
                        ${b.pill}
                      </div>
                    ` : '<div class="brand-promo-spacer"></div>'}
                  </div>
                `).join('')}
              </div>
              <button class="brand-scroll-arrow-btn" onclick="document.getElementById('brandHScroll').scrollBy({left: 180, behavior: 'smooth'}); playSound('click')">
                <i class="fas fa-chevron-right"></i>
              </button>
            </div>
          </div>

          <!-- 5. 60-Day Risk-Free Trial Banner -->
          <div class="risk-free-banner-card">
            <div class="risk-free-left">
              <div class="risk-free-title-badge">60-DAY RISK-FREE TRIAL</div>
              <p class="risk-free-desc">Try new brands. If not satisfied, return and get equal value products.</p>
              <button class="risk-free-explore-btn" onclick="navigateTo('/products'); playSound('click')">
                Explore Now
              </button>
            </div>
            
            <div class="risk-free-right">
              <!-- Golden sparkles -->
              <span class="sparkle sp-1">✦</span>
              <span class="sparkle sp-2">✦</span>
              <!-- Left packshot (Fortune Oil) -->
              <img src="images/products/p86.jpg" alt="Fortune Oil" class="shield-product-left">
              <!-- Center 3D Shield -->
              <img src="images/ui/shield_60days.svg" alt="60 Days Risk Free" class="shield-graphic-center">
              <!-- Right packshot (Namkeen) -->
              <img src="images/products/p66.jpg" alt="Namkeen" class="shield-product-right">
            </div>
          </div>

          <!-- 6. Repeat Last Order -->
          <div class="home-section-container">
            <div class="home-section-heading">
              <h3 class="section-title-main">Repeat Last Order</h3>
              <a href="#/orders" class="section-view-all-link" onclick="playSound('click')">View All Orders</a>
            </div>

            <div class="repeat-order-card">
              <div class="repeat-order-top-row">
                <div class="repeat-order-info">
                  <div class="repeat-order-id">Order #12345</div>
                  <div class="repeat-order-date">Delivered on 20 May, 2024</div>
                  <div class="repeat-order-summary">12 Items • ₹4,560</div>
                </div>
                <button class="repeat-order-btn" onclick="repeatOrderEvent('12345'); playSound('click')">
                  <i class="fas fa-redo"></i> Order Again
                </button>
              </div>

              <div class="repeat-order-thumbs-row">
                <div class="order-thumb-box"><img src="images/products/p21.jpg" alt="Maaza"></div>
                <div class="order-thumb-box"><img src="images/products/p59.jpg" alt="Maggi"></div>
                <div class="order-thumb-box"><img src="images/products/p20.jpg" alt="Sprite"></div>
                <div class="order-thumb-box"><img src="images/products/p32.jpg" alt="Kurkure"></div>
                <div class="order-more-badge">+8</div>
              </div>
            </div>
          </div>

          <!-- 7. Best Deals for You -->
          <div class="home-section-container">
            <div class="home-section-heading">
              <h3 class="section-title-main">Best Deals for You</h3>
              <a href="#/products" class="section-view-all-link" onclick="playSound('click')">View All</a>
            </div>

            <div class="deals-horizontal-scroll">
              ${dealsList.map(item => `
                <div class="deal-product-card" onclick="navigateTo('/product/${item.id}'); playSound('click')">
                  <div class="deal-discount-badge">${item.discount}% OFF</div>
                  <div class="deal-product-img-wrap">
                    <img src="${item.image}" alt="${item.name}" class="deal-product-img">
                  </div>
                  <div class="deal-product-name line-clamp-2">${item.name}</div>
                  <div class="deal-price-row">
                    <span class="deal-price-current">₹${item.price}</span>
                    <span class="deal-price-mrp">₹${item.mrp}</span>
                  </div>
                  <button class="deal-add-btn" onclick="event.stopPropagation(); addToCartDirect('${item.id}');" aria-label="Add to cart">
                    <i class="fas fa-plus"></i>
                  </button>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- 8. Trust Badges Row -->
          <div class="trust-badges-row">
            <div class="trust-badge-item">
              <div class="trust-badge-icon">
                <i class="fas fa-truck"></i>
              </div>
              <div class="trust-badge-content">
                <strong class="trust-badge-title">Free Delivery</strong>
                <span class="trust-badge-sub">On orders above ₹999</span>
              </div>
            </div>

            <div class="trust-badge-item">
              <div class="trust-badge-icon">
                <i class="fas fa-stopwatch"></i>
              </div>
              <div class="trust-badge-content">
                <strong class="trust-badge-title">Fast Delivery</strong>
                <span class="trust-badge-sub">Within 24-48 hours</span>
              </div>
            </div>

            <div class="trust-badge-item">
              <div class="trust-badge-icon">
                <i class="fas fa-sync-alt"></i>
              </div>
              <div class="trust-badge-content">
                <strong class="trust-badge-title">Easy Returns</strong>
                <span class="trust-badge-sub">Hassle-free returns</span>
              </div>
            </div>
          </div>

          <!-- Bottom spacing -->
          <div style="height: 36px;"></div>

        </div>
      `;
      $content.innerHTML = html;
      setupLazyImages();
    },

    // 🔍 SEARCH
    search: () => {
      setTopNav('Search', false);
      const recents = Store.get().recentSearches;
      
      let html = `
        <div class="search-page">
          <div class="search-page-header">
            <div class="search-input-wrap">
              <i class="fas fa-search search-icon"></i>
              <input type="text" id="searchInput" class="form-input search-input" placeholder="Search products, brands, categories..." autocomplete="off">
              <div class="search-clear hidden" id="searchClear"><i class="fas fa-times"></i></div>
              <div class="search-voice" onclick="playSound('click'); showToast('Voice Search', 'Microphone permission required', 'info')"><i class="fas fa-microphone"></i></div>
            </div>
          </div>

          <div id="searchContent">
            <!-- Pre-search view -->
            <div class="search-chips-section reveal">
              ${recents.length > 0 ? `
                <div class="search-chips-title">Recent Searches</div>
                <div class="search-chips" style="margin-bottom:var(--sp-5)">
                  ${recents.map(q => `<div class="search-chip recent" onclick="document.getElementById('searchInput').value='${q}'; document.getElementById('searchInput').dispatchEvent(new Event('input'))"><i class="fas fa-history"></i> ${q}</div>`).join('')}
                </div>
              ` : ''}
              
              <div class="search-chips-title">Trending</div>
              <div class="search-chips">
                ${['Amul Milk', 'Maggi Noodles', 'Dove Soap', 'Lays', 'Aashirvaad Atta'].map(q => `<div class="search-chip trending" onclick="document.getElementById('searchInput').value='${q}'; document.getElementById('searchInput').dispatchEvent(new Event('input'))"><i class="fas fa-fire"></i> ${q}</div>`).join('')}
              </div>
            </div>
          </div>
        </div>
      `;
      
      $content.innerHTML = html;
      const input = document.getElementById('searchInput');
      const clearBtn = document.getElementById('searchClear');
      const content = document.getElementById('searchContent');
      
      setTimeout(() => input.focus(), 100);

      let debounceTimer;
      input.addEventListener('input', (e) => {
        const val = e.target.value.trim();
        if (val) {
          clearBtn.classList.remove('hidden');
        } else {
          clearBtn.classList.add('hidden');
        }
        
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
          if (!val) {
            // Restore pre-search view (requires re-render, skipping for brevity, handled by navigating to /search again)
            navigateTo('/search');
            return;
          }
          
          Store.addRecentSearch(val);
          const results = AppData.getProducts({ query: val });
          
          if (results.length === 0) {
            content.innerHTML = `
              <div class="empty-state reveal">
                <i class="fas fa-search empty-state-icon text-muted"></i>
                <h3>No results found</h3>
                <p>We couldn't find anything matching "${val}". Try checking your spelling or using more general terms.</p>
              </div>
            `;
          } else {
            content.innerHTML = `
              <div class="search-results-section reveal">
                <div class="search-results-header">
                  <div class="search-count">${results.length} results found</div>
                </div>
                <div class="product-grid stagger-children">
                  ${results.map(p => renderProductCard(p)).join('')}
                </div>
              </div>
            `;
            setupLazyImages();
          }
        }, 300);
      });
      
      clearBtn.addEventListener('click', () => {
        input.value = '';
        input.dispatchEvent(new Event('input'));
        input.focus();
      });
    },

    // 📦 PRODUCTS
    products: (req) => {
      const qCategory = req.query.category;
      const qBrand = req.query.brand;
      const title = qCategory || qBrand || 'All Products';
      setTopNav(title, true);

      const products = AppData.getProducts({ category: qCategory, brand: qBrand });
      
      let html = `
        <div class="products-page">
          <div class="filter-bar stagger-children">
            <div class="filter-chip ${!qCategory ? 'active' : ''}" onclick="navigateTo('/products')">All</div>
            ${AppData.categories.slice(0, 10).map(c => `
              <div class="filter-chip ${c === qCategory ? 'active' : ''}" onclick="navigateTo('/products?category=${encodeURIComponent(c)}')">${c}</div>
            `).join('')}
          </div>
          
          <div class="products-toolbar reveal">
            <div class="products-toolbar-inner">
              <div class="products-count">${products.length} Items</div>
              <div class="toolbar-actions">
                <div class="sort-dropdown">
                  <select class="sort-select" id="sortSelect">
                    <option value="relevance">Relevance</option>
                    <option value="price_asc">Price: Low to High</option>
                    <option value="price_desc">Price: High to Low</option>
                    <option value="rating">Rating</option>
                  </select>
                </div>
                <div class="view-toggle">
                  <div class="view-btn active" id="gridBtn"><i class="fas fa-th-large"></i></div>
                  <div class="view-btn" id="listBtn"><i class="fas fa-list"></i></div>
                </div>
              </div>
            </div>
          </div>
          
          ${products.length === 0 ? `
            <div class="products-empty reveal">
              <i class="fas fa-box-open empty-state-icon text-muted"></i>
              <h3>No products found</h3>
            </div>
          ` : `
            <div class="product-grid stagger-children" id="productGrid">
              ${products.map(p => renderProductCard(p)).join('')}
            </div>
          `}
        </div>
      `;
      $content.innerHTML = html;
      setupLazyImages();

      // View toggle logic
      const gridBtn = document.getElementById('gridBtn');
      const listBtn = document.getElementById('listBtn');
      const grid = document.getElementById('productGrid');
      
      if(gridBtn && listBtn && grid) {
        gridBtn.onclick = () => {
          playSound('click');
          gridBtn.classList.add('active');
          listBtn.classList.remove('active');
          grid.parentElement.classList.remove('product-list');
        };
        listBtn.onclick = () => {
          playSound('click');
          listBtn.classList.add('active');
          gridBtn.classList.remove('active');
          grid.parentElement.classList.add('product-list');
        };
      }
      
      // Sort logic
      const sortSelect = document.getElementById('sortSelect');
      if(sortSelect) {
        sortSelect.onchange = (e) => {
          const val = e.target.value;
          const sorted = AppData.getProducts({ category: qCategory, brand: qBrand, sort: val });
          grid.innerHTML = sorted.map(p => renderProductCard(p)).join('');
          setupLazyImages();
          ScrollReveal.observe(grid);
        };
      }
    },

    // 🏷️ PRODUCT DETAIL
    productDetail: (req) => {
      setTopNav('Product Details', false);
      const p = AppData.getProductById(req.params.id);
      if(!p) return Router.navigate('/404');

      Store.addRecentlyViewed(p.id);
      const isWished = Store.isInWishlist(p.id);

      let html = `
        <div class="product-detail">
          <div class="product-gallery reveal">
            ${p.discount > 0 ? `<div class="product-card-discount" style="z-index:2">${p.discount}% OFF</div>` : ''}
            <img src="${p.image}" class="product-gallery-main" id="pdMainImg" alt="${p.name}">
            <div class="product-gallery-thumbs">
              ${(p.images || [p.image]).map((img, i) => `
                <img src="${img}" class="product-gallery-thumb ${i===0?'active':''}" onclick="document.getElementById('pdMainImg').src='${img}'; document.querySelectorAll('.product-gallery-thumb').forEach(t=>t.classList.remove('active')); this.classList.add('active'); playSound('click')">
              `).join('')}
            </div>
          </div>

          <div class="product-detail-body reveal reveal-delay-1">
            <div class="product-detail-brand">${p.brand}</div>
            <h1 class="product-detail-name">${p.name}</h1>
            <div class="product-detail-meta">
              <div class="stars">${getStars(p.rating)}</div>
              <span class="text-muted text-sm">${p.rating} (${p.reviewCount || p.ratingCount || 100} reviews)</span>
              <span class="badge badge-primary">${p.unit}</span>
              ${p.inStock ? '<span class="badge badge-success">In Stock</span>' : '<span class="badge badge-danger">Out of Stock</span>'}
            </div>
            
            <p class="product-detail-desc">${p.description}</p>
            
            <div class="bulk-pricing-table">
              <table>
                <tr><th>Quantity</th><th>Price per item</th></tr>
                <tr><td>1 - 9</td><td>${formatMoney(p.price)}</td></tr>
                <tr><td>10 - 49</td><td>${formatMoney(Math.floor(p.price * 0.95))} <span class="text-primary text-sm">(5% OFF)</span></td></tr>
                <tr><td>50+</td><td>${formatMoney(Math.floor(p.price * 0.90))} <span class="text-primary text-sm">(10% OFF)</span></td></tr>
              </table>
            </div>
          </div>

          <div class="reviews-section reveal reveal-delay-2 section-bg-alt">
            <h3 class="section-title" style="margin-bottom:var(--sp-4)">Customer Reviews</h3>
            ${[1,2,3].map(i => `
              <div class="review-card">
                <div class="review-header">
                  <div class="review-author">Customer ${Math.floor(Math.random()*9000+1000)}</div>
                  <div class="stars">${getStars(5 - Math.floor(Math.random()*2))}</div>
                </div>
                <div class="review-body">Great product, fresh packaging and fast delivery by Feri. Will definitely order again!</div>
                <div class="review-date" style="margin-top:8px">${Math.floor(Math.random()*28+1)} May 2026</div>
              </div>
            `).join('')}
          </div>

          <div class="related-section reveal reveal-delay-3">
            <h3 class="section-title" style="margin-bottom:var(--sp-4)">Similar Products</h3>
            <div class="hscroll stagger-children">
              ${AppData.getProducts({ category: p.category, limit: 6 }).filter(rp => rp.id !== p.id).map(rp => `
                <div class="trending-card" onclick="navigateTo('/product/${rp.id}')">
                  <img data-src="${rp.image}" class="lazy-img trending-card-img" alt="${rp.name}">
                  <div class="trending-card-body">
                    <div class="trending-card-brand">${rp.brand}</div>
                    <div class="trending-card-name line-clamp-2">${rp.name}</div>
                    <div class="trending-card-price">${formatMoney(rp.price)}</div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- Sticky CTA -->
          <div class="product-detail-cta">
            <div class="product-price-block">
              <div class="product-detail-price">${formatMoney(p.price)}</div>
              ${p.discount > 0 ? `<div class="text-sm text-muted" style="text-decoration:line-through">MRP: ${formatMoney(p.mrp)}</div>` : ''}
            </div>
            
            <button class="btn-icon btn-surface" id="pdWishlistBtn" onclick="toggleWishlistEvent('${p.id}', this)">
              <i class="${isWished ? 'fas animate-bouncein text-danger' : 'far'} fa-heart"></i>
            </button>
            
            <button class="btn btn-primary flex-1" id="pdAddBtn" ${!p.inStock ? 'disabled' : ''}>
              <i class="fas fa-shopping-cart"></i> Add to Cart
            </button>
          </div>
          
          <div style="height:20px;"></div>
        </div>
      `;
      $content.innerHTML = html;
      setupLazyImages();

      // Add to Cart logic
      const btn = document.getElementById('pdAddBtn');
      if (btn) {
        btn.onclick = () => {
          playSound('addToCart');
          Store.addToCart(p.id, 1);
          popBadge(document.getElementById('bnavCartBadge'));
          
          btn.innerHTML = '<i class="fas fa-check"></i> Added';
          btn.style.background = 'var(--clr-primary-dark)';
          setTimeout(() => {
            btn.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
            btn.style.background = '';
          }, 2000);
          
          showToast('Added to Cart', p.name);
        };
      }
    },

    // 🛒 CART
    cart: () => {
      setTopNav('Your Cart', false);
      const items = Store.getCartItems();
      const totals = Store.getCartTotals();

      if (items.length === 0) {
        $content.innerHTML = `
          <div class="cart-empty reveal">
            <i class="fas fa-shopping-bag empty-state-icon" style="color:var(--clr-primary-light); opacity:1; font-size:100px;"></i>
            <h3 style="margin-top:20px">Your cart is empty</h3>
            <p style="margin-bottom:24px">Looks like you haven't added anything to your cart yet.</p>
            <button class="btn btn-primary" onclick="navigateTo('/home')">Start Shopping</button>
          </div>
        `;
        return;
      }

      let html = `
        <div class="cart-page">
          <div class="cart-items-list stagger-children">
            ${items.map(item => `
              <div class="cart-item" id="cart-item-${item.productId}">
                <img src="${item.product.image}" class="cart-item-img" alt="${item.product.name}">
                <div class="cart-item-body">
                  <div class="cart-item-brand">${item.product.brand}</div>
                  <div class="cart-item-name truncate">${item.product.name}</div>
                  <div class="cart-item-unit">${item.product.unit}</div>
                  <div class="cart-item-actions">
                    <div class="qty-stepper">
                      <div class="qty-btn" onclick="updateCartQty('${item.productId}', ${item.qty - 1})">-</div>
                      <div class="qty-display">${item.qty}</div>
                      <div class="qty-btn" onclick="updateCartQty('${item.productId}', ${item.qty + 1})">+</div>
                    </div>
                    <div style="text-align:right">
                      <div class="font-bold text-primary">${formatMoney(item.product.price * item.qty)}</div>
                    </div>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>

          <div class="coupon-wrap reveal" style="margin-bottom:var(--sp-5)">
            <input type="text" class="coupon-input" id="couponInput" placeholder="Enter coupon code (e.g. FERI10)">
            <button class="btn btn-outline" onclick="applyCoupon()">Apply</button>
          </div>

          <div class="price-breakdown reveal">
            <div class="font-bold text-lg" style="margin-bottom:var(--sp-3)">Bill Details</div>
            <div class="price-row">
              <span class="label">Item Total</span>
              <span class="val">${formatMoney(totals.subtotal)}</span>
            </div>
            ${totals.totalDiscount > 0 ? `
              <div class="price-row discount">
                <span class="label">Product Discount</span>
                <span class="val">-${formatMoney(totals.totalDiscount)}</span>
              </div>
            ` : ''}
            <div class="price-row">
              <span class="label">Delivery Fee</span>
              <span class="val">${totals.delivery === 0 ? '<span class="text-primary">FREE</span>' : formatMoney(totals.delivery)}</span>
            </div>
            <div class="price-row">
              <span class="label">Taxes (GST 5%)</span>
              <span class="val">${formatMoney(totals.gst)}</span>
            </div>
            <div class="price-row total">
              <span class="label text-text">To Pay</span>
              <span class="val text-xl">${formatMoney(totals.grandTotal)}</span>
            </div>
            ${totals.totalDiscount > 0 ? `
              <div class="price-row savings">
                <i class="fas fa-gift"></i> You save ${formatMoney(totals.totalDiscount)} on this order!
              </div>
            ` : ''}
          </div>

          <div style="height:30px"></div>
          
          <!-- Sticky Bottom Bar -->
          <div class="cart-bottom-bar">
            <div class="cart-total-row">
              <div>
                <div class="cart-total-label">Total to Pay</div>
                <div class="cart-total-val">${formatMoney(totals.grandTotal)}</div>
              </div>
            </div>
            <button class="btn btn-primary btn-full btn-lg" onclick="navigateTo('/checkout'); playSound('click')">
              Proceed to Checkout <i class="fas fa-arrow-right"></i>
            </button>
          </div>
        </div>
      `;
      $content.innerHTML = html;

      // Make functions available globally for inline handlers
      window.updateCartQty = (id, newQty) => {
        if (newQty <= 0) {
          playSound('removeItem');
          const el = document.getElementById(`cart-item-${id}`);
          if(el) {
            el.classList.add('removing');
            setTimeout(() => {
              Store.updateQty(id, newQty);
              Pages.cart(); // re-render
            }, 300);
          } else {
            Store.updateQty(id, newQty);
            Pages.cart();
          }
        } else {
          playSound('click');
          Store.updateQty(id, newQty);
          Pages.cart();
        }
      };

      window.applyCoupon = () => {
        const input = document.getElementById('couponInput');
        const val = input.value.trim().toUpperCase();
        if (['FERI10', 'NEWUSER', 'SAVE50'].includes(val)) {
          playSound('coupon');
          showToast('Coupon Applied!', `You used code ${val}`);
          // Note: Full implementation would store coupon state, skipping for MVP simplicity
          input.value = '';
        } else {
          playSound('error');
          input.classList.remove('error');
          void input.offsetWidth; // trigger reflow
          input.classList.add('error');
          showToast('Invalid Coupon', '', 'error');
        }
      };
    },

    // ✅ CHECKOUT
    checkout: () => {
      setTopNav('Checkout', true);
      const user = Store.get().user;
      const items = Store.getCartItems();
      const totals = Store.getCartTotals();
      
      if(items.length === 0) return navigateTo('/cart');

      let html = `
        <div class="checkout-page">
          <!-- Address -->
          <div class="checkout-section reveal">
            <h3 class="checkout-section-title"><div class="step-num">1</div> Delivery Address</h3>
            <div class="stagger-children">
              ${user.addresses.map(a => `
                <div class="address-card ${a.selected ? 'selected' : ''}" onclick="selectAddress(${a.id}, this)">
                  <div class="address-card-header">
                    <div class="address-type"><i class="fas ${a.type==='Home'?'fa-home':'fa-building'} text-primary"></i> ${a.type}</div>
                    ${a.selected ? '<i class="fas fa-check-circle text-primary"></i>' : ''}
                  </div>
                  <div class="address-text">${a.text}</div>
                </div>
              `).join('')}
              <button class="btn btn-outline btn-full"><i class="fas fa-plus"></i> Add New Address</button>
            </div>
          </div>

          <!-- Payment -->
          <div class="checkout-section reveal reveal-delay-1">
            <h3 class="checkout-section-title"><div class="step-num">2</div> Payment Method</h3>
            <div class="stagger-children">
              ${[
                { id:'upi', name:'UPI', sub:'Google Pay, PhonePe, Paytm', icon:'fa-mobile-alt' },
                { id:'card', name:'Credit / Debit Card', sub:'Visa, MasterCard, RuPay', icon:'fa-credit-card' },
                { id:'cod', name:'Cash on Delivery', sub:'Pay when you receive', icon:'fa-money-bill-wave' }
              ].map((m, i) => `
                <div class="payment-option ${i===0?'selected':''}" onclick="selectPayment(this)">
                  <div class="payment-option-radio"></div>
                  <i class="fas ${m.icon} payment-option-icon text-muted"></i>
                  <div style="flex:1">
                    <div class="payment-option-label">${m.name}</div>
                    <div class="payment-option-sub">${m.sub}</div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- Order Summary -->
          <div class="checkout-section reveal reveal-delay-2">
            <h3 class="checkout-section-title"><div class="step-num">3</div> Order Summary</h3>
            <div class="order-summary-card">
              ${items.slice(0, 2).map(item => `
                <div class="order-summary-item">
                  <img src="${item.product.image}" class="order-summary-img">
                  <div style="flex:1">
                    <div class="order-summary-name truncate">${item.product.name}</div>
                    <div class="order-summary-qty">Qty: ${item.qty}</div>
                  </div>
                  <div class="order-summary-price">${formatMoney(item.product.price * item.qty)}</div>
                </div>
              `).join('')}
              ${items.length > 2 ? `<div class="text-center text-sm text-primary font-bold" style="padding:8px 0; border-top:1px solid var(--clr-border)">+ ${items.length - 2} more items</div>` : ''}
            </div>
            
            <div class="price-breakdown">
              <div class="price-row total" style="border:none; margin:0; padding:0;">
                <span class="label text-text">Total Payable</span>
                <span class="val text-xl text-primary">${formatMoney(totals.grandTotal)}</span>
              </div>
            </div>
          </div>

          <div style="height:30px"></div>
          
          <div class="cart-bottom-bar" style="border-radius:0;">
            <button class="btn btn-primary btn-full btn-lg" id="placeOrderBtn">
              <span id="poText">Place Order — ${formatMoney(totals.grandTotal)}</span>
              <div class="spinner spinner-sm hidden" id="poSpinner" style="margin:0; border-top-color:white;"></div>
            </button>
          </div>
        </div>
      `;
      $content.innerHTML = html;

      window.selectAddress = (id, el) => {
        playSound('click');
        document.querySelectorAll('.address-card').forEach(c => {
          c.classList.remove('selected');
          const header = c.querySelector('.address-card-header');
          const check = header.querySelector('.fa-check-circle');
          if(check) check.remove();
        });
        el.classList.add('selected');
        el.querySelector('.address-card-header').insertAdjacentHTML('beforeend', '<i class="fas fa-check-circle text-primary"></i>');
      };

      window.selectPayment = (el) => {
        playSound('click');
        document.querySelectorAll('.payment-option').forEach(c => c.classList.remove('selected'));
        el.classList.add('selected');
      };

      document.getElementById('placeOrderBtn').onclick = () => {
        playSound('click');
        const btn = document.getElementById('placeOrderBtn');
        const text = document.getElementById('poText');
        const spin = document.getElementById('poSpinner');
        
        btn.disabled = true;
        text.classList.add('hidden');
        spin.classList.remove('hidden');

        setTimeout(() => {
          // Process order
          const order = Store.placeOrder(1, 'Credit');
          
          // Trigger Real-Time Notification (Telegram & WhatsApp)
          if (window.NotificationService) {
            NotificationService.sendOrderNotification(order);
          }
          
          // Show Success Modal
          openOrderSuccessModal(order);
        }, 1500);
      };
    },

    // 📋 ORDERS
    orders: () => {
      setTopNav('My Orders', false);
      const orders = Store.get().orders;

      let html = `
        <div class="orders-page">
          <div class="orders-tabs reveal">
            <div class="orders-tab active">All Orders</div>
            <div class="orders-tab">Processing</div>
            <div class="orders-tab">Shipped</div>
            <div class="orders-tab">Delivered</div>
          </div>

          ${orders.length === 0 ? `
            <div class="empty-state reveal">
              <i class="fas fa-box empty-state-icon"></i>
              <h3>No Orders Yet</h3>
              <p>You haven't placed any orders. Start shopping to see your history here.</p>
              <button class="btn btn-primary mt-4" onclick="navigateTo('/home')">Start Shopping</button>
            </div>
          ` : `
            <div class="stagger-children">
              ${orders.map(o => `
                <div class="order-card" onclick="navigateTo('/order/${o.id}')">
                  <div class="order-card-header">
                    <div>
                      <div class="order-card-id">${o.id}</div>
                      <div class="order-card-date">${new Date(o.date).toLocaleDateString('en-IN', { day:'numeric', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit'})}</div>
                    </div>
                    <div class="status-badge status-${o.status.toLowerCase()}">${o.status}</div>
                  </div>
                  <div class="order-card-images">
                    ${o.items.slice(0,3).map(i => `<img src="${i.image}" class="order-card-img">`).join('')}
                    ${o.items.length > 3 ? `<div class="order-card-more">+${o.items.length - 3}</div>` : ''}
                  </div>
                  <div class="divider" style="margin:var(--sp-3) 0"></div>
                  <div class="order-card-footer">
                    <div class="order-card-total">${o.items.length} item(s) • <strong>${formatMoney(o.totals.grandTotal)}</strong></div>
                    <div class="text-primary font-bold text-sm">View Details <i class="fas fa-chevron-right"></i></div>
                  </div>
                </div>
              `).join('')}
            </div>
          `}
        </div>
      `;
      $content.innerHTML = html;
    },

    // 🗂️ ORDER DETAIL
    orderDetail: (req) => {
      setTopNav('Order Summary', true);
      const o = Store.getOrderById(req.params.id);
      if(!o) return navigateTo('/404');

      const dateStr = new Date(o.date).toLocaleDateString('en-IN', { day:'numeric', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit'});

      let html = `
        <div class="order-detail-page">
          <div class="order-detail-header reveal">
            <h2>${o.id}</h2>
            <p>Placed on ${dateStr}</p>
            <div class="badge bg-surface text-primary" style="margin-top:12px; font-size:14px; padding:6px 16px;">
              ${o.status}
            </div>
          </div>

          <div class="card reveal reveal-delay-1" style="margin-bottom:var(--sp-4)">
            <div class="card-body">
              <h3 class="font-bold text-base mb-4">Track Order</h3>
              <div class="order-tracker">
                <div class="tracker-step done">
                  <div class="tracker-dot"><i class="fas fa-check"></i></div>
                  <div class="tracker-line"></div>
                  <div class="tracker-content">
                    <div class="tracker-title">Order Placed</div>
                    <div class="tracker-sub">${dateStr}</div>
                  </div>
                </div>
                <div class="tracker-step done">
                  <div class="tracker-dot"><i class="fas fa-check"></i></div>
                  <div class="tracker-line"></div>
                  <div class="tracker-content">
                    <div class="tracker-title">Order Confirmed</div>
                    <div class="tracker-sub">Seller has processed your order</div>
                  </div>
                </div>
                <div class="tracker-step current">
                  <div class="tracker-dot"><i class="fas fa-truck"></i></div>
                  <div class="tracker-line"></div>
                  <div class="tracker-content">
                    <div class="tracker-title">Shipped</div>
                    <div class="tracker-sub">Expected by ${o.expectedDelivery}</div>
                  </div>
                </div>
                <div class="tracker-step upcoming">
                  <div class="tracker-dot"></div>
                  <div class="tracker-content">
                    <div class="tracker-title">Delivered</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card reveal reveal-delay-2" style="margin-bottom:var(--sp-4)">
            <div class="card-body">
              <h3 class="font-bold text-base mb-4">Delivery Address</h3>
              <p class="text-sm text-text-2 font-bold">${o.address.type}</p>
              <p class="text-sm text-muted mt-2 leading-relaxed">${o.address.text}</p>
            </div>
          </div>

          <div class="card reveal reveal-delay-3" style="margin-bottom:var(--sp-4)">
            <div class="card-body">
              <h3 class="font-bold text-base mb-4">Items (${o.items.length})</h3>
              <div class="stagger-children">
                ${o.items.map(i => `
                  <div class="order-summary-item">
                    <img src="${i.image}" class="order-summary-img">
                    <div style="flex:1">
                      <div class="order-summary-name truncate">${i.name}</div>
                      <div class="order-summary-qty">Qty: ${i.qty}</div>
                    </div>
                    <div class="order-summary-price">${formatMoney(i.priceAtPurchase * i.qty)}</div>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>

          <div class="price-breakdown reveal reveal-delay-4" style="margin-bottom:var(--sp-6)">
            <div class="font-bold text-base" style="margin-bottom:var(--sp-3)">Payment Summary</div>
            <div class="price-row"><span class="label">Payment Method</span><span class="val">${o.paymentMethod}</span></div>
            <div class="divider" style="margin:var(--sp-2) 0"></div>
            <div class="price-row"><span class="label">Item Total</span><span class="val">${formatMoney(o.totals.subtotal)}</span></div>
            ${o.totals.totalDiscount > 0 ? `<div class="price-row discount"><span class="label">Discount</span><span class="val">-${formatMoney(o.totals.totalDiscount)}</span></div>` : ''}
            <div class="price-row"><span class="label">Delivery</span><span class="val">${o.totals.delivery===0?'Free':formatMoney(o.totals.delivery)}</span></div>
            <div class="price-row"><span class="label">GST</span><span class="val">${formatMoney(o.totals.gst)}</span></div>
            <div class="price-row total"><span class="label text-text">Total Amount</span><span class="val text-xl text-primary">${formatMoney(o.totals.grandTotal)}</span></div>
          </div>
          
          <button class="btn btn-outline btn-full btn-lg reveal reveal-delay-4" onclick="window.print()">
            <i class="fas fa-file-invoice"></i> Download Invoice
          </button>
          
          <div style="height:30px"></div>
        </div>
      `;
      $content.innerHTML = html;
    },

    // 👤 PROFILE
    profile: () => {
      setTopNav('Profile', false);
      const u = Store.get().user;
      const orderCount = Store.get().orders.length;
      const wishlistCount = Store.get().wishlist.length;

      let html = `
        <div class="profile-page">
          <div class="profile-hero reveal">
            <div class="profile-avatar-wrap">
              <div class="profile-avatar">${u.avatar}</div>
              <div class="profile-avatar-edit"><i class="fas fa-pen"></i></div>
            </div>
            <div class="profile-hero-name">${u.name}</div>
            <div class="profile-hero-email">${u.email} • +91 ${u.phone}</div>
          </div>

          <div class="profile-stats reveal reveal-delay-1">
            <div class="profile-stat" onclick="navigateTo('/orders')">
              <div class="profile-stat-val">${orderCount}</div>
              <div class="profile-stat-label">Orders</div>
            </div>
            <div class="profile-stat" onclick="navigateTo('/wishlist')">
              <div class="profile-stat-val">${wishlistCount}</div>
              <div class="profile-stat-label">Wishlist</div>
            </div>
            <div class="profile-stat">
              <div class="profile-stat-val">₹0</div>
              <div class="profile-stat-label">Cashback</div>
            </div>
          </div>

          <div class="profile-section-title reveal reveal-delay-2">Account</div>
          <div class="settings-list reveal reveal-delay-2">
            <div class="settings-item">
              <div class="settings-icon"><i class="fas fa-map-marker-alt"></i></div>
              <div class="settings-label">
                <div class="settings-title">My Addresses</div>
                <div class="settings-sub">${u.addresses.length} saved addresses</div>
              </div>
              <i class="fas fa-chevron-right settings-arrow"></i>
            </div>
            <div class="settings-item">
              <div class="settings-icon"><i class="fas fa-credit-card"></i></div>
              <div class="settings-label">
                <div class="settings-title">Payment Methods</div>
                <div class="settings-sub">Cards, UPI saved</div>
              </div>
              <i class="fas fa-chevron-right settings-arrow"></i>
            </div>
          </div>

          <div class="profile-section-title reveal reveal-delay-3" style="margin-top:var(--sp-4)">Settings</div>
          <div class="settings-list reveal reveal-delay-3">
            <div class="settings-item">
              <div class="settings-icon" style="background:var(--clr-bg); color:var(--clr-text-2)"><i class="fas fa-moon"></i></div>
              <div class="settings-label"><div class="settings-title">Dark Mode</div></div>
              <label class="toggle-switch">
                <input type="checkbox" ${u.preferences.dark ? 'checked' : ''} onchange="toggleTheme()">
                <div class="toggle-slider"></div>
              </label>
            </div>
            <div class="settings-item">
              <div class="settings-icon" style="background:var(--clr-bg); color:var(--clr-text-2)"><i class="fas fa-bell"></i></div>
              <div class="settings-label"><div class="settings-title">Notifications</div></div>
              <label class="toggle-switch">
                <input type="checkbox" checked onchange="playSound('toggle')">
                <div class="toggle-slider"></div>
              </label>
            </div>
            <div class="settings-item">
              <div class="settings-icon" style="background:var(--clr-bg); color:var(--clr-text-2)"><i class="fas fa-volume-up"></i></div>
              <div class="settings-label"><div class="settings-title">Sound Effects</div></div>
              <label class="toggle-switch">
                <input type="checkbox" ${SoundEngine.isEnabled() ? 'checked' : ''} onchange="SoundEngine.setEnabled(this.checked); playSound('toggle')">
                <div class="toggle-slider"></div>
              </label>
            </div>
          </div>

          <div class="profile-section-title reveal reveal-delay-3" style="margin-top:var(--sp-4)">🔔 Order Alerts (Telegram & WhatsApp)</div>
          <div class="settings-list reveal reveal-delay-3" style="padding:16px; background:var(--clr-surface); border-radius:var(--r-lg); border:1px solid var(--clr-border);">
            <div style="margin-bottom:14px;">
              <div style="display:flex; align-items:center; gap:8px; font-weight:700; color:#0088cc; margin-bottom:4px; font-size:14px;">
                <i class="fab fa-telegram-plane" style="font-size:18px;"></i>
                <span>Telegram Instant Bot (100% Free)</span>
              </div>
              <p style="font-size:12px; color:var(--clr-text-2); margin-bottom:10px;">
                Receive instant push notifications with sound on your phone whenever any customer places an order.
              </p>
              <div style="display:flex; flex-direction:column; gap:8px;">
                <div>
                  <label style="font-size:11px; font-weight:600; color:var(--clr-text-2); display:block; margin-bottom:2px;">Telegram Bot Token</label>
                  <input type="text" id="cfgTgToken" class="form-input" placeholder="e.g. 123456:ABC-DEF1234ghIkl..." value="${(NotificationService.getConfig().telegramBotToken || '')}" style="width:100%; font-size:12px; padding:8px 10px; border:1px solid var(--clr-border); border-radius:8px; background:var(--clr-bg); color:var(--clr-text-1);">
                </div>
                <div>
                  <label style="font-size:11px; font-weight:600; color:var(--clr-text-2); display:block; margin-bottom:2px;">Telegram Chat ID</label>
                  <input type="text" id="cfgTgChatId" class="form-input" placeholder="e.g. 123456789" value="${(NotificationService.getConfig().telegramChatId || '')}" style="width:100%; font-size:12px; padding:8px 10px; border:1px solid var(--clr-border); border-radius:8px; background:var(--clr-bg); color:var(--clr-text-1);">
                </div>
              </div>
              
              <div style="margin-top:8px; padding:8px 10px; background:rgba(0,136,204,0.06); border-radius:8px; font-size:11.5px; color:var(--clr-text-2); line-height:1.4;">
                <strong>⚡ 60-Second Setup:</strong><br>
                1. Open Telegram & search for <b>@BotFather</b> &gt; type <code>/newbot</code> &gt; copy Token.<br>
                2. Search <b>@userinfobot</b> on Telegram &gt; copy your Chat ID.<br>
                3. Paste both here and tap <b>Save & Test</b>!
              </div>
            </div>

            <hr style="border:none; border-top:1px solid var(--clr-border); margin:14px 0;">

            <div style="margin-bottom:14px;">
              <div style="display:flex; align-items:center; gap:8px; font-weight:700; color:#25D366; margin-bottom:4px; font-size:14px;">
                <i class="fab fa-whatsapp" style="font-size:18px;"></i>
                <span>WhatsApp Order Receipt</span>
              </div>
              <p style="font-size:12px; color:var(--clr-text-2); margin-bottom:10px;">
                Phone number to receive formatted order invoices via WhatsApp.
              </p>
              <div>
                <label style="font-size:11px; font-weight:600; color:var(--clr-text-2); display:block; margin-bottom:2px;">Admin WhatsApp Number (with country code)</label>
                <input type="text" id="cfgWaPhone" class="form-input" placeholder="e.g. 917767899764" value="${(NotificationService.getConfig().whatsappPhone || '917767899764')}" style="width:100%; font-size:12px; padding:8px 10px; border:1px solid var(--clr-border); border-radius:8px; background:var(--clr-bg); color:var(--clr-text-1);">
              </div>
            </div>

            <div style="display:flex; flex-direction:column; gap:8px; margin-top:14px;">
              <button class="btn btn-primary btn-full" onclick="saveNotificationSettings()" style="font-weight:600; font-size:13px; padding:10px;">
                <i class="fas fa-check"></i> Save Notification Settings
              </button>
              <div style="display:flex; gap:8px;">
                <button class="btn btn-outline btn-sm" onclick="testTelegramAlert()" style="flex:1; font-size:11.5px; border-color:#0088cc; color:#0088cc;">
                  <i class="fab fa-telegram-plane"></i> Test Telegram
                </button>
                <button class="btn btn-outline btn-sm" onclick="testWhatsAppAlert()" style="flex:1; font-size:11.5px; border-color:#25D366; color:#25D366;">
                  <i class="fab fa-whatsapp"></i> Test WhatsApp
                </button>
              </div>
            </div>
          </div>

          <div class="reveal reveal-delay-4" style="margin:var(--sp-6) 0">
            <button class="btn btn-outline btn-full btn-danger" onclick="playSound('click'); showToast('Logged Out', '', 'info')">
              <i class="fas fa-sign-out-alt"></i> Logout
            </button>
            <div class="text-center text-xs text-muted" style="margin-top:16px">App Version 1.0.0</div>
          </div>
          
          <div style="height:20px;"></div>
        </div>
      `;
      $content.innerHTML = html;

      window.saveNotificationSettings = function() {
        playSound('click');
        const tgToken = document.getElementById('cfgTgToken').value.trim();
        const tgChatId = document.getElementById('cfgTgChatId').value.trim();
        const waPhone = document.getElementById('cfgWaPhone').value.trim();
        
        NotificationService.saveConfig({
          telegramEnabled: true,
          telegramBotToken: tgToken,
          telegramChatId: tgChatId,
          whatsappPhone: waPhone,
          whatsappEnabled: true
        });
        
        showToast('Settings Saved', 'Order notifications updated successfully', 'success');
      };

      window.testTelegramAlert = async function() {
        playSound('click');
        window.saveNotificationSettings();
        showToast('Sending Test...', 'Dispatching to Telegram Bot', 'info');
        const res = await NotificationService.sendTestAlert('telegram');
        if (res && res.success) {
          showToast('Telegram Alert Sent!', 'Check your Telegram phone app now!', 'success');
        } else {
          showToast('Telegram Setup Needed', res.error || 'Add your Bot Token and Chat ID to receive alerts', 'info');
        }
      };

      window.testWhatsAppAlert = function() {
        playSound('click');
        window.saveNotificationSettings();
        NotificationService.sendTestAlert('whatsapp');
        showToast('WhatsApp Opened', 'Order invoice ready to send', 'success');
      };
    },

    // ❤️ WISHLIST
    wishlist: () => {
      setTopNav('My Wishlist', true);
      const wIds = Store.get().wishlist;
      const products = wIds.map(id => AppData.getProductById(id)).filter(Boolean);

      if (products.length === 0) {
        $content.innerHTML = `
          <div class="wishlist-empty reveal">
            <i class="far fa-heart empty-state-icon text-danger" style="opacity:0.3; font-size:80px;"></i>
            <h3 style="margin-top:20px">No saved items</h3>
            <p style="margin-bottom:24px">You haven't added any products to your wishlist yet.</p>
            <button class="btn btn-primary" onclick="navigateTo('/home')">Explore Products</button>
          </div>
        `;
        return;
      }

      $content.innerHTML = `
        <div class="wishlist-page">
          <div class="product-grid stagger-children">
            ${products.map(p => renderProductCard(p)).join('')}
          </div>
        </div>
      `;
      setupLazyImages();
    },

    // 🏢 BRANDS
    brands: () => {
      setTopNav('All Brands', true);
      
      $content.innerHTML = `
        <div class="brands-page">
          <div class="search-input-wrap reveal">
            <i class="fas fa-search search-icon"></i>
            <input type="text" class="form-input search-input" placeholder="Search brands...">
          </div>
          
          <div class="brands-grid stagger-children">
            ${AppData.brands.map(b => `
              <div class="brand-full-card" onclick="navigateTo('/products?brand=${encodeURIComponent(b)}')">
                <div class="brand-full-name">${b}</div>
                <div class="brand-full-count">Explore <i class="fas fa-arrow-right"></i></div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    },

    // ❌ 404
    notFound: () => {
      setTopNav('Not Found', true);
      $content.innerHTML = `
        <div class="page-404">
          <div class="page-404-num">404</div>
          <h2>Lost in Space</h2>
          <p>Looks like this page drifted away. Let's get you back home.</p>
          <button class="btn btn-primary mt-4" onclick="navigateTo('/home')"><i class="fas fa-home"></i> Back to Home</button>
        </div>
      `;
    }
  };


  // ── Modals ──────────────────────────────────────
  
  function openModal(htmlContent) {
    const overlay = document.getElementById('modalOverlay');
    const container = document.getElementById('modalContainer');
    
    container.innerHTML = `
      <div class="modal-inner">
        <div class="modal-handle"></div>
        ${htmlContent}
      </div>
    `;
    
    overlay.classList.add('active');
    container.classList.add('active');
    
    // Prevent background scrolling
    document.body.style.overflow = 'hidden';
  }

  window.closeModal = function() {
    playSound('click');
    const overlay = document.getElementById('modalOverlay');
    const container = document.getElementById('modalContainer');
    
    // Animate out
    const inner = container.querySelector('.modal-inner');
    if (inner) {
      inner.style.animation = 'modalOut 0.3s forwards';
    }
    overlay.style.opacity = '0';
    
    setTimeout(() => {
      overlay.classList.remove('active');
      container.classList.remove('active');
      overlay.style.opacity = '';
      container.innerHTML = '';
      document.body.style.overflow = '';
    }, 300);
  };

  window.openOrderSuccessModal = function(order) {
    const dateObj = new Date(order.date);
    const dateStr = dateObj.toLocaleDateString('en-IN', { day:'numeric', month:'short', year:'numeric' }) + ', ' + dateObj.toLocaleTimeString('en-IN', { hour:'2-digit', minute:'2-digit' });
    
    const html = `
      <div class="order-success-modal">
        <div class="order-success-confetti" id="osm-confetti"></div>
        <button class="btn-icon" style="position:absolute; top:16px; right:16px; color:var(--clr-muted);" onclick="navigateTo('/home'); closeModal()">
          <i class="fas fa-times"></i>
        </button>

        <div class="order-success-anim">
          <div class="order-success-ring"></div>
          <div class="order-success-check">
            <svg viewBox="0 0 52 52">
              <path d="M14 27 l 8 8 16 -16" />
            </svg>
          </div>
        </div>

        <div class="order-success-title">Order Placed Successfully!</div>
        <div class="order-success-sub">Thank you! Your order has been placed.</div>

        <div class="order-info-card">
          <div class="order-info-row">
            <div>
              <div class="order-info-label">Order ID</div>
              <div class="order-info-val" style="font-size:var(--fs-base)">
                ${order.id} <i class="far fa-copy text-muted text-sm ml-1" onclick="navigator.clipboard.writeText('${order.id}'); showToast('Copied to clipboard'); playSound('click')" style="cursor:pointer"></i>
              </div>
            </div>
            <div style="text-align:right">
              <div class="order-info-label">Order Date & Time</div>
              <div class="order-info-val" style="font-size:var(--fs-sm); font-weight:600">${dateStr}</div>
            </div>
          </div>
        </div>

        <div class="order-detail-item">
          <div class="order-detail-icon bg-light text-primary"><i class="fas fa-truck"></i></div>
          <div class="order-detail-content">
            <p>Order will be delivered</p>
            <strong class="text-primary">${order.expectedDelivery}</strong>
            <p class="text-xs mt-1">10:00 AM - 08:00 PM</p>
          </div>
          <div class="badge badge-success">Estimated</div>
        </div>

        <div class="order-detail-item">
          <div class="order-detail-icon bg-light text-primary"><i class="fas fa-wallet"></i></div>
          <div class="order-detail-content">
            <p>Payment Method</p>
            <strong>${order.paymentMethod}</strong>
          </div>
          <div style="text-align:right">
            <p>Amount</p>
            <strong>${formatMoney(order.totals.grandTotal)}</strong>
          </div>
        </div>

        <div class="order-guarantee-card" onclick="playSound('click')">
          <div class="order-detail-icon" style="background:#2563EB; color:white; width:36px; height:36px; font-size:16px"><i class="fas fa-shield-alt"></i></div>
          <div>
            <div class="title">60-Day Risk-Free Guarantee</div>
            <p>Try new products with confidence.<br>Not satisfied? Return within 60 days and get equal value products.</p>
          </div>
          <i class="fas fa-chevron-right text-muted" style="margin-left:auto"></i>
        </div>

        ${order.totals.totalDiscount > 0 ? `
          <div class="order-savings-banner" onclick="playSound('click')">
            <div class="flex items-center gap-2">
              <i class="fas fa-gift text-primary"></i>
              <span class="order-savings-text">You saved ${formatMoney(order.totals.totalDiscount)} on this order!</span>
            </div>
            <i class="fas fa-chevron-right text-primary"></i>
          </div>
        ` : ''}

        <div class="order-invite-card" onclick="playSound('click')">
          <div class="order-detail-icon" style="background:#FFF3DC; color:#F5A623; width:40px; height:40px"><i class="fas fa-star"></i></div>
          <div style="flex:1">
            <h4>Invite & Earn</h4>
            <p>Invite other retailers and earn exciting rewards.</p>
          </div>
          <button class="btn btn-outline btn-sm">Invite Now</button>
        </div>

        <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:12px; padding:12px 14px; margin-bottom:12px;">
          <div style="display:flex; align-items:center; gap:8px; font-weight:600; color:#15803D; font-size:13px; margin-bottom:4px;">
            <i class="fab fa-telegram-plane" style="color:#0088cc; font-size:16px;"></i>
            <span>Real-Time Alert Dispatched</span>
          </div>
          <div style="font-size:12px; color:#166534; line-height:1.4;">
            Order details were transmitted to your connected Telegram store bot automatically.
          </div>
        </div>

        <a href="${NotificationService.getWhatsAppUrl(order)}" target="_blank" class="btn btn-full btn-lg mb-3" style="background:#25D366; color:white; font-weight:700; gap:8px; text-decoration:none; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 14px rgba(37,211,102,0.3); border-radius:12px;">
          <i class="fab fa-whatsapp" style="font-size:20px;"></i> Share Invoice on WhatsApp
        </a>

        <button class="btn btn-primary btn-full btn-lg mb-3" onclick="closeModal(); navigateTo('/order/${order.id}')">View Order Details</button>
        <button class="btn btn-ghost btn-full" onclick="closeModal(); navigateTo('/home')">Continue Shopping</button>
      </div>
    `;
    
    openModal(html);
    
    // Trigger Success Animations
    setTimeout(() => {
      playSound('orderSuccess');
      Confetti.burst(150);
    }, 100);
  };

  // ── Initialization ─────────────────────────────
  function init() {
    // 1. Setup Router
    Router.on('/home', Pages.home);
    Router.on('/search', Pages.search);
    Router.on('/products', Pages.products);
    Router.on('/product/:id', Pages.productDetail);
    Router.on('/cart', Pages.cart);
    Router.on('/checkout', Pages.checkout);
    Router.on('/orders', Pages.orders);
    Router.on('/order/:id', Pages.orderDetail);
    Router.on('/wishlist', Pages.wishlist);
    Router.on('/profile', Pages.profile);
    Router.on('/brands', Pages.brands);
    Router.setNotFound(Pages.notFound);

    // 2. Global Event Listeners
    document.addEventListener('feri:statechange', updateBadges);
    
    // 3. Apply Theme & Badges
    applyTheme();
    updateBadges();

    // 4. Show App & Init Router Immediately (Blazing Fast)
    const appShell = document.getElementById('app');
    if (appShell) appShell.style.display = 'flex';
    Router.init();
  }

  return { init };
})();

// Boot
document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
