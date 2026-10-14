// Render an inline SVG with Chromium, preserving strokes and transparent pixels.
// Run by build-brand-assets.py. Playwright can be installed here or in the
// adjacent shared design-system checkout.
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
const require = createRequire(import.meta.url);
let playwright;
try { playwright = require('playwright'); }
catch {
  const root = process.env.BRAND_PLAYWRIGHT_PATH || '/home/pankaj/Projects/leanchain/design-system/node_modules/playwright';
  playwright = require(root);
}
const [src, dest] = process.argv.slice(2);
if (!src || !dest) throw new Error('Usage: node scripts/render-brand-svg.mjs source.svg output.png');
const browser = await playwright.chromium.launch({ headless: true, args: ['--no-sandbox'] });
try {
  const page = await browser.newPage({viewport:{width:1024,height:1024}, deviceScaleFactor:1, colorScheme:'light'});
  const svg = readFileSync(resolve(src),'utf8').replace('<svg ', '<svg width="1024" height="1024" ');
  await page.setContent(`<html><head><style>html,body{margin:0;padding:0;background:transparent}</style></head><body>${svg}</body></html>`);
  await page.locator('svg').screenshot({path:resolve(dest), omitBackground:true, animations:'disabled'});
} finally {await browser.close();}
