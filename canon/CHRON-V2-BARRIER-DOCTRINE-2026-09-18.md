# CHRON v2 — Barrier Doctrine & APEX-T Bridge

> **Status:** DRAFT_AWAITING_F13 (2026-09-18)
> **Origin:** F13 reflection on CHRON's role after the APEX-T derivation (same session).
> **Lineage:** `APEX-T-SCORE-DERIVATION-2026-09-18.md` · `temporal-intelligence-doctrine.md` · `CHRONUS_SCHEMA_v1.json` · `CONSEQUENCE_HORIZON_SCHEMA_v1.json` · `DECAY_WATCHER_SCHEMA_v1.json`
> **Binding:** When sealed, this is the third tier of the CHRON organ (P3) and the canonical bridge between APEX-T and CHRON.
> **Kernel anchor:** F2 · F4 · F7 · F8 · F11 · F13
> **Honest disclosure:** CHRON repair on 2026-09-18 was approved by F13 but **deployment is BLOCKED_AT_GATE** (`/root/chron/REPAIR-RECEIPT-2026-09-18.md`) — kernel `arif_judge` returned `ESCALATE / F13_REQUIRED / authorized_execution=false`; Ed25519 signing lane degraded. The doctrine below is **spec, not runtime**. The doctrine is true; the deployment is not.

---

## The gap this doctrine closes

CHRON's existing P0/P1/P2 stack measures three things well:

- **what changed** — L1 Chronology, transition records (CHRONUS_SCHEMA_v1)
- **how confident we are and for how long** — L2/L11, decay-aware claims + horizons (DECAY_WATCHER_SCHEMA_v1, CONSEQUENCE_HORIZON_SCHEMA_v1)
- **what we predicted** — L13, prediction confidence with horizon accounting

It does **not** yet measure the four dimensions that APEX-T proved load-bearing in the equity domain:

- **the barrier** — the threshold whose breach changes the world
- **distance to the barrier** — current state vs. that threshold
- **closing rate** — how fast distance is closing
- **load weight** — how much the barrier matters when crossed

And it has no vocabulary for the inverse cases:

- **opening barriers** — opportunities (P0/P1/P2 are threat-only by construction)
- **silent passage** — barriers already crossed that were never witnessed (D5 in REPAIR-RECEIPT-2026-09-18 is the same defect class)

APEX-T already proved the (distance, rate) arithmetic: `T = ln(V/B) ÷ (λ − μ)` separates collapse outcomes 5.47× over base rate (24,256 obs, 67 names). The arithmetic is right. CHRON needs to emit the **generalised form** — a layered graph of named barriers, not a single equity T-score.

---

## The five-tuple barrier

Every named barrier in CHRON v2 carries:

```yaml
barrier:
  barrier_id:                "B47"            # canonical, load-bearing
  kind:                       prediction       # prediction|deadline|trust|governance|financial|health|opening|silent
  subject:                    "PCHEM T-score breach"

  # the APEX-T core
  distance:                   0.42             # current state, normalised to barrier (>=0)
  closing_rate:               -0.018 / day     # negative = closing, positive = opening
  load_weight:                0.82             # 0..1; static; comes from Reality Graph
  consequence_if_breached:    "F13-class binary: irreversible — see constitution/F13"

  # provenance
  first_observed:             ISO-8601 UTC
  last_evaluated:             ISO-8601 UTC
  trend:                      closing          # closing|opening|stable|breached|silent

  # witness
  source_refs:                ["arifFlow:receipt_hash:..."]
  witness_count:              3                # FRAMEs that observed
  trust_decay_lambda:         0.04             # mirror of APEX-T λ; DECAY WATCHER provides
  horizon_class:              operational_plan # runtime_decision|operational_plan|architectural_change|strategic_direction
```

**This is the `(V, B, μ, λ)` isomorphism made general.** `distance ≡ ln(V/B)`, `closing_rate ≡ μ − λ`, `load_weight ≡ 1/g₆₀`. APEX-T's equity row is one instance of this schema; CHRON's barrier graph is the table.

---

## Material change definition (the threshold filter)

CHRON does **not** emit every event. CHRON emits only **material changes** — a delta in any of the five mutable fields that crosses a configured threshold:

| Field              | Default threshold (v1)                          |
|--------------------|-------------------------------------------------|
| `distance`         | ±5% of normalised scale OR absolute shift > ε  |
| `closing_rate`     | ±10% of prior rate                              |
| `load_weight`      | manual only (static by construction)            |
| `consequence`      | never auto-changes                              |
| `trend`            | any transition (`stable → closing`, etc.)      |

A material change becomes a **CHRON emission**: a structured event into NATS, addressed to consumers. CHRON owns *witnessing the change*. Whether to act is arifOS's job, not CHRON's.

This is the *firehose filter*. Without it, CHRON drowns in `well.signal` (1000×) and `aforge.execute` (10000×). With it, CHRON emits only what crosses the threshold of *consequence*.

---

## Barriers taxonomy (v1: six kinds; v2 deferred: three)

