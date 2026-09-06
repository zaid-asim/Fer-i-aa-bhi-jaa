// Verify App scripts in headless node environment with jsdom-like mock
const fs = require('fs');

const dataJs = fs.readFileSync('js/data.js', 'utf-8');
const storeJs = fs.readFileSync('js/store.js', 'utf-8');
const soundJs = fs.readFileSync('js/sound.js', 'utf-8');
const animJs = fs.readFileSync('js/animations.js', 'utf-8');
const routerJs = fs.readFileSync('js/router.js', 'utf-8');
const appJs = fs.readFileSync('js/app.js', 'utf-8');

console.log("data.js size:", dataJs.length);
console.log("store.js size:", storeJs.length);
console.log("sound.js size:", soundJs.length);
console.log("animations.js size:", animJs.length);
console.log("router.js size:", routerJs.length);
console.log("app.js size:", appJs.length);

// Check if all asset files referenced in data.js exist
const matches = dataJs.match(/image:\s*"([^"]+)"/g) || [];
console.log("Total product images in data.js:", matches.length);

let missing = 0;
for (const m of matches) {
  const p = m.replace(/image:\s*"/, '').replace('"', '');
  if (!fs.existsSync(p)) {
    console.error("Missing file:", p);
    missing++;
  }
}
console.log("Missing image files:", missing);

// Check UI assets
const uiAssets = [
  'images/ui/feri_logo.svg',
  'images/ui/credit_wallet.svg',
  'images/ui/shield_60days.svg',
  'images/ui/store_avatar.svg',
  'images/brands/hul.svg',
  'images/brands/coca_cola.svg',
  'images/brands/pepsico.svg',
  'images/brands/itc.svg',
  'images/brands/nestle.svg',
  'images/brands/parle.svg',
  'images/brands/britannia.svg',
  'images/brands/amul.svg',
  'images/brands/dabur.svg',
  'images/brands/tata.svg',
  'images/categories/cat_grocery.svg',
  'images/categories/cat_beverages.svg',
  'images/categories/cat_snacks.svg',
  'images/categories/cat_personal_care.svg',
  'images/categories/cat_home_care.svg',
  'images/categories/cat_dairy.svg',
  'images/categories/cat_biscuits.svg',
  'images/categories/cat_pooja.svg',
  'images/categories/cat_stationery.svg',
  'images/categories/cat_more.svg'
];

let missingUi = 0;
for (const a of uiAssets) {
  if (!fs.existsSync(a)) {
    console.error("Missing UI asset:", a);
    missingUi++;
  }
}
console.log("Total UI assets checked:", uiAssets.length);
console.log("Missing UI assets:", missingUi);
