# AAA + arifOS site diffs (Q3) — branch `site/claude-2026-10-15`

**Probe basis (live, 2026-10-15 23:1xZ):**
- `curl :8088/health` → `floors_active:13, floors_target:13, floors_pass:16, floors_failing:[]`
- `curl :7072/health` → `transport: streamable-http, tools_listed:122`
- `curl :3001/health` → `status: degraded` (drift field declared `false`); per audit §7 the degraded field is **unspecified which dimension** — that's pending Q7, this diff does not paper over it.

**Branch state:** `site/claude-2026-10-15` exists locally. No `public/` edits applied.

---

## A. AAA site — `sites/arif-fazil.com/public/aaa/`

| # | File | Line | Before | After | Why |
|---|---|---|---|---|---|
| A1 | `aaa/index.html` | 230 | "Kernel health: 2 passed, 4 failed (F2, F11, F12, F13), 10 unmeasured." | "Kernel health — see [arifOS page](/arifos/) for the live row set. Counts here are mirrors of that page." | The **arifos page already holds the canonical floor table**; AAA must link, not duplicate. |
| A2 | `aaa/index.html` | 230 | Static "11:15 Malaysia" stamp with no live probe. | Render last-seen from `/health` `generated_at_utc`. If older than 15 min → render "last seen HH:MM (MYT), STALE — see /health"; never render the stale number as fresh. | Q3 freshness rule. |
| A3 | `aaa/AGENTS.md` | 66–68 (F10–F13 bullets) | Floor definitions repeated. | Replace with "Floor definitions: see [`/arifos/AGENTS.md`](../arifos/AGENTS.md)." | One definer — A1 above. |

No matching `Arif bukan coder` literal in `aaa/` (scoped to this site) — search ran on `aaaa/index.html`, `aaa/AGENTS.md`, `aaa/apps/**/index.html`. The phrasing lives in `about/`, `pilot/`, `institution/`, `words/` — out of Q3 scope; not touching.

## B. arifOS site — `sites/arif-fazil.com/public/arifos/`

| # | File | Line | Before | After | Why |
|---|---|---|---|---|---|
| B1 | `arifos/index.html` | 379 (Verified actor card) | "every irreversible action carries an Ed25519 signature verifiable by an independent verifier." | "Every irreversible action **envelope** carries the cryptographic primitives to sign and verify; **observed calls are unsigned on this probe** (`actor_verified=false` per `arif_init`). The signature surface is in design, not in observed reality." | Q3: wording must state what is actually signed. Probe says: nothing is signed yet. |
| B2 | `arifos/index.html` | 504 (Roadmap item 1) | "Verified actor binding — Ed25519 signed action envelope." | "Verified actor binding — bind Ed25519 on the action envelope; surface currently unsigned." | Honesty. |
| B3 | `arifos/federation.html` | 217 (legend emojis) | "🟢 healthy · 🟡 degraded · 🔴 down · ⬜ unknown" | "green = healthy · yellow = degraded · red = down · grey = unknown" | Q3: remove decorative emoji. Status meaning survives. |
| B4 | `arifos/index.html` | Live status pill (`Connected`) | Constant "Live · 122 tools · arifOS · v2026.07.24" elsewhere; not wired to `/health`. | Render from live `:7072/health` and `:8088/health` on page load. If `/health` stale → "last seen HH:MM (MYT), STALE — see /health". | Q3 freshness rule. |
| B5 | `arifos/federation.html` | floor rows around line 240+ | Floor table is the **single definer** of F1–F13 names + one-line rule. | No change. Confirmed via grep that `aaa/` and `geox/` reference this table rather than redefining. | Q3 one-definer rule verified. |

---

## Freshness threshold (named)

Default `STALE_AFTER_MIN = 15`. Applies to:
- AAA `index.html` live pill
- arifOS `index.html` "Connected" pill and "Kernel health" badge
- Any `🟢` / `healthy` indicator derived from `/health`

When `now - generated_at_utc > STALE_AFTER_MIN`, render the age and stop printing the live value.

---

## Ed25519 scope wording (named)

Ed25519 currently scopes:
- **who**: the actor envelope, only on the verification path under design.
- **what is signed**: nothing observed this probe.
- **what is NOT signed**: every observed public read (`arif_init` returns `actor_verified=false`).

Any future marketing copy that says "cryptographically signed" without a corresponding observed signature is wrong and should be downgraded.

---

## MENUNGGU ARIF

- Apply edits A1–B4 on the local branch and commit.
- Wire a tiny `<script>` that fetches `/health` for each pill, parses `generated_at_utc` and `status`, and renders the freshness-aware version.
- The "What remains open" section stays untouched per queue rule (Qwen owns it).