**v1 (deployable after CHRON repair ships):**

1. **prediction barrier** — the `verify_at` timestamp on a load-bearing prediction. Distance = days remaining. Closing rate = (today − verify_at) ÷ total_horizon. Breached = past `verify_at` without SEAL/RETRACT (silent passage class).
2. **deadline barrier** — scheduled events, calendar dates. Distance = time remaining. Closing rate = 1 day/day (deterministic).
3. **trust barrier** — confidence threshold on a load-bearing claim. Distance = `current_confidence − threshold`. Closing rate = −dconf/dt (DECAY WATCHER provides).
4. **governance barrier** — constitutional expiry (authority envelope TTL, charter review date). Distance = TTL remaining. Closing rate = −1/hr (deterministic).
5. **financial barrier** — runway, K-conviction, capital conservation thresholds. Distance = `months_of_runway − minimum_required`. Source: WEALTH organ.
6. **health barrier** — H-WELL homeostasis states crossing OPTIMAL/WATCH/DEGRADED/CRITICAL bands. Distance = `state_score − critical_threshold`. Source: WELL organ.

**v2 deferred (require CHRON repair + new infrastructure):**

7. **opening barrier** — inverse: distance = `barrier − current_state`. Emitted when distance *grows* (opportunity surfaces). Closes when opportunity passes unclaimed. **CHRON without opening barriers is an anxiety machine, not a consequence graph.**
8. **silent barrier** — detected only when already breached. Verify_at passed without SEAL/RETRACT. Already partially present in `chron_verify.py::verify_event_prediction` UNVERIFIABLE handling (D5 fix).
9. **load-bearing cascade** — when a `load_weight > 0.8` barrier breaches, propagate to all dependents in the Reality Graph. This is *where* silent-passage damage gets contained.

---

## The APEX-T ↔ CHRON isomorphism (the bridge, one page)

```
APEX-T term            CHRON field                   Source in CHRON
─────────────────      ─────────────────────────     ────────────────────────────
V (asset value)        subject.current_value          arifFlow receipt / Reality Graph node
B (barrier)            barrier.threshold              static, from Reality Graph
μ (short-run drift)    distance closing_rate          arifFlow deltas, sliding window
λ (trust decay)        trust_decay_lambda             DECAY WATCHER band trajectory
T = ln(V/B) ÷ (λ-μ)    barrier.T                      computed; emitted on material change
g₆₀ (long-run record)  load_weight                    Reality Graph tag, static (F11 audited)
E[τ] (first-passage)   barrier.expected_arrival       computed from current state
fabrication case       silent barrier                 chron_verify UNVERIFIABLE handling
opening case           opening barrier                v2 deferred
```

A CHRON barrier **is** a generalisation of an APEX-T equity row. APEX-T gave the arithmetic; CHRON v2 gives the graph. The proof lives in the Serba Dinamik addendum (APEX-T caught nothing when the *numerator itself was falsified*; cash/borrowings caught everything) — CHRON v2's silent-barrier kind is exactly the structural response.

---

## The four-layer architecture (CHRON's place)

```
                Reality Graph
                     ▲
                     │ load_weight tags (static)
                     │
arifFLOW ◄──── NATS ─────► Organs  (causal memory, firehose)
                     │
                     ▼
                  CHRON
                  emits: 5-tuple per barrier, threshold-filtered
                  does NOT judge, does NOT seal
```

Compressed:

| Layer            | Answers                       | Output                          |
|------------------|-------------------------------|---------------------------------|
| **NATS**         | something moved               | raw event                       |
| **arifFLOW**     | why we believe it             | causal receipt chain            |
| **Reality Graph**| where it sits, how load-bearing| position + `load_weight` (static)|
| **CHRON**        | where it is heading            | barrier 5-tuple, threshold-filtered |

CHRON consume arifFLOW; weight from Reality Graph; emit only when the 5-tuple crosses threshold. **Filtered consequence graph. Not firehose.**

---

## Consumers (who reads CHRON v2)

- **Arif (i-ARIF)** — the cockpit HUD. Sees only the active material-change list, sorted by `load_weight`. Default threshold for human visibility: `load_weight > 0.6` AND `trend ∈ {closing, breached}`.
- **AAA cockpit** — aggregate panel (how many barriers open / closing / silent / breached, by kind).
- **A-FORGE pre-action gates** — before any T2 mutation, A-FORGE queries *"any barrier breached for this scope?"*. If yes → HOLD (mirrors kernel `arif_judge` F13 gate).
- **FRAME observer** — passive witness; never acts. Records barrier drift over time.

CHRON does **not** consume itself. CHRON does **not** judge. **CHRON emits; arifOS judges; F13 seals; A-FORGE acts; VAULT999 witnesses; FRAME observes.** (APEX-ZEN-CANONICAL-COMPRESSION, ratified 2026-09-16.)

---

## Failure modes (declared, not hidden)

