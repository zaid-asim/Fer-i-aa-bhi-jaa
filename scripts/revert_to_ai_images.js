const fs = require('fs');
const path = require('path');

const dataFile = path.join(__dirname, '../js/data.js');
const code = fs.readFileSync(dataFile, 'utf-8');

// Evaluate the code to get AppData
const sandbox = { Math: Math, console: console };
const vm = require('vm');
vm.createContext(sandbox);

const modifiedCode = code + '\n; sandbox.AppData = AppData;';
sandbox.sandbox = sandbox; 

vm.runInContext(modifiedCode, sandbox);
const AppData = sandbox.AppData;

console.log(`Loaded ${AppData.products.length} products.`);

// Revert to Pollinations AI
AppData.products.forEach((p) => {
  const query = encodeURIComponent(`${p.brand} ${p.name} product packaging isolated white background studio lighting`);
  const aiUrl = `https://image.pollinations.ai/prompt/${query}?width=300&height=300&nologo=true&seed=${p.id}`;
  p.image = aiUrl;
  p.images = [aiUrl, aiUrl, aiUrl];
});

console.log('Rewriting data.js with AI links...');

// Rewrite data.js with static data
const newDataJs = `/* ══════════════════════════════════════════════
   FERI — Static Seed Data
   Generated with Pollinations AI links
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

console.log(\`Loaded \${AppData.products.length} products with AI images.\`);
`;

fs.writeFileSync(dataFile, newDataJs, 'utf-8');
console.log('Done!');
