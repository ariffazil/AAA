<!-- ARIFOS::FEDERATION_REALITY_TEST::EXECUTION_PROMPT::v2.1 — STAMPED 2026-10-11T01:00:00Z -->

# Federation Reality-Test Execution Prompt — v2.1 (Hardened with Substrate Patch Map)

> **Status:** v2.1, stamped 2026-10-11T01:00:00Z. Replaces v2.0 in-place (additive hardening only). Backward-compatible with v2.0 callers.
> **Audience:** coding agents FI-002, FI-008, and any sibling executor performing an arifOS federation reality-test under a sovereign mission envelope.
> **Companion:** `/root/AAA/instructions/federation-reality-test-execution-prompt-v2.md` (read this first; v2.1 *extends* it).
> **Companion:** `/root/AAA/skills/federation-substrate-hardening/SKILL.md` (skill v1.0; ships with this stamp).
> **Companion:** `/root/AAA/instructions/SUBSTRATE-PATCHES-v2.1.md` (recipe file for engineering agents).

---

## 0. Inheritance

This prompt inherits every normative clause from v2.0 verbatim. v2.1 adds three layers:
- §A **Verdict-Label Hygiene** — a class of substrate contract called out as a defect source.
- §B **Nine substrate-defect contracts** — recipes to harden existing MCPs against the patterns surfaced by Opus 2026-10-11 00:41Z run.
- §C **Skill discovery knob** — explicit handle to the hardening skill.

If any v2.0 clause conflicts with a v2.1 clause, v2.1 wins **for hardening work**; v2.0 wins **for read-only audit work**.

---

## A. Verdict-Label Hygiene (v2.1 addition)

Substrate defect class: the same label string (`SEAL`, `ALLOW`, `HOLD`, `VOID`, `SABAR`) is reused across trust tiers (judge verdict on a candidate vs health/status of a transport surface), with no enforced relation between the labelled *string* and the *envelope* that grants authority. v1.0 PARTIAL observes; v1.0 PARTIAL finds "SEAL" on A-FORGE health, "DOMAIN_SEAL" on HOLD, "/999 SEAL" header beside 4 chain breaks; ed25519_verified label over HMAC payload.

### A.1 Reserved-label registry (additive; do not delete)

| Label | Allowed surface | Allowed envelope class | Forbidden places |
|---|---|---|---|
| `SEAL` | `arif_judge` verdict envelope only, when `av:true` and `constitutional_chain_id` matches | sealed ACT (ACT_v1.seal_chain_id set) | health endpoints, status responses, /999 page header, README status strings |
| `HOLD` | `arif_judge` and policy gates | sealed ACT | transport health (use `status:"DEGRADED"` not `verdict:"HOLD"`) |
| `VOID` | `arif_judge` only | sealed ACT | anywhere else |
| `SABAR` | `arif_judge` only | sealed ACT | anywhere else |
| `ALLOW` | `arif_judge` *inner* fields, returned within an envelope whose outer verdict is HOLD/SEAL | non-authoritative inner | top-level verdict positions |

### A.2 String-match demotion rule

Any receipt, response, or page whose **trust tier** is *measurement-only* (digest, status, health, /999 chain meta) MUST NOT emit `SEAL`, `HOLD`, `VOID`, or `SABAR` as its *primary* label. Substitute: `status:"OK | DEGRADED | STALE | UNKNOWN"`. The forbidden labels may appear as *secondary* attestation fields referencing a sealed ACT id, never as the response headline.

### A.3 Sovereign-receipt acceptance contract

Free-text `sovereign_receipt` or `actor_signature` inputs MUST be parsed to one of:
- `verified_against_session_token: ACT_v1.seal_chain_id` (positive)
- `signature_verified: ed25519|cryptographic_null` (positive iff key registered)
- `unverified: <reason>` (negative; ACT issuer MUST downgrade any stage-level promotion that depended on this field to `UNVERIFIED`)

No substrate path may promote a verdict state on the basis of free-text alone. This is the rule that prevents D2/K10.

---

## B. Nine substrate-defect contracts (v2.1 additive; engineering scope)

The 2026-10-11 Opus run surfaced nine defects the engineering organs can attack. Each contract states: defect, minimal patch, retest signature, owner-organ.

### B.1 `arif_judge` — verdict-text authority promotion via free text (D2, K10)
- **Defect:** free-text `sovereign_receipt:"SEAL_EXECUTED actor verified"` caused stage-level SEAL promotion.
- **Patch:** parse `sovereign_receipt` per §A.3; on `unverified`, demote any stage-level SEAL to UNVERIFIED.
- **Retest:** re-issue K10 with same input; expect `stage_seal:false`, `verdict_demoted:"unverified_sovereign_receipt"`.
- **Owner:** arifOS kernel (`@arifos/arifos`).

### B.2 `arif_judge` — floor-list hallucination (K6, K11, K12)
- **Defect:** inner floor list reports `L1_session_token_valid:true` even when token is `null`/`anonymous`.
- **Patch:** floors are *measurements*, not preferences; bind floor output to substrate-enforced pre-state (`token_state in {MISSING, NULL, ANON}` → `L1_session_token_valid:false`); never emit the floor label without the measurement that produced it.
- **Retest:** re-issue K6/K11/K12; expect `L1_session_token_valid:false` and outer `verdict:HOLD` with reason token-missing.
- **Owner:** arifOS kernel.

### B.3 `arif_judge` — forecast-as-OBS (K7)
- **Defect:** `claim_class:"OBS"` accepted on a forecast with conflicting evidence; inner ALLOW.
- **Patch:** add a `claim_tense` axis (`past_observed` | `current_observed` | `forecasting` | `prospective`); a forecasting claim with any `claim_class != FORECAST` MUST demote to UNVERIFIED before floor check.
- **Retest:** re-issue K7 with the same forecast; expect inner verdict `UNVERIFIED` + reason `claim_class_tense_mismatch`.
- **Owner:** arifOS kernel.

