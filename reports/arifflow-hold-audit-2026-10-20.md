# arifFlow HOLD audit — 7 actors, measured 2026-10-20 21:56 MYT

**Probe:** `GET http://127.0.0.1:7073/health` + `/var/lib/arifflow/receipts.jsonl` (10,864 receipts)
**Host:** af-forge (KVM8, 100.64.0.2) · service `arifflow.service` pid 3923105, started 21:41:01 MYT
**Verdict of this audit:** the 7 holds are real; the proposed "inject Verify to auto-clear" is
metric fabrication; one hold (chron) is misattributed and would get *worse* under the proposal.

## 1. What the daemon actually reports

```
diagnosis: SIMULATION        verdict: SIMULATION        (top-level, vector constellation)
legacy_verdict: OPTIMAL      legacy_diagnosis: BALANCED (deprecated fossils)
fq.quotient = 0.259259…      rollup_formula: minimum_gated_harmonic_mean
execute_count 37 · verify_count 57 · hold_count 637 · cycle_count 91
```

`fq.quotient = 0.2593` = exactly `7 / 27` — the window ratio of one actor: **hermes-asi**.
`main.rs:541-565` gates the federation scalar to `min(FQ_i)` whenever any executing actor sits
below 0.50. So the entire federation scalar is currently pinned by one actor's ratio.

## 2. The seven holds, with the arithmetic behind each

Per-actor window = last 50 receipts for that actor (`ACTOR_FQ_WINDOW`), quotient per
`invariants.rs:356-360` (`verify_count / execute_count`; `None` if either side is 0),
alias per `:363` (`None → 0.0`).

| actor | wExec | wVer | quotient | held? | honest reading |
|---|---|---|---|---|---|
| hermes-asi | 27 | 7 | **0.2593** | yes | **genuine** — executes 4× more than it verifies in-ledger; this is the actor that pins the federation |
| fi-002 | 12 | 5 | 0.4167 | yes | genuine — below the 0.50 stuck line |
| 333-agi/memory-helix | 9 | 4 | 0.4444 | yes | genuine — below 0.50 |
| codex | 3 | 0 | None→0.00 | yes | genuine in substance — executed 3×, zero verifies |
| grok-build | 1 | 0 | None→0.00 | yes | genuine in substance — executed once, never verified |
| morning-briefing | 2 | 0 | None→0.00 | yes | genuine in substance — executed twice, never verified |
| chron | 2 | 10 | **5.0000** | yes | **misattributed** — chron is verification-dominant (fossilised), not under-verified; it holds only because the enforcer's window saw 0 executes → `None → 0.00` |

## 3. Three claims in circulation, checked

| Claim | Reality |
|---|---|
| "FQ agregat dikunci oleh hermes-asi FQ 0.25 (28 exec / 7 verify)" | **Substantively right.** Live window 27/7 = 0.2593. The "28" is a stale count of one receipt. |
| "Main.rs:548 mengunci FQ agregat" | **Right mechanism**, wrong line: the gate is `541-565` (min-gated harmonic mean, threshold 0.50); 548 is a `None` arm in the filter_map. |
| "Tier 3 = 0" dashboard, "Bukan keputusan untuk Arif. Server tidak jatuh." | **No such dashboard artifact exists on this host.** No file under `/root/AAA/cockpit`, `/root/AAA/observability`, or the HUD scripts renders a 3-tier attention membrane with that text. It is an agent-written narration, not a live surface. Tier-3 count cannot be cited from a nonexistent panel. |

## 4. Why "inject Verify receipts for all 7" is fabrication, not cleanup

1. `/release` is **fail-closed** since 2026-10-20: `requester_id` required, and the release is
   arbitrated by arifOS `888_JUDGE` (`arif_judge mode=intercept`) before the hold is lifted
   (`main.rs:1516-1600`). A script that "just clears holds" has no legitimate path.
2. The only self-service path that works is the **Verify-receipt auto-release in `/ingest`**
   (`main.rs:1533-1535`). So the plan's only viable route is writing verification events that
   did not happen — into a hash-chained ledger that is sealed to VAULT999.
3. For **chron** the proposal is directionally wrong: chron is already 10 verifies / 2 executes
   = 5.0 (verification dominance). Adding Verify receipts drives it further into fossilisation,
   the opposite pole of the same Calhoun sink.
4. The 7 holds are not "blocked work". Five of them are exactly the signal the gate exists to
   produce: work executed with no verification recorded.

## 5. The one real code defect

`invariants.rs:356-363` collapses two different states into one number:

```rust
self.quotient = if self.verify_count == 0 || self.execute_count == 0 { None } else { … };
self.fq = self.quotient.unwrap_or(0.0);   // UNMEASURED and 0.00 become identical
```

