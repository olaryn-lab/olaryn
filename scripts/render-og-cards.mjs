// Render the 1200x630 social cards from scripts/og-card.html with Chromium.
// Writes og-image.png (home) and assets/og/{identity,billing,analytics}.png. Bump the ?v= on the og:image URLs afterwards.
// Playwright can be installed here, or point BRAND_PLAYWRIGHT_PATH at another checkout's node_modules/playwright.
import { createRequire } from 'node:module';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { dirname, extname, join, normalize, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
let playwright;
try { playwright = require('playwright'); }
catch { playwright = require(process.env.BRAND_PLAYWRIGHT_PATH || '/home/pankaj/Projects/leanchain/design-system/node_modules/playwright'); }

const TYPES = { '.html': 'text/html', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.css': 'text/css' };
const server = createServer(async (req, res) => {
  const path = normalize(decodeURIComponent(new URL(req.url, 'http://x').pathname)).replace(/^([/\\])+/, '');
  try { res.writeHead(200, { 'content-type': TYPES[extname(path)] || 'application/octet-stream' }); res.end(await readFile(join(ROOT, path))); }
  catch { res.writeHead(404); res.end(); }
});
await new Promise((ok) => server.listen(0, '127.0.0.1', ok));
const base = `http://127.0.0.1:${server.address().port}`;

const browser = await playwright.chromium.launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1, colorScheme: 'light' });
  for (const [card, out] of [['home', 'og-image.png'], ['auth', 'assets/og/identity.png'], ['billing', 'assets/og/billing.png'], ['analytics', 'assets/og/analytics.png']]) {
    await page.goto(`${base}/scripts/og-card.html?p=${card}`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: join(ROOT, out) });
    console.log('wrote', out);
  }
} finally { await browser.close(); server.close(); }
