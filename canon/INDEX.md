---
registry: canon-INDEX
version: 0.1
compiled_on: 2026-10-11
compiled_by: FI-008 (kimi-code)
authority_resolution: /root/AAA/AGENTS.md → Active Instruction Fragments table
scope: AGENTS.md-cited canon (14 entries)
NOT_scope: filesystem-wide scan (gap: ~196 canon files uncatalogued; pending pass 2)
build_policy: READ-ONLY with respect to existing canon/* — no file moves, no metadata rewrites
seed_principle: One Canon ID, One Active Path
---

# Canon INDEX — Authoritative Registry

**Authority:** ARIF (sovereign). No file in `/root/AAA/canon/` holds operational authority unless listed below with `Status = ACTIVE`.

## Status vocabulary (5-state model)

| Status | Meaning |
|---|---|
| `ACTIVE` | Sealed/ratified, in force. No superseder. |
| `DRAFT` | Pending F13 ratification. Not yet binding. |
| `SUPERSEDED` | Replaced by another `ACTIVE` canon (see `Supersedes` column). History only. |
| `ARCHIVED` | Moved to `/root/AAA/canon/archive/`. History only. |
| `VOID` | Rejected. No authority. |

`SEALED`, `FINAL`, `LATEST`, `v3-final-final` are NOT lifecycle status. They appear as frontmatter metadata or receipts only.

## Status mapping (from legacy AGENTS.md table)

| Legacy phrase | Mapped to |
|---|---|
| `F13_SEAL` | `ACTIVE` |
| `CANONICAL` | `ACTIVE` |
| `F13_RATIFIED_CHAT` | `ACTIVE` |
| `LIVE` / `ACTIVE` (instruction) | `ACTIVE` |
| `ACCOMPANIES-SEAL` / `PARTIAL` / `RESEARCH_RATIFIED_F13_CHAT` | `ACTIVE` (with F13-class binary noted) |
| `DRAFT_AWAITING_F13` | `DRAFT` |
| `DRAFT` | `DRAFT` |
| `PENDING_F13` | `DRAFT` |
| `REPRODUCED+ROOT-CAUSED` (defect exhibit) | `ACTIVE` (companion to doctrine) |

---

## ACTIVE Canon (F13_SEAL / CANONICAL / F13_RATIFIED_CHAT)

| # | ID | File (relative to `/root/AAA/`) | F13 form | Witness | Notes |
|---|---|---|---|---|---|
| 01 | `apx-zen-compression` | `canon/APEX-ZEN-CANONICAL-COMPRESSION.md` | CANONICAL 2026-09-16 | — | Federation end-state: BUILD→VERIFY→JUDGE→SEAL→ACT→WITNESS |
| 02 | `a-z-apex-zen` | `canon/A-Z-APEX-ZEN-DOCTRINE.md` | F13_SEAL via sovereign-chat 2026-09-13 | `reports/SHEBTOC-EXECUTION-RECEIPT-2026-10-04.md` | WAIVED not satisfied; ritual marker only; chain `9932e51830072cb3` |
| 03 | `apx-zen-runtime-vnext` | `canon/APEX-ZEN-RUNTIME-PROMPT-vNEXT.md` | F13_RATIFIED_CHAT 2026-09-20 | — | Runtime prompt; companion to compression canon |
| 04 | `kimi-apx-zen-bootstrap` | `canon/KIMI-APEX-ZEN-BOOTSTRAP.md` | F13_RATIFIED_CHAT 2026-09-20 | — | Session-opener rendering of vNext (no independent authority) |
| 05 | `apx-zen-maint-witness` | `canon/APEX-ZEN-CONSTITUTIONAL-MAINTENANCE-WITNESS-2026-09-20.md` | F13_RATIFIED_CHAT 2026-09-20 | — | External witness on FI-008 maintenance behavior |
| 06 | `petronas-atlas` | `canon/PETRONAS/ATLAS.md` | CANONICAL 2026-09-12 | — | apex-zen SoT for PETRONAS mentions; sub-folder not in this index line |
| 07 | `mail-gateway-spec` | `canon/FEDERATION_GMAIL_GATEWAY_SPEC.md` | F13_SEAL 2026-09-20 | `A-FORGE/bridges/gws_truth_test.py` | ENFORCED_WITH_ROOT_RESIDUAL (11/12); AppArmor binds root where profile attaches |
| 08 | `mail-gateway-quickref` | `canon/MAIL-GATEWAY-AGENT-QUICKREF.md` | F13_SEAL 2026-09-20 | — | Companion to gateway spec |
| 09 | `arch-canon` | `canon/CONSTITUTIONAL-ARCHITECTURE-CANON-2026-09-21.md` | F13_RATIFIED_CHAT 2026-09-21 | `reports/constitutional-architecture-witness-2026-09-21.md` | 11-layer stack; HALAL/SYUBHAH/HARAM; `P(a,S) → {ALLOW,HOLD,DENY}` |
| 10 | `substrate-canon` | `canon/BIJAKSANA-SUBSTRATE-CANON-2026-09-21.md` | F13_RATIFIED_CHAT 2026-09-21 | `reports/bijaksana-substrate-witness-2026-09-21.md` | 64 WAJIB components; 49 HARAM patterns |
| 11 | `commercial-canon` | `canon/COMMERCIAL-SURVIVAL-CANON-2026-09-21.md` | F13_SEAL via sovereign-chat 2026-09-21 | `reports/commercial-survival-witness-2026-09-21.md` | "The assurance is the product"; Layer 1→4 path |
| 12 | `complexity-budget` | `canon/CONSTITUTIONAL-COMPLEXITY-BUDGET-2026-09-21.md` | F13_SEAL via sovereign-chat 2026-09-21 | `reports/constitutional-complexity-budget-witness-2026-09-21.md` | **Canon #0** — rule that holds the rule-writer; ratification order 0→3→2→1→4 |
| 15 | `verdict-vocabulary` | `canon/VERDICT-VOCABULARY-2026-10-11.md` + `canon/verdict-vocabulary-2026-10-11.json` | F13_RATIFIED_CHAT 2026-10-11 | `_registry_2026-10-11/PASS2-REGISTRY-DELTA.md` | 10-state runtime register (HEALTHY/DRYRUN_ACCEPTED/SUCCEEDED/VERIFIED/PARTIAL/SABAR/AUTHORIZED/HOLD/SEAL/VOID); machine-readable JSON + verifier `scripts/verdict_vocabulary.py` + 35-test suite (all passing) |

## DRAFT Canon (pending F13 ratification)

| # | ID | File | F13 form | Notes |
|---|---|---|---|---|
| 13 | `meta-wisdom` | `canon/META-WISDOM-CANON-2026-09-21.md` | DRAFT_AWAITING_F13 2026-09-21 | Canon #4 awaiting ratification order; FI-003 note re precedence |
| 14 | `apx-t-score` | `canon/APEX-T-SCORE-DERIVATION-2026-09-18.md` | DRAFT_AWAITING_F13 2026-09-18 | F13-authored; Merton→Black-Cox derivation; backtest 24,256 stock-months |

---

## SUPERSEDED, ARCHIVED, VOID

*(empty in v0.1 — pass 2 will populate after filesystem scan + supersession markup)*

---

## Known Gaps (pass 2)

- `/root/AAA/canon/` holds ~210 `.md` files; only 14 cited by `AGENTS.md`. **~196 files are uncatalogued** in this index.
- Many `*.bak.*` files exist in canon/ — needs supersession/archival classification.
- `archive/`, `drafts/`, `deltas/`, `research/`, `PETRONAS/` subdirectories not enumerated.
- `/root/AAA/instructions/` indexed separately — not in this canon-INDEX (instructions ≠ canon).

Pass 2 will: grep each uncited `.md` for inbound references, classify into ACTIVE/DRAFT/SUPERSEDED/ARCHIVED, populate this INDEX, and produce the supersession audit.

---

**Maintainer:** ARIF. **Patch author:** FI-008. **Status:** v0.1 draft 2026-10-11.
**Verification:** `/root/AAA/scripts/canon_scanner.py` (read-only lookup).
