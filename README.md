# Olaryn

Static site for [olaryn.com](https://olaryn.com), deployed on Cloudflare Pages.

## Pages

| Route | Purpose |
| --- | --- |
| `/` | Olaryn company homepage; keeps the original simple centred layout and “Learning compounds.” wording, with the three infrastructure links |
| `/auth/` | Public Zikela identity developer-focused marketing page |
| `/billing/` | Public Bilyra billing, credits, and usage marketing page |
| `/analytics/` | Public Yeleva analytics overview (the internal analytics application remains separate) |

The marketing pages use ordinary directory `index.html` files. All pages share `/assets/base.css` (self-hosted Inter/Geist Mono `@font-face` rules, every colour token for light and dark, and the shared header, buttons, sections and footer); the home page adds `/assets/home.css` and the product pages `/assets/platform.css`. Change a token once in `base.css`, never per page. Bump the `?v=` on the stylesheet links when a shared stylesheet changes. Fonts live in `assets/fonts/` (Latin subset, OFL) so no third-party font request is made and the CSP can stay `default-src 'self'`.

No framework, backend routes, or dependency installation is needed; the only script is the theme toggle (`assets/theme.js`). The CSP forbids inline styles and scripts, so all styling stays in the stylesheets. Cloudflare Pages serves these as clean URLs. The shared site assets use root-relative paths.

Marketing and platform runtime stay separate:
- Product marketing pages use **Zikela** (identity), **Bilyra** (billing) and **Yeleva** (analytics) at `/auth/`, `/billing/` and `/analytics/`. The Olaryn homepage keeps its original simple layout and copy, in the same theme as the product pages. The Olaryn mark is an inline SVG in the theme's ink colour. The legacy `/authward/` URL redirects to `/auth/`. Backend repositories and service URLs are not renamed as part of this change.
- `https://auth.olaryn.com` remains the OAuth/OIDC issuer and hosts the protected developer portal (`/developer`) and docs (`/docs`). Never proxy, redirect, or rewrite identity protocol endpoints through the marketing pages.
- `https://billing.olaryn.com` remains the service API. There is no public developer signup or pricing page for Billing. The public description must not advertise the private API as open self-service.
- `https://analytics.olaryn.com` remains the analytics service hostname, not a public product marketing page. The public `/analytics/` overview is separate from the application and does not expose a public signup.
- Feature copy must match the Authward and Billing repository contracts. Avoid displaying invented commercial prices or live account balances.

## Brand identity

The site uses one monochrome theme: black, white and greys, with a single green (`--ok`) used only for small status dots. Light pages are `#F9FAFB` with white cards on `#F3F4F6` panels; dark pages are `#090909` with `#111111`/`#181818` panels and cards. Text is Inter (weight 450 body, 400 headings) with Geist Mono for numbers and code. Headings come in two tones: an ink line followed by a grey line at the same size. Buttons are pills: black primary (white in dark mode) and grey secondary. The Olaryn mark is monochrome: black in light mode, white in dark mode (`logo-mark.svg` matches).

The Olaryn mark is an open O with a seed in the gap. Zikela adds a keyhole inside it, Bilyra ledger lines and Yeleva rising bars. The source drawings live in `assets/marks.svg`; pages inline them as `<svg>` so they always load and follow the page theme (copy any change into the pages too). The product brands Beseam, LemonCrow, and Trevra retain their own logos.

Copy rule: product names are only names. Everything else is written in plain, non-technical words, and every claim must match the Zikela and Bilyra repository contracts.

## Light and dark themes

Every page follows the visitor's OS setting and also has a toggle button (top right) that saves an explicit choice in `localStorage` under `olaryn-theme`. `assets/theme.js` is loaded in `<head>` so the saved choice applies before first paint; it sets `data-theme="light|dark"` on `<html>`. In `base.css` the dark tokens exist twice on purpose (OS preference unless light was chosen, and explicit `data-theme="dark"`); change both together. Brand marks are inline SVGs using `currentColor` so they follow the page theme rather than the OS (the standalone `*.svg` files are for favicons, social cards and other non-page uses). Without JavaScript the toggle stays hidden and the page follows the OS.

## Local preview and validation

Run at the repository root:

```bash
python3 scripts/check-pages.py
python3 -m http.server 43181 --bind 127.0.0.1
```

Visit `http://127.0.0.1:43181/`, `/auth/`, `/billing/`, and `/analytics/`. Confirm mobile and desktop layouts, both color modes, links, and focus states. No live deployment occurs just by changing this source branch.

## Social cards

`og-image.png` and `assets/og/{zikela,bilyra,yeleva}.png` are rendered from `scripts/og-card.html` by `node scripts/render-og-cards.mjs` (needs Playwright; set `BRAND_PLAYWRIGHT_PATH` if it lives in another checkout). Bump the `?v=` on the `og:image` URLs when they change.

## Logo assets

`logo-mark.svg` and `favicon.svg` are the Olaryn source assets. Regenerate the Olaryn PNG favicons, Apple/PWA icons and all social cards with `python3 scripts/build-brand-assets.py --brand olaryn` (requires Pillow, Node.js, and Playwright/Chromium). Do not edit generated raster assets by hand.