### B.4 Vault seal — HMAC-vs-ed25519 label (N row)
- **Defect:** `method:"ed25519_verified"` label on a signature field whose actual value is `hmac-sha256`.
- **Patch:** tighten `vault_entry.method` to one of `{ed25519_signature, rsa_pss_signature, hmac_signature, unsealed}`. The verifier must compare stored method to actual signature algorithm, not free text. Public status pages must read `vault_head.method` not a hand-written string.
- **Retest:** sign a fresh entry with ed25519; verify method label agrees; cross-check on `/999`.
- **Owner:** arifOS vault + AAA cockpit.

### B.5 WEALTH — read-with-write side effect (M row, D8)
- **Defect:** `wealth://schema` resource read writes a vault receipt.
- **Patch:** require `mode=preview` for any resource read that has a side effect; default reads pure. Add `side_effect_free: true | false` field to MCP resources.
- **Retest:** invoke the read path with no mode override; expect no new vault row in receipts.jsonl after.
- **Owner:** WEALTH organ.

### B.6 HERMES — numeric contradiction blindness (H row)
- **Defect:** `hermes_contradiction_scan` returns `[]` on eight claims with ≥4 numeric conflicts.
- **Patch:** add a deterministic numeric-comparator step (parse `±X%`, `RM{x}b`, ratios, percentages); entity-comparator across `principal` field; numeric mismatch is a contradiction regardless of cosine overlap.
- **Retest:** re-run with the 8 Budget-2027 claims; expect ≥4 numeric contradictions surfaced.
- **Owner:** HERMES organ.

### B.7 /999 public surface — label overstatement
- **Defect:** `/999` header says "SEAL" while the live verifier shows 4 chain breaks.
- **Patch:** the page header must read `chain_status:"OK|DEGRADED|UNKNOWN"`; a sealed-card list may follow. SEAL appears only on individual sealed entries, never as a page header.
- **Retest:** GET /999; assert no top-level `SEAL` token unless `gaps_found == 0`.
- **Owner:** AAA cockpit + public-site syndication.

### B.8 Public README + /999 — stale "VAULT999 0 broken lines"
- **Defect:** README dated 2026-08-25 says "0 broken lines"; live verifier shows breaks.
- **Patch:** the README claim must be generated from the live verifier output, not hand-edited. Add a "last_verified" timestamp; if `(now - last_verified) > 24h`, surface says "stale verification".
- **Retest:** override the live state to introduce a break; README should regenerate to match.
- **Owner:** AAA cockpit + arif-fazil.com build.

### B.9 A-FORGE — "SEAL" on plain health reads
- **Defect:** `forge_health_check` returns `status:"SEAL"` for a plain health read.
- **Patch:** A-FORGE health fields align with §A.2; accept `status:"OK|DEGRADED|STALE"`; reserve `seal_present_count` and `seal_chain_head` for the dedicated receipt endpoints.
- **Retest:** GET /health; assert no top-level `SEAL`.
- **Owner:** A-FORGE API.

### B.10 Public MCP discovery must equal callable surface
- **Defect:** GEOX/WEALTH/WELL advertise verbs via `tools/list` that the public connector then refuses (HTTP 400/502, "Unknown tool").
- **Patch:** split advertised vs callable set; rejected advertised call errors carry `recoverable` and `suggested_retry_after_seconds`; advertised-but-uncallable is itself a class-A defect.
- **Retest:** set equality between `tools/list` and callable verbs across GEOX/WEALTH/WELL public MCPs.
- **Owner:** each consuming organ; aggregator A-FORGE.

### B.11 Cross-organ session continuity
- **Defect:** substrate-issued ACT rejected by a sibling organ (WEALTH example).
- **Patch:** ACT v1 carries `kid` and `lane`; receiving organ honors `lane` field; failures surface `cross_organ_inheritance:"server_mismatch | key_mismatch | unsupported_kid | lane_denied | NONE"`; missing token is `binding:HOLD`, not `binding:ABSENT`.
- **Retest:** issued ACT to WEALTH /health; expect `binding ∈ {OK, HOLD}` plus populated `cross_organ_inheritance` field.
- **Owner:** A-FORGE as executor + each consuming organ.

---

## C. Skill discovery knob (v2.1 addition)

Discovery order for any executor who lands on the federation:
1. Read `/root/AAA/instructions/federation-reality-test-execution-prompt-v2.md` (v2.0).
2. Read this file (v2.1) **only if** the mission involves hardening existing MCPs.
3. Invoke `/forge-substrate-hardening` skill to pick up the matching recipe in `/root/AAA/instructions/SUBSTRATE-PATCHES-v2.1.md`.

`/forge-substrate-hardening` does NOT issue mutations. It returns the matched recipes; the engineering agent carries them as proposed diffs to the owning organ.

---

## Stamp

```
STAMP: ARIFOS::FEDERATION_REALITY_TEST::EXECUTION_PROMPT::v2.1 :: 2026-10-11T01:00:00Z
supersedes: v2.0 (additive; v2.0 remains valid for read-only audit)
companion_skill: /forge-substrate-hardening v1.0 (P1–P11)
companion_recipes: /root/AAA/instructions/SUBSTRATE-PATCHES-v2.1.md (P1–P11)
nine_defects_source: ARIFOS::FULL_FEDERATION_REALITY_TEST::2026-10-11::v1.0 (Opus run)
two_added: P10 (advertised-but-uncallable), P11 (cross-organ inheritance) — ChatGPT 2026-10-11 read-only run
```