Consequence: an actor that has *not executed anything in the window* reads `FQ=0.00` and is
held as if it had verified nothing. `chron` is held on this type error. It is a reporting +
attribution defect (a hold whose stated reason is false), not a reason to loosen the gate:
do **not** auto-release unmeasured actors. Fix = distinguish `UNMEASURED` from `0.00` in the
hold reason and in the aggregate filter; keep the hold.

## 6. What actually clears the holds

- **hermes-asi:** record verifications when verification actually happens. Ratio must reach
  14/27 (0.52) before the min-gate lifts; one Verify receipt only resets
  `consecutive_executes_without_verify`. The debt is behavioural, not scriptable.
- **fi-002, memory-helix:** same rule, smaller gap.
- **codex, grok-build, morning-briefing:** each needs one real verification of its own output,
  then a Verify receipt for that check.
- **chron:** needs the reason corrected to `HELD: FQ=UNMEASURED`, and an F13 binary on whether
  verification-dominant actors hold at all.

## 7. Note on the top-level verdict

`legacy_verdict: OPTIMAL` is a deprecated fossil (`scalar_fq_note` says so in the payload
itself). The live top-level verdict is `SIMULATION` with vector dimension `fq.band =
PATHOLOGICAL`. Raising the scalar past 0.50 would not turn the constellation green; it would
only move one deprecated number. Anyone promising "FQ > 0.50 → kembali hijau/OPTIMAL" is
reading the fossil.

## 8. Root cause found after acting on it (22:00 MYT)

Evidence-window vs hold durability are asymmetric:

- `ReceiptStore::new(1000)` is built empty at startup (`main.rs:1798`) and nothing
  rehydrates it from `receipts.jsonl`. FQ, per-actor counts and the min-gate are therefore
  computed over **ingests since the process started** — here, since 21:41:01.
- Holds are durable by design (`persist_hold_ledger` / `load_hold_ledger`, `main.rs:435-464`,
  added 2026-10-20). So a hold and its reason survive a restart, while the evidence window
  that produced the reason starts again from zero.

Measured proof: three genuine Verify receipts (real audits, payload attached) at 14:00Z moved
the aggregate `0.2593 → 0.3750`, flipped the diagnosis `SIMULATION → STAGNATION` and the
verdict `SIMULATION → FEEL_UNANCHORED`, and *added* a hold: actor `hermes` now reads
`HELD: FQ=0.00` while its own ledger window is 2 Execute / 1 Verify (= 0.50).

Three consequences:

1. The federation scalar is not a stable health measure; it is a function of **time since last
   restart** and of who ingested last. Quoting it without the process start time is meaningless.
2. Any actor that stops emitting receipts drifts to `FQ=0.00` and is held — silence reads as
   failure. This is the same `None → 0.00` defect as §5, now at fleet scale.
3. "Clear the holds" is the wrong question. The honest questions are: does a hold survive the
   evidence that justified it, and does silence deserve a HOLD or a SABAR?

Recommended F13 binary (not applied): after restart, either rehydrate the receipt window from
disk so holds and evidence share a time base, or mark every post-restart FQ as
`WINDOW_SINCE <timestamp>` so nobody quotes a two-minute window as a two-day verdict.

## 9. Audit of the second report ("security theatre") — claim by claim, 22:10 MYT

Second independent report proposed deleting eight things. Six hold, two are wrong, one is
worse than it says. Grounded against live code + payloads.

**1. `verdicts.py:440` — HOLD carries two meanings. TRUE, strongest finding.**
`ToolStatus.HOLD = "HOLD"  # Tool blocked by constitutional gate (NOT governance verdict —
transport block)`. The enum's own comment admits the collision, and its history note says
"Earlier commits incorrectly extended this enum … collapsing transport vs governance
semantics." Proven live: `arif_init` returned `status=HOLD, verdict=OBSERVE_ONLY` (no intent
supplied) and then `status=completed, verdict=HOLD` (intent supplied). The two fields swap
meaning between calls on the same tool.

**2. "Five words for no" — WRONG DIAGNOSIS. They are five different decision types.**
HARAM = two physical irreversible patterns (amanah_gate). BLOCKED = ABI capability/role
resolution failure (kernel_abi). L4_BLOCKED_VERBS = authority-band ceiling
(governance_identity/authority). HOLD = the genuinely conflated one. WAITING_FOR_WITNESS =
defined in `models/verdicts.py` and **emitted nowhere** (`grep` → 0 emitters outside the
definition). Collapsing to two would delete the distinction between physical safety and
authority banding. The one truly removable item here is WAITING_FOR_WITNESS: dead vocabulary.

**3. `arif_init` returns HOLD on a successful bind. TRUE, and sharper than stated.**
Live: `status=completed`, `verdict=HOLD`, but `hold_scope=MUTATION`,
`can_continue_observing=true`, `allowed_next_verbs` = 6 verbs. So the hold is *scoped* to
mutation — the structure is honest. The lie is lexical: the first word an agent reads is HOLD.
Combined with finding 1, the same tool emits three different HOLDs (input-contract,
authority-scope, transport).

