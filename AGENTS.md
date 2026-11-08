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

## Testing Policy

- Write only high-value tests that catch meaningful bugs, regressions, or security issues.
- Prefer real behavior and integration tests over mocked or implementation-detail tests.
- Avoid trivial, redundant, or coverage-driven tests.
- Run focused tests during development; preserve existing mandatory CI and release checks.

## Agent workflow (mandatory)

- **One task, one worktree.** Start each task with `.githooks/agent-task start <task-id>`. It creates `.worktrees/<task-id>` on branch `agent/<task-id>` from `origin/main`. Work only there: never edit the main checkout, and never share a worktree with another agent.
- **Gate, then land.** Commit, run `make verify`, then `.githooks/agent-task land`. `make verify` runs the checks in `.githooks/verify.rules` that your change touches. `land` rebases onto `origin/main` and pushes to `main`; `git push` runs the same gate on exactly what lands. If a check fails, fix it and land again.
- **Never bypass the gate** with `--no-verify`; only a person may. Report a failure you cannot fix.
- **Clean up.** After landing, run `.githooks/agent-task finish <task-id>` from outside the worktree. It removes the worktree and branch only when every commit is on `origin/main` and no file is modified or untracked; ignored files (dependencies, build output) go with it. `.githooks/agent-task list` shows tasks not yet landed.
- **Never lose work.** Do not force-remove a worktree, discard uncommitted or untracked files, delete unlanded commits, or delete remote branches. Leave other agents' worktrees alone. If you stop before landing, report the worktree and branch that hold the work.
- The desktop runner re-checks `main` after each push. `make verify` also runs `git config core.hooksPath .githooks`, which turns the gate on for the clone.
