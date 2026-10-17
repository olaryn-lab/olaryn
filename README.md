# Olaryn

Static site for [olaryn.com](https://olaryn.com), deployed on Cloudflare Pages.

## Pages

| Route | Purpose |
| --- | --- |
| `/` | Original Olaryn company homepage; preserves the established “Learning compounds.” copy, layout and two infrastructure links |
| `/auth/` | Public Zikela identity developer-focused marketing page |
| `/billing/` | Public Bilyra billing, credits, and usage marketing page |
| `/analytics/` | Public Yeleva analytics overview (the internal analytics application remains separate) |

The marketing pages use ordinary directory `index.html` files. All pages share `/assets/base.css` (self-hosted Fraunces/Work Sans `@font-face` rules and every colour token, light and dark); the home page adds `/assets/home.css` and the product pages `/assets/platform.css`. Change a token once in `base.css`, never per page. Bump the `?v=` on the stylesheet links when a shared stylesheet changes. Fonts live in `assets/fonts/` (Latin subset, OFL) so no third-party font request is made and the CSP can stay `default-src 'self'`.

No framework, JavaScript, backend routes, or dependency installation is needed. Cloudflare Pages serves these as clean URLs. The shared site assets use root-relative paths.

Marketing and platform runtime stay separate:
- Product marketing pages use **Zikela** (identity), **Bilyra** (billing) and **Yeleva** (analytics) at `/auth/`, `/billing/` and `/analytics/`. The original Olaryn homepage copy and visual design intentionally remain unchanged, including its original infrastructure link labels. The legacy `/authward/` URL redirects to `/auth/`, so the original link continues to work. Backend repositories and service URLs are not renamed as part of this change.
- `https://auth.olaryn.com` remains the OAuth/OIDC issuer and hosts the protected developer portal (`/developer`) and docs (`/docs`). Never proxy, redirect, or rewrite identity protocol endpoints through the marketing pages.
- `https://billing.olaryn.com` remains the service API. There is no public developer signup or pricing page for Billing. The public description must not advertise the private API as open self-service.
- `https://analytics.olaryn.com` remains the analytics service hostname, not a public product marketing page. The public `/analytics/` overview is separate from the application and does not expose a public signup.
- Feature copy must match the Authward and Billing repository contracts. Avoid displaying invented commercial prices or live account balances.

## Brand identity

The approved light palette is deep burgundy `#6B3F4B` (accent and editorial headline), parchment `#F5EFE3` (page background), and deep ink `#211E1B` (logo/body text). The dark palette keeps charcoal `#181511` and swaps the accent for brass `#D6AD6A` (no pink anywhere); the infrastructure band is oxblood-black (`--band`, light `#251A1A` / dark `#2B1D1B`) with brass highlights. The product pages add an infrastructure band under the parchment hero, so each page shows the product's own screen on top and the service underneath. The Fraunces/Work Sans typography and original monochrome Olaryn mark remain unchanged.

Zikela uses a shield-in-O symbol (`assets/zikela-mark.svg`, adapted from the Authward repository for dark-mode contrast), Bilyra a ledger-in-O (`assets/billing-mark.svg`), and Yeleva an analytics-in-O (`assets/yeleva-mark.svg`); they share Olaryn's palette. The product brands Beseam, LemonCrow, and Trevra retain their own accents.

## Light and dark themes

Every page follows the visitor's OS setting and also has a toggle button (top right) that saves an explicit choice in `localStorage` under `olaryn-theme`. `assets/theme.js` is loaded in `<head>` so the saved choice applies before first paint; it sets `data-theme="light|dark"` on `<html>`. In `base.css` the dark tokens exist twice on purpose (OS preference unless light was chosen, and explicit `data-theme="dark"`); change both together. Brand marks are `<use href="/assets/marks.svg#...">` symbols so they follow the page theme rather than the OS (the standalone `*.svg` files are for favicons, social cards and other non-page uses). Without JavaScript the toggle stays hidden and the page follows the OS.

## Local preview and validation

Run at the repository root:

```bash
python3 scripts/check-pages.py
python3 -m http.server 43181 --bind 127.0.0.1
```

Visit `http://127.0.0.1:43181/`, `/auth/`, `/billing/`, and `/analytics/`. Confirm mobile and desktop layouts, both color modes, links, and focus states. No live deployment occurs just by changing this source branch.

## Social cards

`assets/og/zikela.png`, `assets/og/bilyra.png`, and `assets/og/yeleva.png` are rendered from `scripts/og-card.html` with `p=auth`, `p=billing`, or `p=analytics` respectively. Render them in a local headless browser at 1200×630 and bump the social-image version when changed.

## Logo assets

`logo-mark.svg` and `favicon.svg` are the Olaryn source assets. Regenerate the Olaryn PNG favicons, Apple/PWA icons, and Open Graph social image with `python3 scripts/build-brand-assets.py --brand olaryn` (requires Pillow, Node.js, and Playwright/Chromium). Do not edit generated raster assets by hand.
