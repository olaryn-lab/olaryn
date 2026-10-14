# Olaryn

Static landing page for [olaryn.com](https://olaryn.com), deployed on Cloudflare Pages.

## Brand identity

The approved light palette is deep burgundy `#6B3F4B` (accent and editorial
headline), parchment `#F5EFE3` (page background), and deep ink `#211E1B`
(logo/body text). The dark palette keeps charcoal `#181511` with lighter
burgundy `#DBA6B6` for contrast. The Fraunces/Work Sans typography and the
original monochrome mark remain unchanged.

Authward uses Olaryn's generated theme from the shared design system, with
white cards on a parchment page canvas and the same 6px corners.
The product brands Beseam, LemonCrow and Trevra retain their own accents.

Review locally with `python3 -m http.server 43181 --bind 127.0.0.1`.
No live deployment occurs by changing this source branch.

## Logo assets

The Olaryn master mark is an abstract compounding loop (not a security
shield). The approved parent palette is burgundy `#6B3F4B` on parchment
`#F5EFE3`, with a corresponding light-burgundy mark for dark mode. The
existing Fraunces wordmark typography is unchanged.

`logo-mark.svg` and `favicon.svg` are the source assets. Regenerate
PNG favicons, Apple/PWA icons and the Open Graph social image with
`python3 scripts/build-brand-assets.py --brand olaryn` (requires Pillow,
Node.js and Playwright/Chromium). Do not edit generated raster assets by hand.
Authward uses a related O-ring symbol with a *shield inside*; its logo
and near-white application canvas live in the Authward repository.