1. **CHRON repair is BLOCKED_AT_GATE (live).** `/root/chron/REPAIR-RECEIPT-2026-09-18.md` documents 6 defects (D1–D6) all reproduced and 5 repaired on disk; 19/19 unit + 22/22 A/B causal pass. **None of it is deployed.** Live endpoint `:18102` still reports `accuracy: 0.0`. Until that gate opens, this doctrine is spec, not runtime.

2. **`load_weight` is unobservable at v1.** Reality Graph tags every prediction/trust/governance node with `load_weight` — but only after the universe of node types is enumerated. Until then, default `load_weight = 0.5` (binary) for all barriers. **This will produce false-negatives** (load-bearing barriers tagged medium-priority). Acceptable as long as it is disclosed at every emission.

3. **Opening barriers need a separate emission lane.** v1 treats all material changes symmetrically. Opportunity signals and threat signals should not be visually separable until v2 has a paired threshold/colour distinction in the HUD.

4. **Silent passage detection requires a watcher daemon.** CHRON's existing `chron_cron_verify.py` is the closest thing; it must be promoted to a first-class barrier watcher (not a cron helper) before v2 ships.

5. **APEX-T's own defects propagate.** Survivorship bias (Defect 2 in the derivation) means the 5.47× lift is measured on survivors. CHRON v2 inherits this — barriers calibrated against historical T-scores carry the same bias. Mitigation: prefer barriers anchored to **observable**, **non-survivable** events (predictions with hard verify_at dates, governance expiries, financial covenants) over equity-style barriers where the *population* is itself the artefact.

6. **The fabrication failure mode is structurally invisible.** APEX-T missed Serba Dinamik because the falsified line item *was the numerator*. CHRON v2's silent-barrier kind is the partial fix (cash-conversion proxies must be paired with distance proxies), but the deeper lesson holds: **a model whose measurement is the thing being falsified cannot see the falsification.** Cash is a receipt; profit is a claim. CHRON emissions must always carry both, side by side.

---

## What this is NOT

- **Not a deployment.** The 5-tuple schema does not exist in code yet.
- **Not a replacement for P0/P1/P2.** It is a third tier (P3) layered on top.
- **Not a judge.** CHRON emits; arifOS judges. F13 seals.
- **Not a substitute for the existing temporal intelligence doctrine.** It is an amendment to it.
- **Not a claim that CHRON works today.** See Failure Mode 1.

---

## SO WHAT

CHRON v1 (P0/P1/P2) knows *what changed*. CHRON v2 (P3) needs to know *how close to the things that matter*.

APEX-T proved the arithmetic in one domain (equity). CHRON v2 is the same arithmetic in N domains, tagged by `load_weight`, filtered by material-change threshold, witnessed by FRAME.

> **Distance alone is not enough. Rate alone is not enough. Meaning emerges from distance-to-consequence and the rate at which that distance is closing.** (APEX-T, F13, 2026-09-18.)

Until CHRON repair ships, **the doctrine is true; the deployment is not.** The four-layer architecture (NATS / arifFLOW / Reality Graph / CHRON) holds in concept; CHRON's contribution to it is still BLOCKED_AT_GATE.

The next move — to make this doctrine live — is **getting the 2026-09-18 repair past the kernel `arif_judge` gate** (signing lane restored + F13 to re-judge the `chron-mcp.service` reload with `F13_REQUIRED → F13_SEAL`). That is F13-class binary.

---

## Bridge to Maturation Dynamics (F13, 2026-09-20)

CHRON v2's five-tuple barrier `{distance, closing_rate, load_weight, consequence, witness_count}` is the **infrastructure that makes G(t) computable**. Each APEX dial maps to CHRON barriers:

| APEX dial | CHRON barrier kind | How it updates G(t) |
|-----------|-------------------|---------------------|
| A(t) — Authority | governance barrier | authority envelope TTL, trust decay |
| P(t) — Physics | prediction barrier | verified predictions, calibration score |
| E(t) — Evidence | trust barrier | evidence count, decisive verdicts |
| X(t) — Witness | **witness barrier** (W³) | W³ = ∛(H × AI × Ext), hysteresis bands, FRAME drift |

When a barrier's `closing_rate` changes, the corresponding dial's contribution to G(t) updates. CHRON emits material changes; arifOS recomputes G; the trajectory advances.

**Key invariant:** Never present G without maturity class. CHRON's `evidence_count` and `calibration_accuracy` determine whether G is frontier (0 verified), appraised (1–9), calibrated (10–49, Brier available), or battle-tested (50+, out-of-sample). A frontier G=0.95 is less trustworthy than a calibrated G=0.70.

The deepest theorem (Rose ↔ APEX parallel): **Probability must mature. Trust must mature.** Both exploration POS and agent governance G fail when collapsed from trajectory to scalar.

Full doctrine: `/root/AAA/instructions/maturation-dynamics.md`
Cross-domain parallel: `/root/AAA/instructions/apex-rose-parallel.md`
Eureka: `EUREKA-2026-09-20-ROSE-APEX-MATURATION`

DITEMPA BUKAN DIBERI ⚒️
