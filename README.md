# Olaryn

Static site for [olaryn.com](https://olaryn.com), deployed on Cloudflare Pages.

## Pages

| Route | Purpose |
| --- | --- |
| `/` | Olaryn company homepage; introduces Zikela (identity), Bilyra (billing), and Yeleva (analytics), with permanent service hostnames |
| `/authward/` | Public Authward developer-focused marketing page |
| `/billing/` | Public Tallyward (Olaryn Billing service) architecture and capabilities page; the URL and `billing.olaryn.com` keep the `billing` name |

The marketing pages use ordinary directory `index.html` files. All pages share `/assets/base.css` (self-hosted Fraunces/Work Sans `@font-face` rules and every colour token, light and dark); the home page adds `/assets/home.css` and the product pages `/assets/platform.css`. Change a token once in `base.css`, never per page. Bump the `?v=` on the stylesheet links when a shared stylesheet changes. Fonts live in `assets/fonts/` (Latin subset, OFL) so no third-party font request is made and the CSP can stay `default-src 'self'`.

No framework, JavaScript, backend routes, or dependency installation is needed. Cloudflare Pages serves these as clean URLs. The shared site assets use root-relative paths.

Marketing and platform runtime stay separate:
- Olaryn's product names are **Zikela** (identity), **Bilyra** (billing), and **Yeleva** (analytics). The initial rename updates the homepage only; the existing Authward and Tallyward marketing pages remain at their current routes until their own copy/assets are migrated.
- `https://auth.olaryn.com` remains the OAuth/OIDC issuer and hosts the protected developer portal (`/developer`) and docs (`/docs`). Never proxy, redirect, or rewrite identity protocol endpoints through the marketing pages.
- `https://billing.olaryn.com` remains the service API. There is no public developer signup or pricing page for Billing. The public description must not advertise the private API as open self-service.
- `https://analytics.olaryn.com` remains the analytics service hostname, not a public product marketing page. The homepage identifies it without linking visitors into its application.
- Feature copy must match the Authward and Billing repository contracts. Avoid displaying invented commercial prices or live account balances.

## Brand identity

The approved light palette is deep burgundy `#6B3F4B` (accent and editorial headline), parchment `#F5EFE3` (page background), and deep ink `#211E1B` (logo/body text). The dark palette keeps charcoal `#181511` and swaps the accent for brass `#D6AD6A` (no pink anywhere); the infrastructure band is oxblood-black (`--band`, light `#251A1A` / dark `#2B1D1B`) with brass highlights. The product pages add an infrastructure band under the parchment hero, so each page shows the product's own screen on top and the service underneath. The Fraunces/Work Sans typography and original monochrome Olaryn mark remain unchanged.

Authward uses its own shield-in-O symbol (`assets/authward-mark.svg`, adapted from the Authward repository for dark-mode contrast) and Billing a ledger-in-O symbol (`assets/billing-mark.svg`); both share Olaryn's palette. The product brands Beseam, LemonCrow, and Trevra retain their own accents.

## Light and dark themes

Every page follows the visitor's OS setting and also has a toggle button (top right) that saves an explicit choice in `localStorage` under `olaryn-theme`. `assets/theme.js` is loaded in `<head>` so the saved choice applies before first paint; it sets `data-theme="light|dark"` on `<html>`. In `base.css` the dark tokens exist twice on purpose (OS preference unless light was chosen, and explicit `data-theme="dark"`); change both together. Brand marks are `<use href="/assets/marks.svg#...">` symbols so they follow the page theme rather than the OS (the standalone `*.svg` files are for favicons, social cards and other non-page uses). Without JavaScript the toggle stays hidden and the page follows the OS.

## Local preview and validation

Run at the repository root:

```bash
python3 scripts/check-pages.py
python3 -m http.server 43181 --bind 127.0.0.1
```

Visit `http://127.0.0.1:43181/`, `/authward/`, and `/billing/`. Confirm mobile and desktop layouts, both color modes, links, and focus states. No live deployment occurs just by changing this source branch.

## Social cards

`assets/og/authward.png` and `assets/og/billing.png` are rendered from `scripts/og-card.html`. With the local server running, capture each with headless Chrome at 1200×630, e.g. `google-chrome --headless=new --window-size=1200,630 --virtual-time-budget=4000 --screenshot=assets/og/billing.png 'http://127.0.0.1:43181/scripts/og-card.html?p=billing'`. Bump the `?v=` on the page's `og:image` after regenerating.

## Logo assets

`logo-mark.svg` and `favicon.svg` are the Olaryn source assets. Regenerate the Olaryn PNG favicons, Apple/PWA icons, and Open Graph social image with `python3 scripts/build-brand-assets.py --brand olaryn` (requires Pillow, Node.js, and Playwright/Chromium). Do not edit generated raster assets by hand.
