# Olaryn

Static site for [olaryn.com](https://olaryn.com), deployed on Cloudflare Pages.

## Pages

| Route | Purpose |
| --- | --- |
| `/` | Olaryn company homepage; links to its products and shared infrastructure |
| `/authward/` | Public Authward developer-focused marketing page: the real discovery document, the login flow, ownership, setup and protocol surface |
| `/billing/` | Public Tallyward (Olaryn Billing service) page: a playable reservation ledger, enforced rules, credit lifetimes and the API shapes; the URL and `billing.olaryn.com` keep the `billing` name |

The marketing pages use ordinary directory `index.html` files. All pages share `/assets/base.css` (self-hosted Archivo and JetBrains Mono `@font-face` rules, every colour token for both themes, and the pane/seam/button primitives); the home page adds `/assets/home.css` and the product pages `/assets/platform.css`. Change a token once in `base.css`, never per page. Bump the `?v=` on the stylesheet links when a shared stylesheet changes. Fonts live in `assets/fonts/` (Latin subset, OFL) so no third-party font request is made and the CSP can stay `default-src 'self'`.

No framework, backend routes, build step or dependency installation is needed. Two small scripts exist: `assets/theme.js` (theme toggle) and `assets/ledger.js` (the Tallyward ledger simulation, which runs entirely in the browser and makes no network calls). Cloudflare Pages serves these as clean URLs. The shared site assets use root-relative paths.

Marketing and platform runtime stay separate:
- `https://auth.olaryn.com` remains the OAuth/OIDC issuer and hosts the protected developer portal (`/developer`) and docs (`/docs`). Never proxy, redirect, or rewrite identity protocol endpoints through the marketing pages.
- `https://billing.olaryn.com` remains the service API. There is no public developer signup or pricing page for Billing. The public description must not advertise the private API as open self-service.
- Feature copy must match the Authward and Billing repository contracts. Avoid displaying invented commercial prices or live account balances.

## Brand identity

The visual world is a graphite working surface: panes on a ground, divided by 1px hairline seams (no shadows, square corners). One accent (azure, `#0A59C0` light / `#62B2FF` dark) marks the primary action and code keys; green, amber and red appear only as state (ok, held, error). Light is a cool grey-white twin of the dark graphite; there is no pink and no warm cream. Type is Archivo (headings at a condensed width, body at normal width) and JetBrains Mono for code and data only. The original monochrome Olaryn mark is unchanged; its dot takes the accent.

Authward uses its own shield-in-O symbol (`assets/authward-mark.svg`) and Tallyward a ledger-in-O symbol (`assets/billing-mark.svg`); both are monochrome ink. The product brands Beseam, LemonCrow, and Trevra retain their own accents. DESIGN.md records the system; PRODUCT.md records product truth.

## Live material on the pages

The Authward hero shows an excerpt of the real `https://auth.olaryn.com/.well-known/openid-configuration`, copied as a snapshot (the page cannot fetch it: the CSP is `default-src 'self'` and the issuer sends no CORS headers). Its chip carries the snapshot date. To refresh, curl the document, copy the same keys, update the `24 more members` count and the date. Never publish the per-application entries in `scopes_supported`. The Tallyward ledger and request shapes follow `../Billing/src/billing_service/schemas.py` and `models.py`.

## Light and dark themes

Every page follows the visitor's OS setting and also has a toggle button (top right) that saves an explicit choice in `localStorage` under `olaryn-theme`. `assets/theme.js` is loaded in `<head>` so the saved choice applies before first paint; it sets `data-theme="light|dark"` on `<html>`. In `base.css` every colour token is a single `light-dark(light, dark)` value, resolved by the page's `color-scheme` (OS by default, forced by `data-theme`), so there is one place to change a colour. Brand marks are `<use href="/assets/marks.svg#...">` symbols so they follow the page theme rather than the OS (the standalone `*.svg` files are for favicons, social cards and other non-page uses). Without JavaScript the toggle stays hidden and the page follows the OS.

## Local preview and validation

Run at the repository root:

```bash
python3 scripts/check-pages.py
python3 -m http.server 43181 --bind 127.0.0.1
```

Visit `http://127.0.0.1:43181/`, `/authward/`, and `/billing/`. Confirm mobile and desktop layouts, both color modes, links, and focus states. No live deployment occurs just by changing this source branch.

## Social cards

`assets/og/authward.png`, `assets/og/billing.png` and `og-image.png` (home) are rendered from `scripts/og-card.html` (`?p=authward|billing|home`). With the local server running, capture each with headless Chrome at 1200×630, e.g. `google-chrome --headless=new --window-size=1200,630 --virtual-time-budget=4000 --screenshot=assets/og/billing.png 'http://127.0.0.1:43181/scripts/og-card.html?p=billing'`. Bump the `?v=` on the page's `og:image` after regenerating.

## Logo assets

`logo-mark.svg` and `favicon.svg` are the Olaryn source assets. Regenerate the Olaryn PNG favicons and Apple/PWA icons with `python3 scripts/build-brand-assets.py --brand olaryn` (requires Pillow, Node.js, and Playwright/Chromium); the social cards come from `scripts/og-card.html` as above. Do not edit generated raster assets by hand.
