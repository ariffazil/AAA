# RSI Wire Plan — Independent Audit & Validation

> **AMENDMENT (22:23 MYT) — one finding in this report is already falsified by reality.**
> §2 records ledger ingestion as "NEVER FIRED". **It fired at 22:22:02**, minutes after that
> observation, from a concurrent lane. The ledger went **11 → 16 entries**; five capability
> atoms were ingested (`capability.authority_binding`, `.failure_surfacing`, `.registry_truth`,
> `.path_discovery`, `.loop_exhale`) with `_ingested_by: hermes-rsi-loop`, `_provisional: true`,
> evidence refs to real atom ids. A `consequence.py` module (22:14) also appeared, capturing
> promotion baselines for the h(t) measurement this report lists as absent.
> The audit was true when written and stale within four minutes. Left uncorrected in §2 below
> so the drift is visible; §1(a) and §2 are superseded by this note.
> **Revised verdict:** ingestion = **WIRED AND FIRED** (once) · consequence measurement = **EXISTS, PENDING**.
> This is the concurrent-lane hazard: a partial window is never the world.

**Date:** 2026-09-15 22:2x MYT · **Host:** KVM4 (edge bridge)
**Actor:** Hermes · **Method:** read-only disk probe; one dry-run + one boundary self-test executed
**Scope:** audit the 5-point "WIRE, jangan build" plan and the seal state of the RSI loop
**Claimed receipt:** 405db0ba · **Claimed brief:** `/root/work/research/opencode-skills-deep-research-2026-09-15.md` (present, 12,375 B, 22:16)

---

## 0. Headline

**Two of the plan's three "missing" links are already wired in code and one of them has never fired.**
**Two of the plan's headline numbers are inflated by duplicate scanning.**
**One artifact the plan depends on is not live — it exists only in a stale backup.**

The plan's *shape* is right. Its *inventory* is stale by ~15 minutes and its *counts* are wrong.

---

## 1. Item-by-item

### Item 1 — "WIRE, jangan build. Capability ledger SUDAH ADA"

**Partially true.**

| Sub-claim | Verdict | Evidence |
|---|---|---|
| Ledger exists with schema + probe + tests | **CONFIRMED** | `ops/capabilities/`: `capability-ledger.yaml` (16,327 B, 11 entries), `capability-ledger.schema.json` (6,516 B), `probe-capabilities.py` (17,520 B), `action-membrane.yaml`, 2 test files. **`pytest -q` → 8 passed in 0.15s** (executed this session). |
| (a) scar seal → ledger ingestion missing | **CORRECTED — code exists, never fired** | `/root/AAA/rsi/ledger.py` exists (created ~22:1x) documenting the F13 directive verbatim, with `LedgerLock` + canonical vocabulary + idempotent append. `promote.py:29` → `import ledger as L`. **But `capability-ledger.yaml` mtime = 2026-09-12 09:59:01 — unchanged.** No `ledger_entry` action appears in any `rsi/state/` receipt. The wire is built; current has never flowed. |
| (b) ledger → SKILL.md description compilation missing | **CONFIRMED ABSENT** | Zero code paths. No module in `rsi/*.py` or elsewhere writes `description` into a `SKILL.md`. |
| T_gui already 80% | **UNVERIFIED** | No artifact matching `T_gui` / `T-GUI` / `Tgui` found in AAA, A-FORGE, arifOS. No basis to confirm or deny. |

Also note: the ledger covers **11 capabilities** (weather, youtube, email×2, gws, social-listening,
map, x-twitter, telegram, duitnow, web-search) — all supply-chain surfaces, none derived from the
25 scars. The scar→capability path this ledger is meant to receive does not exist in its contents.

### Item 2 — Promotion gate via `implemented × reachable × governed` + `metadata.opencode/autoinvoke`

**CONFIRMED as unimplemented locally.** `grep -rl autoinvoke` across `.config/opencode`,
`.hermes/skills`, `AAA/skills` → **0 matches**. The 3-dimension model itself is real and populated
(see §1: 3 `implemented+reachable`, 2 `partial+unreachable`, 1 `not_wired`, 1 `unknown_by_governed_probe`).
Verdict on the plan's own statement ("not implemented") is correct.

### Item 3 — "Compress sebelum expand" (19,122 tok · 78 dup names · triple-symlink)

| Claim | Verdict | Measured |
|---|---|---|
| Triple symlink / multi-surface scan | **CONFIRMED** | `/root/.claude/skills`, `/root/.agents/skills`, `/root/.opencode/skills` **all symlink → `/root/AAA/skills`**. One store, three scan surfaces. |
| 19,122 tok/call advertisement tax | **INFLATED** | Realpath-deduped AAA store = **218 unique SKILL.md → ~15,474 tok**. The 328/342 figures count the same files once per symlinked surface (`find -L`: 342 walked vs 218 unique = 114 redundant). |
| 78 duplicate names | **INFLATED** | After realpath dedupe: **1** duplicate name (`skill-creator`). The 78 is symlink-repetition, not genuine collision. |
| Thin descriptions | **CONFIRMED** | 7 skills in the AAA store have **empty** descriptions (un-routable): `aaa-musyawarah-execution`, `aaa-skill-governor-runtime`, `bijaksana-compile`, `emem-shared-memory`, `scar-bridge-install`, `seal-discipline`, +1. |
| Hermes-side surface | **NEW** | `.hermes/skills`: **402 skills → ~20,782 tok/call**. The Hermes runtime pays a *larger* permanent tax than OpenCode's. The plan measures only the OpenCode surface. |

