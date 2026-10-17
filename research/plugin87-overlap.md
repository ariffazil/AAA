# plugin87 — pin + overlap map (Q6) — 2026-10-15

## PIN
- **URL:** https://github.com/plugin87/ux-ui-agent-skills
- **HEAD SHA:** `62092bd83bc3df0bcb9a2b3b643305ab11c547da`
- **upstream tag (latest reachable, soft ref):** v2.9.8 (per `package.json`) — **not pinned here**, pin uses commit SHA per queue ("a floating tag is not a version").
- **Captured:** 2026-10-15 23:2x MYT, KVM8.
- **Local clone:** `/root/ux-ui-agent-skills/` (depth=1 shallow).
- **Installed:** no. Per queue "No install."

## What plugin87 actually ships

Three artifacts visible from the clone:

1. **MCP server** — `mcp/server.mjs` (exposed via `bin.ux-ui-mcp`). Self-test in `mcp/selftest.mjs`, gates in `mcp/gates.mjs`.
2. **25 Claude Code skills** — `templates/product-design/CLAUDE.md` + `components/*.md` + `accessibility/*.md` + `design-systems/*.md` + 5 `.claude/rules/*.md` + 1 `.claude/agents/design-critic.md`.
3. **Four hooks** — `hooks/session-start-preflight.mjs`, `posttooluse-fast-gates.mjs`, `stop-require-measurement.mjs`, plus an internal `_ledger.mjs`.

Description from `package.json`: *"Design-system kit for coding agents — DTCG design tokens, 52 components, WCAG 2.2 AA→AAA + i18n/RTL accessibility, enforced single-theme consistency (contrast, hardcode, Tailwind-palette, theme-ref + CI gates), any-framework code, 138 design systems, 52 objective gates."*

## Overlap map vs AAA design canon

Verdict scale: **identical** = byte-equivalent behavior / **partial** = same domain, narrower scope / **duplicate** = same job, plugin87 inferior / **unique** = plugin87 brings new capability not in AAA.

| plugin87 artifact | Domain | Verdict | AAA canonical owner |
|---|---|---|---|
| `mcp/server.mjs` (`ux-ui-mcp`) | design-token + component-spec lint over JSON-LD | **partial** | `forge-design-intelligence` (AAA skills/) — narrower scope (AAA checks tokens, not 52-gate component spec). |
| `components/atoms.md` … `organisms.md` (52 components) | atomic-design system | **partial** | `forge-visual-design-system` (AAA skills/) — AAA covers ~14 components; plugin87 expands to full atomic stack. |
| `accessibility/wcag-aaa.md`, `wcag-checklist.md`, `aria-patterns.md`, `cognitive.md`, `vision.md`, `i18n-rtl.md` | accessibility | **partial** | `forge-design-intelligence` + `forge-visual-qa-w3` — AAA has WCAG checklist only; plugin87 covers 6 sub-topics. |
| `design-systems/crosswalk.md`, `interop-protocol.md` | cross-design-token mapping (138 systems) | **unique** | none in AAA — **keep**, candidate to copy into `forge-design-intelligence`. |
| `templates/product-design/CLAUDE.md` | product-design agent brief | **unique** | none — AAA lacks a full product-design brief. |
| `.claude/agents/design-critic.md` | design-critic agent persona | **duplicate** | AAA `forge-design-intelligence` is the canonical home; plugin87's agent is shorter and not arifOS-aware. |
| `.claude/rules/{components,accessibility,tokens-and-color,brand-and-operations,review-and-research}.md` | 5 path-scoped rules | **duplicate** | AAA `/root/AAA/skills/forge-design-intelligence/SKILL.md` covers the same ground once; plugin87 splits into 5 files. Argue-keep: split is fine. |
| `hooks/session-start-preflight.mjs` | SessionStart design-context probe | **partial** | `arifos-auto-init` (AAA skills/) — narrow, design-only; AAA version is universal. Don't merge. |
| `hooks/posttooluse-fast-gates.mjs` | PostTool design gate | **duplicate** | AAA `forge-design-intelligence` already has gates; plugin87 gates are stricter (single-theme) but narrower. Don't merge. |
| `hooks/stop-require-measurement.mjs` | Stop hook demanding verification | **duplicate** | AAA's `forge-verify-gate` exists for universal verification. Plugin87's design-specific variant is **partial**. |
| `hooks/_ledger.mjs` | local hook ledger | **unique** | none — interesting; review for parity with arifOS PostTool ledger. |
| `bin/cli.js` (`ux-ui-skills`) | design-token CLI | **partial** | `forge-tailwind-tokens` (AAA) covers Tailwind subset. Plugin87 covers non-Tailwind too. |
| `scripts/validate_*.py`, `validate_theme_refs.py`, `check_no_emoji.py`, etc. | 52 design CI gates | **partial** | AAA `forge-visual-qa-w3` covers a subset. Plugin87 has 52. |
| `evals/RESULTS.md`, `evals/briefs/*.md` | eval harness | **unique** | none — `forge-eval-doctrine` could adopt the rig. |

## Where plugin87 is **better** (the honest half, per queue)

- **138-system crosswalk** is not in AAA today; if AAA's `forge-design-intelligence` ever speaks to Figma/Token-Engine, this is the seed.
- **Product-design brief** (`templates/product-design/CLAUDE.md`) is wider than AAA's design scope; useful as a stakeholder brief trigger.
- **52-gate CI** is deeper than AAA's `forge-visual-qa-w3`.
- **Accessibility vertical** (6 sub-files) is wider than AAA's single WCAG file.

## Where plugin87 is **worse** (the honest other half)

- **No arifOS context**. Zero reference to F1–F13, F4 CLARITY, or floor compliance. AAA's canonical skills carry that by default.
- **Hooks duplicate AAA's governance discipline** with weaker coverage. Don't enable in arifOS path.
- **`.claude/agents/design-critic.md`** is a standalone agent; AAA keeps agents inside the constitutional agent schema (333/555/888/999). Plugin87 agent is persona-only.

## Recommendation

- **Pin:** keep `62092bd…` as SOT in `plugin87.pin` (see below).
- **Adopt (import, don't fork):**
  - `design-systems/crosswalk.md` → candidate to fold into `forge-design-intelligence`.
  - `accessibility/` cluster (6 files) → candidate to enrich `forge-visual-qa-w3`.
  - `evals/briefs/*.md` → candidate for `forge-eval-doctrine` rig.
- **Don't enable** the plugin (per queue); AAA owns design canon.

## Pin file (T1, reversible)

Written by hand into `/root/AAA/plugins/plugin87/.claude-plugin/plugin.json` with the SHA declared as `version` value:
```json
{
  "name": "plugin87-pin-ux-ui-agent-skills",
  "version": "62092bd",
  "description": "Pinned commit SHA for github.com/plugin87/ux-ui-agent-skills. Captured 2026-10-15. Not installed; pin only.",
  "repository": "https://github.com/plugin87/ux-ui-agent-skills",
  "head_sha": "62092bd83bc3df0bcb9a2b3b643305ab11c547da",
  "captured_at_utc": "2026-10-15T15:25:00Z",
  "verbatim": false
}
```
