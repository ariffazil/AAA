# SEAL RECEIPT v2 — owner-discovery pass: attention-cost receipt + external-action repair

**Date:** 2026-09-16 · **Actor:** HERMES (edge bridge) · **Authority:** F13 SOVEREIGN —
*"now execute all remaining task and seal all"* (follows *"u execute all and seal all … no residual
chaos"*).

**Consequence class (C18):** doctrine-layer documentation + two sensor patches + one table annotation.
Reversible via git. External surface: GitHub **branch** pushes only (no `main`, no PyPI).

**C20 step 0 ran first.** The mission artifact was probed before it was read for content:
`AMBIGUOUS(F13) · REFERENCE(C1-C20)`. Nothing was imported from it; its mission was executed.

---

## 1. Owner discovery — six targets, resolved by probing disk (not by keyword guess)

| Target | Owners found (path) | Verdict |
|---|---|---|
| **attention-cost receipt** | `instructions/sovereign-attention-preservation.md` (W₈₈₈ doctrine) + `agent-output-contract` skill (response shape + word budgets) | **OWNER EXISTS → patched** |
| **consent receipt linkage** | C18 clause (added earlier tonight) + **claim-ledger** MCP (`claim_artifact_register` / `claim_record`) | **OWNER EXISTS → already patched; no new ledger** |
| **W₈₈₈ attention enforcement** | `sovereign-attention-preservation.md` · `attention-kill-criterion.md` (W1-W6) · `human-attention-membrane.md` · `wajib_no_clarify_without_musyawarah.json` (W0-W4 ask-gate) | **SPLIT ACROSS FOUR OWNERS — correct as-is, one fact one owner; nothing to add** |
| **external action rollback** | C18 requires the retraction path *before* the write · `FORGE-incident-triage` (reversible-containment shape, infra scope) | **PARTIAL — declaration owned, procedure missing** |
| **correction / apology / repair** | `public-claims-maintenance` (self-claims repair) · `responsible-disclosure-handling` (inbound correction) · `memory-promotion-gate` + `arif_memory revise/forget` (memory correction) | **OWNED for repo · inbound · memory** |
| **public/external retraction** (email/post/DM already delivered) | **none** | **GAP → proposal only** |

**The finding:** four of the six domains already had owners. The real hole is narrower and more
useful than the artifact assumed — not "no repair capability", but *the one surface where the
damage lands on a human*: an email already sent, a DM already delivered, a post already published.

## 2. EXECUTED — patches to existing owners (zero new skills)

**a. `instructions/sovereign-attention-preservation.md` §5 — Attention-Cost Check.**
W₈₈₈ was declared but unmeasurable, so compliance was a claim, not a witness. Added five questions,
answered **at seal / session-close time, never in a human-facing reply** — the bridge protocol bans
receipts to humans, and a burden label on every message is itself burden. Explicitly states
*length is not the metric*: a long answer is Amanah when the issue is complex; a short one is a
failure when it omits what the sovereign needed to decide. **This is the only change tonight that
touches live behaviour** — additive, receipt-time only, revocable by deleting one section.

**b. `instructions/external-action-repair.md` — NEW FRAGMENT, `DRAFT_AWAITING_F13` (PROPOSAL).**
Law, not a skill (it governs every external write). Seven-step repair sequence
FREEZE → EVIDENCE → ASSESS → REPAIR → NOTIFY → PATCH → RECEIPT, and seven hard rules — the load-bearing
ones being *never repair by substituting a stronger claim*, *an apology admits the specific error,
never general liability*, *freeze before you fix*, *deleting is not repairing*. **Status is a proposal,
not a ratification** — a governance rule invented by the agent in the same turn it noticed the gap is
exactly the "beautiful taxonomy" failure this whole session exists to prevent.

**c. `canon/SYMBOL_TABLE.json` — F13 `known_ambiguity` recorded.** Found while probing our own new
fragment: `F13` carries two live meanings (kernel floor 13 · the sovereign, Arif). The table now says
so, and the probe reports `AMBIGUOUS` instead of guessing. That is a real fact about our own canon,
not a probe defect.

## 3. SENSOR REPAIRED — third false positive, third repair (and the sweep caught the repair's bug)

| Run | What the probe did | Fix |
|---|---|---|
| v1.0 | called a canon-*citing* artifact FATAL | REDEFINED vs REFERENCE split |
| v1.1 | called our own doctrine fragment FATAL for the preposition in *"escalate to F13 **as** a binary ask"* | a single prose mention is not an assignment — redefinition now requires markers across **several** indices |
| v1.2 test | my new regression case expected exit 2; actual 0 | **the chaos sweep's own C12 check caught it** — I corrected the expectation, not the sensor |

Regression suite now **7 cases, 7 passing**, re-run by the chaos sweep on every cycle. The invariant
pinned: a prose citation of a reserved symbol must never be FATAL.

## 4. VERIFICATION (mission-required checks, all run)

```
symbol-probe regression   7/7 pass  (sweep C12 covers it automatically)
skills-census             loadable 409 · shells 45 · diverged 30 · broken_symlinks 0 · WARN
                          witness_hash 72a0e4764ea03d9f  (unchanged — no new skills created)
hermes-chaos-sweep        fail=0 warn=1
mcp-health-census         27 servers · 15 healthy · 8 stdio_present · 4 disabled_intentional · CLEAR
owner-lookup gate         every target above was resolved through it before any decision
kernel FLOOR_TABLE.json   13 floors, F1–F13 — untouched
```

WARN is honest and named: **4 skill names have two live owners** (`FORGE-mcp-testing`,
`RSI-recursive-improvement`, `KERNEL-trinity-33`, `sovereign-recognize`). That is a merge decision,
not a cleanup — HOLD.

## 5. HOLD (unchanged, with reasons)

| Item | Why |
|---|---|
| External-action-repair ratification | proposal only; a new governance rule needs F13, not agent enthusiasm |
| Attention-cost check made mandatory everywhere | it is declared at receipt-time; widening it is a live-behaviour change → F13 |
| 4 duplicate skill owners | ambiguous ownership = human merge |
| `arifOS` main push / merge | fires `07-publish-pypi.yml` (OIDC publish); 3 of 4 local commits touch `pyproject.toml` |
| 45 shells · 431 cross-root collisions · opencode/grok/claude/codex drift | blast radius outside HERMES |
| Kernel `FLOOR_TABLE.json` | F13 only |

## 6. Attention-Cost Check — applied to this very session (first use)

```
1. Did I ask a question I was authorised to resolve myself?   No — mission resolved inward, 0 questions.
2. Reduced to one clean binary, or handed back a menu?        Binary: approve the repair fragment or not.
3. Reading with no decision weight?                           Removed: refused a 3-bundle rename scheme
                                                              whose members already existed.
4. Hidden a risk to keep it short?                            No — kernel refusal, unowned gap, and the
                                                              four duplicate owners are all stated.
5. One clear next action, mine to take?                       Yes: nothing further is blocked on me.
```

## 7. VERDICT

- C17–C20 doctrine-layer: **SEALED** (F13 chat instrument). Kernel path untouched.
- Attention-cost receipt: **EXECUTED as owner patch** (declared, receipt-time, revocable).
- External-action repair: **PROPOSAL ONLY** (`DRAFT_AWAITING_F13`) — the honest state for an unowned
  governance gap. Named, not fabricated.
- Sensors: **repaired + regression-pinned**; census preserves `witness_hash`, proving zero new skills.
- Kernel canon · `arifOS` main · skill-owner merges: **HOLD.**

**Kernel note (unchanged):** `arif_init` issued `OBSERVE_ONLY` (`actor_cryptographically_verified=false`);
`arif_judge` returned **SABAR**, `seal_allowed=false`. This file is a witness record, not a VAULT999
entry. Stated plainly so no one later reads more authority into it than it carries.

DITEMPA BUKAN DIBERI ⚒️
