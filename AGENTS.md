# Olaryn Website — Mandatory Design Preservation Rules

**Owner decision (2026-10-18): The site has been redesigned without approval three times. NEVER do it again.**

## Approved designs — do not alter them without explicit owner approval

- **Homepage (/):** the original *minimal centered* one-screen aesthetic. Open-O logo at center, “Olaryn”, **“Learning compounds.”**, short philosophy, three compact infrastructure links, and **Beseam / LemonCrow / Trevra icon logos in the footer**. The visual baseline was restored from Git commit `66b5caa`; the retired infrastructure brand names must NOT return.
- **/auth/, /billing/, /analytics/:** preserve the existing polished original header, stage/demo illustration, core content sections, feature graphics, typography and layout (visual baseline from `844cbfe`). Their copy should describe shared internal Olaryn infrastructure and should not contain redundant SaaS sales pitches. The owner explicitly approved **removal of redundant announcement strips, oversized closing CTA sections, duplicate links and extra footer columns** on 2026-10-18, and only that narrow simplification was incorporated into the locked design. The original visual examples and sections remain protected.
- **A copy request is NOT a redesign request.** If told “reflect the strategy”, “make it internal”, “remove marketing copy”, “simplify”, or “update the landing page,” do **only** the content change. Do not replace cards, page layout, hero, navigation, CSS, diagrams or logo arrangement. Never turn the homepage into a long scrolling text-heavy company site.
- Before any visual/layout change, request the owner's *explicit approval specifying the pages and scope*. Never assume approval based on strategic conversations. User explicitly wants this protection.
- Backend/service hostnames and OAuth routes are not marketing pages; don't change them.

## Mandatory tests

1. Run `python3 scripts/check-pages.py`.
2. Run `python3 scripts/check-design-lock.py`. It verifies **approved DOM layout structure** and **CSS hashes** for all four pages. These checks run in GitHub Actions.
3. Test desktop/mobile and light/dark mode before deploying.
4. **Do not change `design-lock.json` to bypass a failure.** It may be updated *only after explicit owner approval of a visual redesign*. Copy-only changes can leave the design lock intact.
5. If you cannot complete a requested content edit without changing the visual design, stop and ask first.

The Olaryn production site is the `olaryn` Cloudflare Worker serving `olaryn.com`, NOT the separate Pages project. Deploy via `scripts/deploy-cloudflare.sh` only after verification.
