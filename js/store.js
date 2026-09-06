/* ══════════════════════════════════════════════
   FERI — State Management (Store)
   ══════════════════════════════════════════════ */

const Store = (() => {
  const STORAGE_KEY = 'feri_app_state';
  
  // Default Initial State
  const defaultState = {
    cart: [], // { productId, qty, addedAt }
    wishlist: [], // [productId]
    orders: [], // { id, items, total, status, date, address, payment, expectedDelivery }
    user: { 
      name: 'Guest User', 
      email: 'guest@feri.app', 
      phone: '9876543210', 
      avatar: '😊', 
      addresses: [
        { id: 1, type: 'Home', text: '123, Green Park, South Extension, New Delhi - 110049', selected: true },
        { id: 2, type: 'Work', text: '45/B, Tech Park, Sector 4, Gurgaon - 122001', selected: false }
      ], 
      preferences: { notifications: true, sound: true, dark: false } 
    },
    recentlyViewed: [],
    recentSearches: ['milk', 'dove', 'maggi', 'amul butter']
  };

  // Load from localStorage or use default
  let state = defaultState;
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      state = { ...defaultState, ...JSON.parse(saved) };
    }
  } catch(e) { console.error('Failed to load state from localStorage', e); }

  // Save to localStorage and emit event
  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch(e) { console.error('Failed to save state to localStorage', e); }
    
    // Dispatch custom event for UI updates
    document.dispatchEvent(new CustomEvent('feri:statechange'));
  }

  return {
    get: () => state,
    
    // Cart Actions
    addToCart: (productId, qty = 1) => {
      const existing = state.cart.find(item => item.productId === productId);
      if (existing) {
        existing.qty += qty;
      } else {
        state.cart.push({ productId, qty, addedAt: Date.now() });
      }
      saveState();
    },
    
    removeFromCart: (productId) => {
      state.cart = state.cart.filter(item => item.productId !== productId);
      saveState();
    },
    
    updateQty: (productId, qty) => {
      const item = state.cart.find(item => item.productId === productId);
      if (item) {
        item.qty = qty;
        if (item.qty <= 0) state.cart = state.cart.filter(i => i.productId !== productId);
        saveState();
      }
    },

    clearCart: () => {
      state.cart = [];
      saveState();
    },

    getCartCount: () => {
      return state.cart.reduce((total, item) => total + item.qty, 0);
    },

    getCartItems: () => {
      return state.cart.map(item => {
        const product = AppData.getProductById(item.productId);
        return { ...item, product };
      }).filter(item => item.product); // Filter out if product not found
    },

    getCartTotals: (couponCode = '') => {
      const items = Store.getCartItems();
      let subtotal = 0;
      let totalDiscount = 0;
      
      items.forEach(item => {
        const p = item.product;
        subtotal += p.mrp * item.qty;
        totalDiscount += (p.mrp - p.price) * item.qty;
      });

      let finalPrice = subtotal - totalDiscount;
      let couponSavings = 0;

      // Simple mock coupon logic
      if (couponCode === 'FERI10') { couponSavings = Math.floor(finalPrice * 0.1); }
      else if (couponCode === 'NEWUSER') { couponSavings = Math.floor(finalPrice * 0.15); }
      else if (couponCode === 'SAVE50') { couponSavings = 50; }

      finalPrice -= couponSavings;
      
      const delivery = finalPrice > 499 ? 0 : 50;
      const gst = Math.floor(finalPrice * 0.05); // Mock 5% GST
      
      const grandTotal = finalPrice + delivery + gst;

      return { subtotal, totalDiscount, couponSavings, delivery, gst, grandTotal, finalPrice };
    },

    // Wishlist Actions
    toggleWishlist: (productId) => {
      const idx = state.wishlist.indexOf(productId);
      let isAdded = false;
      if (idx > -1) {
        state.wishlist.splice(idx, 1);
      } else {
        state.wishlist.push(productId);
        isAdded = true;
      }
      saveState();
      return isAdded;
    },

    isInWishlist: (productId) => {
      return state.wishlist.includes(productId);
    },

    // Orders Actions
    placeOrder: (addressId, paymentMethod, couponCode = '') => {
      const items = Store.getCartItems().map(i => ({
        productId: i.productId,
        qty: i.qty,
        priceAtPurchase: i.product.price,
        name: i.product.name,
        image: i.product.image
      }));
      
      const totals = Store.getCartTotals(couponCode);
      const address = state.user.addresses.find(a => a.id === addressId) || state.user.addresses[0];

      // Delivery date logic: Today + 2 days
      const d = new Date();
      d.setDate(d.getDate() + 2);
      const expectedDelivery = d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric', weekday: 'short' });

      const newOrder = {
        id: 'ORD' + Math.floor(10000000 + Math.random() * 90000000), // e.g. ORD12345678
        date: new Date().toISOString(),
        items,
        totals,
        status: 'Processing',
        address,
        paymentMethod,
        expectedDelivery
      };

      state.orders.unshift(newOrder); // Add to beginning
      state.cart = []; // Clear cart
      saveState();
      return newOrder;
    },

    getOrderById: (id) => {
      return state.orders.find(o => o.id === id);
    },

    // Misc
    addRecentSearch: (query) => {
      if(!query.trim()) return;
      state.recentSearches = state.recentSearches.filter(q => q.toLowerCase() !== query.toLowerCase());
      state.recentSearches.unshift(query);
      if (state.recentSearches.length > 10) state.recentSearches.pop();
      saveState();
    },

    addRecentlyViewed: (productId) => {
      state.recentlyViewed = state.recentlyViewed.filter(id => id !== productId);
      state.recentlyViewed.unshift(productId);
      if (state.recentlyViewed.length > 20) state.recentlyViewed.pop();
      saveState();
    },

    updatePreference: (key, value) => {
      state.user.preferences[key] = value;
      saveState();
    }
  };
})();