**4. `explanation_gate` always empty. TRUE in substance, wrong location.**
0 of 10,965 stored receipts carry `explanation_class` or `explanation_schema`; `refusals: 0`,
`last_violation: null`. The four-field shape `{class, code, outcome, schema}` the report quotes
is built in the **/ingest response** (`main.rs:1289-1294`), not stored on the receipt.
Verdict: dormant gate, never lying — it has simply never been exercised. Deleting it deletes
CM-1 (2026-09-19), whose purpose was to refuse NARRATIVE-class executions.

**5. provenance nulls "on every receipt" — HALF TRUE, and it missed the real ones.**
`witness_organs` non-null on 412/10,965; `formula_version`/`formula_hash` on 86/10,965.
Genuinely always-null: `merkle_root` 0/10,965 and `tri_witness_votes` 0/10,965. Merkle exists
only in the scheduler path, which `arifFlow/AGENTS.md` already documents as dead code at
daemon runtime.

**6. `window_start_utc` holds process uptime — TRUE, one line.**
`main.rs:714`: `start_time.elapsed().as_secs().to_string()`. Live value "941". The field name
says UTC timestamp; the content is seconds since the daemon started.

**7. `legacy_verdict` / `legacy_diagnosis` — TRUE, but the prescription is unsafe.**
`observatory_routes.py:1773-1774` (`_probe_arifflow_fq`, the FLOW PLANE behind the dashboard
screenshot) *prefers* the deprecated band over the live top-level verdict. BUT swapping them
is a category error: the top-level `verdict` is the **vector constellation**
(SIMULATION/STAGNATION/FEEL_UNANCHORED), a different axis from the flow scalar band
(OPTIMAL/BALANCED). The daemon emits no current-axis flow verdict at all — only the deprecated
band. **Correction to §1 of this report: "buang keutamaan tu" would have replaced one category
error with another.** The real question is which axis the FLOW PLANE represents — F13 binary.

**8. `arif_init` withholds `arif_forge` and `arif_seal` — TRUE observation, WRONG prescription.**
`allowed_next_verbs` excludes both for an unverified caller. But forge is already restored by
identity: `authority.py:363-374` grants `LIMITED_MUTATE` + `L4_ALLOWED_VERBS | {"arif_forge"}`
when the actor card declares `adat_agentic.forge.inherited=true`. And `arif_seal` is the one
irreversible write in the system — keeping it out of an OBSERVE_ONLY session matches the
report's own stated principle ("safety is narrow and physical").

**Blocking constraint the report missed: `compute_jcs_body_hash` (`receipt.rs:1033`) hashes the
entire receipt struct.** Deleting `merkle_root`, `tri_witness_votes` or `explanation_class`
from the schema changes the hash of every future receipt and breaks comparability with the
10,965 sealed ones. Those fields may be stopped at the emission/response layer; they may not
be deleted from the struct without a versioned schema migration.

## 10. What was removed, and what it revealed

Applied and verified live (arifFlow commit `1c4339e`, binary deployed to
`/opt/arifflow/bin/arifflow`, backup `arifflow.bak-20261020T2245`, 246 tests passed):

**Removed:** `provenance.window_start_utc = start_time.elapsed().as_secs()` (uptime under a
UTC name). Replaced with a real RFC3339 UTC stamp, a separate `window_age_s`, and
`window_basis: process_lifetime_since_start`.

**Removed:** `"HELD: FQ={:.2}"` formatted off the `None → 0.0` alias. Reasons now carry the
measured counts and say `UNMEASURED` when a quotient cannot be computed. No threshold moved,
no actor released.

**What the new strings immediately exposed — a hold at a healthy FQ:**

```
codex | HELD: FQ=3.00 (execute=1 verify=3)
```

A held actor whose measured quotient is 3.00, six times above the 0.50 gate. The old string,
`HELD: FQ=0.00`, hid this because it printed the stale alias. This is §8's asymmetry proven
in one line: the hold is durable, the evidence that justified it is not. Any hold can now
outlive the state that produced it, and until now the reporting made that unreadable.

`chron` now reads `HELD: FQ=UNMEASURED — window has execute=0 verify=1`, which is true and is
a different fact from "verified nothing".

Post-deploy the top-level verdict moved `SIMULATION → PARTIAL_WIRING` because the vector
dimensions have no post-restart samples yet. That is the same window-lifetime effect, not a
new regression, and it will move again on its own.

**Still open (F13 binaries, not deletions):**
1. Holds durable + evidence ephemeral → does a hold survive a restart at all, or is it
   re-derived from the rehydrated window?
2. Which axis belongs on the FLOW PLANE of the dashboard: the deprecated flow band
   (OPTIMAL/BALANCED) or the vector constellation (SIMULATION/…)? Both are emitted; only one
   is current.
3. `HOLD` carries three meanings on one tool (`status=HOLD` for input contract,
   `verdict=HOLD` for authority scope, transport block). Constitutional vocabulary change.
