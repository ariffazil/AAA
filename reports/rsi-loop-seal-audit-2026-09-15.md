# RSI Loop — SEAL AUDIT & VALIDATION

> **Date:** 2026-09-15 · **Host:** KVM8 forge (100.64.0.2)
> **Authority:** F13 SOVEREIGN, verdict PARTIAL-SEAL 2026-09-15
> **Method:** read-only disk probe + live MCP transport probe + boundary self-test
> **Commits:** AAA `7d99544cf` · A-FORGE `a072abe1`

Every number below was measured on disk in this session. Where another lane's
number disagreed, both are recorded — a partial window is never the world.

---

## 1. The seal (what is now committed)

| Artifact | State |
|---|---|
| `/root/AAA/rsi/` (9 modules) | **committed** — running state gitignored, code sealed |
| `/root/AAA/ops/capabilities/capability-ledger.yaml` | **committed** — 11 → 16 entries |
| `/root/AAA/scripts/skill-learn-ingest.py` | **committed** — resolver + dead-letter |
| `/root/A-FORGE` RSI measurement surface | **committed** — 5 files, 1,363 insertions |
| `/etc/cron.d/aaa-rsi-loop` | installed, 2 jobs, syntax-checked |
| Boundary self-test | **PASS** — 8/8 forbidden paths blocked |

---

## 2. Claims audited

### CONFIRMED

| Claim | Evidence |
|---|---|
| Capability ledger already exists (schema + probe + tests) | `ops/capabilities/`: 11 entries, `capability-ledger.schema.json`, `probe-capabilities.py` (17.5 KB), 2 test files, flock writer |
| Ledger validates | `probe-capabilities.py --validate` → **PASSED (16 capabilities)** after ingest |
| Triple symlink surface | `.claude`, `.agents`, `.opencode`, `.codex` → all realpath to `/root/AAA/skills` |
| L4 judgment learning missing | `config.yaml: judgment_layer: propose_only`; no automated ranking write |
| `SKILL_ALIAS_TABLE.json` not on live path | not found under `/root/AAA/skills` |

### CORRECTED (with measurement)

| Claim | Claimed | Measured | Why it differed |
|---|---|---|---|
| Dirty files | 1,142 | **150** (AAA 132, A-FORGE 7, GEOX 8, WELL 2, WEALTH 1, arifOS 0) | — |
| 27 cron disabled | "metabolism inactive" | 27 are Hermes-book jobs in state `migrated`; live metabolism = system crontab **41** + `/etc/cron.d` **35** | `migrated` ≠ dead; they moved to KVM4/system cron |
| Mesh last sync 2026-08-08 (37 d) | stale | probe ran **2026-09-15 03:20**, `mesh-health.json` fresh | read the schedule *in the skill doc*, not the live surface |
| Advertisement tax | 19,122 tok | **15,234 tok** (Hermes 373 skills / 60,938 desc chars); AAA 218 / 54,572 chars ≈ 13,643 tok | realpath dedupe; the 19k figure counted symlinked surfaces twice |
| 78 duplicate names | 78 | **1** (`claude` ×2) | symlink repetition, not collision |
| Empty descriptions | 7 | **1** (`scar-bridge-install`) | the others are YAML block scalars (`description: >`), false positives of a single-line regex |
| Registry drift 203 / 328 / 178 | 3-way drift | dirs **183** · SKILL.md **218** · registry **live**, tracked in git, mtime Sep 15 14:59 | the "registry is backup-only" claim is false — `git ls-files` confirms it |
| `rsi/` unsealed (no commit) | true at the time | **now committed** `7d99544cf` | concurrent-lane audit written before the commit |

### FALSE POSITIVE I CAUGHT IN MY OWN WORK

The RSI-wire audit reported h(t) as "characterized: false / 13 events". Reading
the live tool revealed why: **`forge_rsi_*` was registered but not served** — the
HTTP transport whitelist did not include it, so every call returned
`SESSION_REQUIRED` while `/health` stayed green. Registration ≠ service.

---

## 3. Defects found and fixed this session

All four share one class: **a dead instrument that reported healthy.**

| # | Defect | Measured before | After |
|---|---|---|---|
| 1 | Skill-atom resolver case-sensitive + blind to the live harness root | same atom rejected hourly for **12 days** | queue drained; lesson merged, version 2.0.0 → 2.0.1 |
| 2 | `forge_rsi_*` in `registerRSITools()` but absent from `STATELESS_TOOLS` | every measurement call → `SESSION_REQUIRED` | served; h(t) + FQ readable |
| 3 | `dual-rate-fq` read `ts`, live writer emits `created_at` | governance FQ **0**, window **0**, status **OK** | **10,329 samples**, gov FQ **1.31**, daily **10.4** |
| 4 | Loop maintained a parallel capability registry | DUPLICATE_SOT — the exact pattern the loop detects | **wired into the existing ledger** (flock, surgical append, format preserved) |
| 5 | Layer-1 skill promotion derived `skill_id` from the capability namespace | every Layer-1 promotion dead-lettered — silent no-op | owner map → `FORGE-verify-runtime`; first loop lesson merged |
| 6 | Rejected atoms re-scanned forever, `.rejected` clutter unbounded | 288 re-checks on one atom | dead-lettered to `queue/rejected/` |

---

## 4. Honest state — what is NOT proven

| Item | State | Why |
|---|---|---|
| Capability survival | **0 survivals**, 5 nodes all `PROVISIONAL` | independence is `NOMINAL` — the extractor and verifier are different *names* written by the same author. C1–C3 still hold (C3 re-derives against the live filesystem), so the verdict may assert *"this pattern exists"*; it may not assert *"this pattern was beaten"*. |
| Persistence of consequence | **5 baselines, all PENDING** | first verdict after one 7-day window (≈2026-09-22). Until then the answer to *"what future behaviour changed?"* is **not yet observable**, not "yes". |
| h(t) characterized | **false** — 13 impulse events, half-life `null` | needs ≥5 samples with measurable decay |
| Capability → AAA feedback | **HOLD** | nothing upstream reads the capability graph yet; it is a sink, by design, until F13 says otherwise |
| Governance self-authorization | **HOLD** | unchanged; `FORBIDDEN_PATHS` hardcoded in `promote.py` |

### One governance finding to surface, not hide

The **musyawarah gate** flagged the RSI loop's `Execute` receipts as T2/T3
without a `musyawarah_reference`. The loop declares `risk_class: T0Observe` on
those receipts — verified on disk. So the gate appears to classify by
`step_type` rather than declared risk class. The gate is **DRY-RUN** (6,062
would-have-blocked), so nothing is blocked today. If it flips to enforce, the
RSI loop stops. Recorded here rather than worked around.

---

## 5. Rollback (F1 AMANAH)

| Component | Reverse |
|---|---|
| cron | `rm /etc/cron.d/aaa-rsi-loop` |
| loop code | `git -C /root/AAA revert 7d99544cf` |
| A-FORGE | `git -C /root/A-FORGE revert a072abe1` |
| ledger entries | `git -C /root/AAA checkout HEAD~1 -- ops/capabilities/capability-ledger.yaml` |
| backup | `/root/forge_work/capability-ledger.yaml.bak-20260915-pre-rsi` |

DITEMPA BUKAN DIBERI ⚒️
