const puppeteer = require('puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 414, height: 896, deviceScaleFactor: 2 });
    
    console.log("Navigating to http://localhost:8080/index.html...");
    await page.goto('http://localhost:8080/index.html', { waitUntil: 'networkidle0' });
    
    // Wait 300ms for fast splash fadeout
    await new Promise(r => setTimeout(r, 400));
    
    await page.screenshot({ path: 'images/ui/screenshot_verified_top.png', fullPage: false });
    console.log("Saved top screenshot to images/ui/screenshot_verified_top.png");

    await page.evaluate(() => window.scrollBy(0, 480));
    await new Promise(r => setTimeout(r, 300));
    await page.screenshot({ path: 'images/ui/screenshot_verified_bottom.png', fullPage: false });
    console.log("Saved bottom screenshot to images/ui/screenshot_verified_bottom.png");

    await browser.close();
    console.log("Puppeteer screenshots captured successfully!");
  } catch (err) {
    console.error("Puppeteer error:", err);
  }
})();
