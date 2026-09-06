/* ══════════════════════════════════════════════
   FERI — Hash-based SPA Router
   ══════════════════════════════════════════════ */

const Router = (() => {
  let routes = {};
  let notFoundHandler = null;

  function on(route, handler) {
    routes[route] = handler;
  }

  function setNotFound(handler) {
    notFoundHandler = handler;
  }

  function resolveRoute() {
    let hash = window.location.hash || '#/home';
    if (!hash.startsWith('#/')) hash = '#/home';
    
    const pathParts = hash.substring(1).split('?');
    const path = pathParts[0];
    const query = pathParts[1] || '';
    
    const queryParams = {};
    query.split('&').forEach(pair => {
      if(!pair) return;
      const [key, val] = pair.split('=');
      queryParams[key] = decodeURIComponent(val || '');
    });

    let matchedHandler = null;
    let params = {};

    // Exact match
    if (routes[path]) {
      matchedHandler = routes[path];
    } else {
      // Parameterized match (e.g. /product/:id)
      for (const route in routes) {
        if (route.includes(':')) {
          const routeParts = route.split('/');
          const currentParts = path.split('/');
          
          if (routeParts.length === currentParts.length) {
            let match = true;
            for (let i = 0; i < routeParts.length; i++) {
              if (routeParts[i].startsWith(':')) {
                const paramName = routeParts[i].substring(1);
                params[paramName] = currentParts[i];
              } else if (routeParts[i] !== currentParts[i]) {
                match = false;
                break;
              }
            }
            if (match) {
              matchedHandler = routes[route];
              break;
            }
          }
        }
      }
    }

    if (matchedHandler) {
      // Trigger page transition animation
      const content = document.getElementById('pageContent');
      if (content) animatePageIn(content);
      
      // Update Bottom Nav active state
      updateBottomNav(path);

      // Execute handler
      matchedHandler({ path, params, query: queryParams });
      
      // Scroll to top
      window.scrollTo({ top: 0, behavior: 'instant' });
      
    } else if (notFoundHandler) {
      updateBottomNav('');
      notFoundHandler({ path });
    }
  }

  function updateBottomNav(path) {
    document.querySelectorAll('.bnav-item').forEach(el => el.classList.remove('active'));
    
    let activeId = '';
    if (path.startsWith('/home')) activeId = 'bnav-home';
    else if (path.startsWith('/search') || path.startsWith('/products')) activeId = 'bnav-categories';
    else if (path.startsWith('/cart')) activeId = 'bnav-cart';
    else if (path.startsWith('/orders') || path.startsWith('/order/')) activeId = 'bnav-orders';
    else if (path.startsWith('/profile') || path.startsWith('/wishlist')) activeId = 'bnav-profile';
    
    if (activeId) {
      const el = document.getElementById(activeId);
      if (el) el.classList.add('active');
    }
  }

  function init() {
    window.addEventListener('hashchange', resolveRoute);
    // Initial resolve
    setTimeout(resolveRoute, 0);
  }

  function navigate(path) {
    window.location.hash = path;
  }

  return { on, setNotFound, init, navigate };
})();

// Global navigate function helper
function navigateTo(path) {
  Router.navigate(path);
}
