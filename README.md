# Olaryn

Static site for [olaryn.com](https://olaryn.com), deployed on Cloudflare Pages.

## Pages

| Route | Purpose |
| --- | --- |
| `/` | Olaryn company homepage; links to its products and shared infrastructure |
| `/authward/` | Public Authward developer-focused marketing page |
| `/billing/` | Public Olaryn Billing architecture and capabilities page |

The marketing pages use ordinary directory `index.html` files. All pages share `/assets/base.css` (self-hosted Fraunces/Work Sans `@font-face` rules and every colour token, light and dark); the home page adds `/assets/home.css` and the product pages `/assets/platform.css`. Change a token once in `base.css`, never per page. Bump the `?v=` on the stylesheet links when a shared stylesheet changes. Fonts live in `assets/fonts/` (Latin subset, OFL) so no third-party font request is made and the CSP can stay `default-src 'self'`.

No framework, JavaScript, backend routes, or dependency installation is needed. Cloudflare Pages serves these as clean URLs. The shared site assets use root-relative paths.

Marketing and platform runtime stay separate:
- `https://auth.olaryn.com` remains the OAuth/OIDC issuer and hosts the protected developer portal (`/developer`) and docs (`/docs`). Never proxy, redirect, or rewrite identity protocol endpoints through the marketing pages.
- `https://billing.olaryn.com` remains the service API. There is no public developer signup or pricing page for Billing. The public description must not advertise the private API as open self-service.
- Feature copy must match the Authward and Billing repository contracts. Avoid displaying invented commercial prices or live account balances.

## Brand identity

The approved light palette is deep burgundy `#6B3F4B` (accent and editorial headline), parchment `#F5EFE3` (page background), and deep ink `#211E1B` (logo/body text). The dark palette keeps charcoal `#181511` with lighter burgundy `#DBA6B6` for contrast. The Fraunces/Work Sans typography and original monochrome Olaryn mark remain unchanged.

Authward uses its own shield-in-O symbol (`assets/authward-mark.svg`, adapted from the Authward repository for dark-mode contrast) and Billing a ledger-in-O symbol (`assets/billing-mark.svg`); both share Olaryn's palette. The product brands Beseam, LemonCrow, and Trevra retain their own accents.

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
