# Olaryn

Static site for [olaryn.com](https://olaryn.com). **Production is deployed to the Cloudflare Worker named `olaryn`**, bound to the apex custom domain. The separate `olaryn.pages.dev` Pages project is a direct-upload mirror and does **not** serve `olaryn.com`.

## Pages

| Route | Purpose |
| --- | --- |
| `/` | Company homepage: an independent software business with Beseam, LemonCrow, and Trevra as the primary focus |
| `/auth/` | Reference-style overview of Olaryn Identity (shared sign-in and access) |
| `/billing/` | Reference-style overview of Olaryn Billing (subscriptions, credits, and metered usage) |
| `/analytics/` | Reference-style overview of Olaryn Analytics (visits, activity, and usage) |

The pages use ordinary directory `index.html` files. Each uses `/assets/base.css` for self-hosted fonts, monochrome light/dark tokens, and shared primitives. The homepage adds `/assets/home.css`; the three infrastructure pages share `/assets/infrastructure.css`. Their restrained, documentation-like presentation replaces former product-sales pages, including demo dashboards, pricing/signup prompts, and repeated promotional sections.

There is no frontend framework, backend route, or dependency installation requirement. The only runtime script is the theme toggle (`assets/theme.js`). The CSP forbids inline styles and scripts, so page styling belongs in stylesheets. The Cloudflare Worker serves clean paths; links are root-relative.

## Company and infrastructure boundaries

- **Olaryn** is an independent software company, not a commercial bundle of infrastructure tools. **Beseam, LemonCrow, and Trevra** are the independent customer-facing products. “We build software that compounds” describes the way we operate.
- **Identity, Billing, and Analytics** are shared internal foundations. The three pages under `olaryn.com` are short, *publicly accessible descriptions*, not authenticated documentation or private dashboards. They must not present the systems as open commercial SaaS offerings.
- `https://auth.olaryn.com` remains the OAuth/OIDC issuer and hosts identity developer documentation at `/docs`. Never proxy, redirect, or rewrite identity protocol endpoints through `olaryn.com/auth/`.
- `https://billing.olaryn.com` remains an internal service/API. There is no public self-service billing signup or pricing.
- `https://analytics.olaryn.com` is the analytics service, not a product landing page; `olaryn.com/analytics/` does not expose internal reports.
- Legacy marketing paths redirect to these overviews, but internal repository identifiers and runtime hostnames are not renamed.
- Keep the documentation high-level and safe for public access. Never expose credentials, private dashboards, account data, deployment secrets, or confidential operations details.

## Brand identity

The site uses one monochrome theme: black, white and greys, with a single green (`--ok`) used only for small status dots. Light pages are `#F9FAFB` with white cards on `#F3F4F6` panels; dark pages are `#090909` with `#111111`/`#181818` panels and cards. Text is Inter (weight 450 body, 400 headings) with Geist Mono for numbers and code. Headings come in two tones: an ink line followed by a grey line at the same size. Buttons are pills: black primary (white in dark mode) and grey secondary. The Olaryn mark is monochrome: black in light mode, white in dark mode (`logo-mark.svg` matches).

The Olaryn mark is an open O with a seed in the gap. Olaryn Identity adds a keyhole inside it, Olaryn Billing ledger lines and Olaryn Analytics rising bars. The source drawings live in `assets/marks.svg`; pages inline them as `<svg>` so they always load and follow the page theme (copy any change into the pages too). The product brands Beseam, LemonCrow, and Trevra retain their own logos.

Copy rule: the company homepage should foreground real software businesses; infrastructure pages explain their purpose, responsibilities and service boundaries in factual language. No invented pricing, customer metrics, or exposed internal data.

## Light and dark themes

Every page follows the visitor's OS setting and also has a toggle button (top right) that saves an explicit choice in `localStorage` under `olaryn-theme`. `assets/theme.js` is loaded in `<head>` so the saved choice applies before first paint; it sets `data-theme="light|dark"` on `<html>`. In `base.css` the dark tokens exist twice on purpose (OS preference unless light was chosen, and explicit `data-theme="dark"`); change both together. Brand marks are inline SVGs using `currentColor` so they follow the page theme rather than the OS (the standalone `*.svg` files are for favicons, social cards and other non-page uses). Without JavaScript the toggle stays hidden and the page follows the OS.

## Local preview and validation

Run at the repository root:

```bash
python3 scripts/check-pages.py
python3 -m http.server 43181 --bind 127.0.0.1
```

Visit `http://127.0.0.1:43181/`, `/auth/`, `/billing/`, and `/analytics/`. Confirm mobile and desktop layouts, both color modes, links, and focus states. No live deployment occurs just by changing this source branch; GitHub Actions currently runs validation only.

## Deploying the live website

`olaryn.com` is served by the **Workers static-assets deployment** named `olaryn`; `olaryn.pages.dev` is a separate Pages project. **Pushing GitHub `main` does not deploy the apex domain**. Do not confuse the two deployment targets.

After committing and pushing validated changes, use an authenticated Wrangler session:

```bash
DEPLOY_DRY_RUN=1 bash scripts/deploy-cloudflare.sh
bash scripts/deploy-cloudflare.sh
```

The deployment script packages only tracked public files, checks that the website files are committed, uses `wrangler.jsonc` to retain the existing `olaryn.com` custom domain and Worker preview settings, and deploys to the Worker rather than the Pages mirror. If Wrangler isn't on `PATH`, set `WRANGLER_BIN` to an installed CLI path; otherwise the script uses `npx wrangler@4`.

Cloudflare automatic Git deployment is **not** configured. For unattended deploys, provide a scoped Cloudflare API token through GitHub Actions secrets and add a post-validation deployment job. Never commit credentials or put the local Wrangler OAuth refresh token in GitHub secrets.

## Social cards

`og-image.png` and `assets/og/{identity,billing,analytics}.png` are rendered from `scripts/og-card.html` by `node scripts/render-og-cards.mjs` (needs Playwright; set `BRAND_PLAYWRIGHT_PATH` if it lives in another checkout). Bump the `?v=` on the `og:image` URLs when they change.

## Logo assets

`logo-mark.svg` and `favicon.svg` are the Olaryn source assets. Regenerate the Olaryn PNG favicons, Apple/PWA icons and all social cards with `python3 scripts/build-brand-assets.py --brand olaryn` (requires Pillow, Node.js, and Playwright/Chromium). Do not edit generated raster assets by hand.
