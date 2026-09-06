const fs = require('fs');
const path = require('path');

const dataFile = path.join(__dirname, '../js/data.js');
const linksFile = path.join(__dirname, '../js/image_links.json');

const code = fs.readFileSync(dataFile, 'utf-8');
const links = JSON.parse(fs.readFileSync(linksFile, 'utf-8'));

// Evaluate the code to get AppData
const sandbox = { Math: Math, console: console };
const vm = require('vm');
vm.createContext(sandbox);

const modifiedCode = code + '\n; sandbox.AppData = AppData;';
sandbox.sandbox = sandbox; 

vm.runInContext(modifiedCode, sandbox);
const AppData = sandbox.AppData;

console.log(`Loaded ${AppData.products.length} products.`);

// Assign realistic URLs from DummyJSON cyclically
AppData.products.forEach((p, index) => {
  const url = links[index % links.length];
  p.image = url;
  p.images = [url, url, url];
});

console.log('Rewriting data.js...');

// Rewrite data.js with static data
const newDataJs = `/* ══════════════════════════════════════════════
   FERI — Static Seed Data
   Generated with pre-loaded CDN real images
   ══════════════════════════════════════════════ */

const AppData = ${JSON.stringify(AppData, null, 2)};

// Ensure uniqueness of brands array
AppData.brands = [...new Set(AppData.brands)];

// Helper to get products
AppData.getProducts = (options = {}) => {
  let res = [...AppData.products];
  if (options.category) res = res.filter(p => p.category === options.category);
  if (options.brand) res = res.filter(p => p.brand === options.brand);
  if (options.query) {
    const q = options.query.toLowerCase();
    res = res.filter(p => p.name.toLowerCase().includes(q) || p.brand.toLowerCase().includes(q) || p.tags.some(t => t.includes(q)));
  }
  if (options.sort) {
    if (options.sort === 'price_asc') res.sort((a, b) => a.price - b.price);
    else if (options.sort === 'price_desc') res.sort((a, b) => b.price - a.price);
    else if (options.sort === 'rating') res.sort((a, b) => b.rating - a.rating);
  }
  
  if (options.limit) res = res.slice(0, options.limit);
  return res;
};

AppData.getProductById = (id) => {
  return AppData.products.find(p => p.id === id);
};

console.log(\`Loaded \${AppData.products.length} products with CDN images.\`);
`;

fs.writeFileSync(dataFile, newDataJs, 'utf-8');
console.log('Done!');