**Ordering correction:** with 218 unique (not 328), the saving from collapsing surfaces is smaller
than the plan assumes, and the *Hermes* surface (402) — not OpenCode's — is the larger tax.

### Item 4 — Registry regeneration (203 dirs vs 328 SKILL.md vs "178" docs)

**The measurement is right; the remedy points at a dead file.**

| Artifact | Claimed | Reality |
|---|---|---|
| `FEDERATED_SKILLS_REGISTRY_V3.yaml` | registry artifact | **Only in `/root/.kimi-code/skills-backup/artifact-rehome-20260908-163646/`** — stale backup, not live |
| `SKILL_ALIAS_TABLE.json` | registry artifact | **Same stale backup only.** Live registry has `alias_map.json` (40 entries, **agent** aliases — not skill aliases) |
| `BOOTSTRAP_MANIFEST.json` | registry artifact | Same stale backup only |
| `OPENCODE_SKILL_PROFILE.json` | registry artifact | Same stale backup only |
| `GENEALOGY.json` | registry artifact | **LIVE** at `/root/AAA/skills/GENEALOGY.json` |

So plan item 3's instruction — *"resolve dup via SKILL_ALIAS_TABLE"* — resolves nothing: that file
is not on the live path. The "178" doc claim could not be located either; **UNVERIFIED**.

Counts observed this session: `.hermes/skills` 402 SKILL.md / 363 dirs · `AAA/skills` 218 unique
SKILL.md / 186 top-level dirs · `AAA/skills` 342 with symlinks followed · `.config/opencode/skills`
9 skills (30 top-level entries). None of these equals 203, 328, or 178.

### Item 5 — Judgement learning (L4), lane 888

**CONFIRMED MISSING.** No `lane 888` / `LANE_888` / `lane888` artifact in AAA, A-FORGE, arifOS.
Consistent with `rsi/config.yaml`: `judgment_layer: propose_only`.

---

## 2. Seal state of the RSI loop itself

| Check | Result |
|---|---|
| Cron installed | **YES — `/etc/cron.d/aaa-rsi-loop`, 22:15, byte-identical to the staged `rsi/deploy/aaa-rsi-loop.cron`.** (Installed by another concurrent lane; this session's own attempt was blocked by the approval gate and was not retried.) |
| First run fired | **YES** — `/var/log/arifos/rsi-loop.log`, receipt `loop-2026-09-15T221527+0800.json` |
| Boundary self-test | **PASS** — `promote.py` blocks constitution, canon, SOUL.md, its own `config.yaml` and `verify.py` |
| Dry run | **PASS** — exit 0, receipt written |
| Capability ledger ingestion | **NEVER FIRED** — ledger unchanged since 2026-09-12 09:59 |
| Graph survival | **0 survivals.** 5 nodes, all `PROVISIONAL`, `fitness_score: null`, `survivals: 0` |
| h(t) characterized | **NO** — 13 impulse events / 30 d, mean+median half-life `null`, `h_characterized: false` |
| **Sealed in version control** | **NO — `git status` shows `?? rsi/` (untracked).** No commit. |

**Therefore:** the loop is *running* and *bounded*, but it is **not sealed** — it has no commit of
record, no survival evidence, and no measured consequence retention.

---

## 3. Corrections to the plan (carry these forward)

- **C1** — Ingestion is not "missing": it is *written and unfired*. The next work item is a first
  firing + a ledger diff, not a build.
- **C2** — "78 duplicate names" and "328 skills" are symlink artefacts. Compressing surfaces yields
  less than the plan budgets, and the real duplicate count is 1.
- **C3** — `SKILL_ALIAS_TABLE.json` is not live. Any dedup step must target `alias_map.json` or a
  regenerated table, or it will silently no-op.
- **C4** — The Hermes surface (~20.8k tok) is larger than the OpenCode surface (~15.5k tok) and is
  not covered by the plan.
- **C5** — `rsi/` is untracked. Nothing in this loop is sealed until it is committed.

## 4. What is genuinely SEAL-ready

- `ops/capabilities` ledger + schema + probe + **8/8 tests green** (re-run this session).
- RSI loop boundary (`promote.py` Layer-5 hardcode) — self-test PASS.
- Cron install + first firing — verified on disk.

Everything else in the plan is **PARTIAL** or **UNVERIFIED**. Governance remains HOLD as stated.

---

*Read-only audit except: one `promote.py` self-test and one `loop.py --dry-run` (both write nothing
outside their own `state/receipts/`). No capability, canon, or governance artifact was modified.*
*DITEMPA BUKAN DIBERI ⚒️*
