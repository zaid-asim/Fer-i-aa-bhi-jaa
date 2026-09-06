const fs = require('fs');
const https = require('https');
const path = require('path');

const dataFile = path.join(__dirname, '../js/data.js');
const code = fs.readFileSync(dataFile, 'utf-8');

const sandbox = { Math: Math, console: console };
const vm = require('vm');
vm.createContext(sandbox);

// Convert const AppData to var AppData so it attaches to the sandbox, or explicitly assign it
const modifiedCode = code + '\n; sandbox.AppData = AppData;';
sandbox.sandbox = sandbox; // Make sandbox available inside the VM context

vm.runInContext(modifiedCode, sandbox);

const AppData = sandbox.AppData;

const imgDir = path.join(__dirname, '../img/products');

async function downloadImage(url, dest) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      // Handle redirects
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return downloadImage(res.headers.location, dest).then(resolve).catch(reject);
      }
      if (res.statusCode !== 200) {
        return reject(new Error(`Failed to get '${url}' (${res.statusCode})`));
      }
      const file = fs.createWriteStream(dest);
      res.pipe(file);
      file.on('finish', () => {
        file.close(resolve);
      });
    }).on('error', (err) => {
      fs.unlink(dest, () => reject(err));
    });
  });
}

async function run() {
  console.log(`Starting download for ${AppData.products.length} products...`);
  
  // Create a concurrency limit
  const limit = 2; // Keep it low to avoid 429
  let active = 0;
  let index = 0;
  
  await new Promise((resolve) => {
    function next() {
      if (index >= AppData.products.length && active === 0) {
        return resolve();
      }
      while (active < limit && index < AppData.products.length) {
        const p = AppData.products[index++];
        active++;
        
        const filename = `${p.id}.jpg`;
        const dest = path.join(imgDir, filename);
        
        // Update product object
        const oldImage = p.image;
        p.image = `img/products/${filename}`;
        p.images = [p.image, p.image, p.image]; // Simplify to use same image for now
        
        // Add a small delay
        setTimeout(() => {
          downloadImage(oldImage, dest)
            .then(() => {
              console.log(`[${index}/${AppData.products.length}] Downloaded ${filename}`);
              active--;
              next();
            })
            .catch(err => {
              console.error(`Error on ${filename}:`, err.message);
              active--;
              next();
            });
        }, 300);
      }
    }
    next(); // Start the loop
  });
  
  console.log('Finished downloading images. Rewriting data.js...');
  
  // Rewrite data.js with static data
  const newDataJs = `/* ══════════════════════════════════════════════
   FERI — Static Seed Data
   Generated with pre-loaded AI images
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

console.log(\`Loaded \${AppData.products.length} pre-generated products with local images.\`);
`;

  fs.writeFileSync(dataFile, newDataJs, 'utf-8');
  console.log('Done!');
}

run();
