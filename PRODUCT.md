# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack
Existing static HTML/CSS/JS on Cloudflare Pages, no framework and no build step. Auto-deploys on push to `main`. CSP forbids inline scripts and styles; fonts are self-hosted.

## Users
Engineers evaluating whether to integrate Olaryn's shared infrastructure into a product (confirmed). They arrive from a link or search, skim for what it is and how it connects, and leave for the docs. The home page also serves anyone checking what the company Olaryn is.

## Product Purpose
Olaryn is a company based in Zürich, Switzerland, behind Beseam, LemonCrow and Trevra and the shared infrastructure they run on. olaryn.com is the company home plus two product pages:
- **Authward** (`/authward/`): identity provider. Passkeys, magic links and social sign-in behind the customer's own login screen; standard OAuth 2.0 / OIDC (Authorization Code + PKCE S256, device authorization RFC 8628, discovery and JWKS, 15-minute revocable JWTs, signing keys rotated every 30 days, exact redirect URIs only). Setup is by pasting one prompt into a coding agent, or via CLI or MCP server. Developer access is by invitation.
- **Tallyward** (`/billing/`): credits, usage and subscription coordination for every Olaryn product. Coordinates Stripe (money) and OpenMeter (access/entitlements). Reserve, settle or release credits. Internal to Olaryn products; no public signup or pricing. "Tallyward" is a display name only: URL, subdomain and the word "billing" as an operational term are unchanged.

## Positioning
Authward: the identity layer the end customer never sees; the product builds its own login, consent and account screens, Authward runs credentials, sessions, tokens and keys behind them, with no proprietary SDK.
Tallyward: credits that are reserved before work and settled after; competing holds are serialized, access follows verified paid invoices, paid actions are idempotent, refunds reverse credits.

## Capabilities and Constraints
- Light and dark themes with a user toggle (persisted in localStorage key `olaryn-theme`, no flash).
- No pink anywhere (explicit user constraint).
- No invented contact address, customer, testimonial, benchmark, pricing or status claim. Authward's "Request access" link points at the live form at `https://auth.olaryn.com/developer/request-access`; do not invent a contact address.
- Tallyward must not claim public availability. Authward must not claim self-serve signup.
- Existing marks in `assets/marks.svg` (olaryn, authward, billing/tallyward ledger-in-O), company logos in `assets/companies/`, favicons and social cards in `assets/og/`.
- Max horizontal fit at 320px; no horizontal scroll; AA contrast in both themes.

## Brand Commitments
Name "Olaryn", tagline "Learning compounds." (home). Product names Authward and Tallyward ("by Olaryn"). Home links to the three companies. Location Zürich, Switzerland.

## Evidence on Hand
- Live and public: `https://auth.olaryn.com/.well-known/openid-configuration` and `https://auth.olaryn.com/docs` (both return 200).
- Source and tests for both products in `../Authward` and `../Billing` (request/response shapes, catalog entries, rules).
- Absent, must not be fabricated: customers, testimonials, screenshots of the developer console, pricing, uptime, benchmarks.

## Product Principles
1. Show the real artifact (live discovery document, real request bodies) before describing it.
2. State only what the code enforces.
3. Fewer words; each page earns its structure from its own product rather than a shared template.
4. The page is a front door to the docs, not a substitute for them.

## Accessibility & Inclusion
WCAG AA contrast in both themes, keyboard focus visible, `prefers-reduced-motion` respected, works without JavaScript except the theme toggle.
