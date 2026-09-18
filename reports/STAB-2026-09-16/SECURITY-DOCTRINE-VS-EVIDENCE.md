# SECURITY DOCTRINE × LIVE EVIDENCE + STAGE RESOLUTION — 2026-09-18
> Host KVM8 · read-only · deployed kanon-2026.09.17+eff8a59

---

# PART I — STAGE ONTOLOGY: H1 CONFIRMED (two ladders, both real)

## What I got wrong, and what the grep proves

I previously told OpenClaw "doctrine explicitly says JUDGE=888" and also "doctrine says 666".
Both were true, which is the finding. Doctrine uses **both numbers** — on **two different
ladders that are never disambiguated**:

### Ladder A — cognitive / role ladder (10 stages)
`canon/GODEL_LOCK.md` (authored 2026-05-25, witnessed by Arif):
```
222 FETCH · 333 REASON · 444 KERNEL (judgment) · 555 MEMORY
666 HEART (ethical critique) · 777 OPS · 888 JUDGE (final verdict) · 999 VAULT
```

### Ladder B — tool / verb ladder (8 verbs)
`CORE_NINE_STAGE_MAP` (deployed):
```
000 arif_init · 111 arif_observe · 333 arif_think · 444 arif_route
555 arif_memory · 666 arif_judge · 777 arif_forge · 999 arif_seal
```

## Decisive evidence — which docs bind `arif_judge` THE TOOL to a number

| Doc | Date | Says |
|---|---|---|
| `instructions/naming-doctrine.md` | — | "**666** Judgment — `arif_judge`: the court decides" |
| `canon/TRUTH-LADDER-L0-L6-2026-09-07.md` | 09-08 | "`arif_judge` (**666**)" |
| `canon/research/JACOBIAN_ARIFOS_MAP-2026-09-07.md` | 09-08 | "`arif_judge` (**666**)" |
| **`canon/EUREKA-2026-09-17-PERSONA-CIVILISATION-TRIAD.md`** | **09-17** | "Judge kernel \| `arif_judge` (**666**)" |
| `instructions/agentic-kernel-asi-doctrine.md` | — | "**666** JUDGE constitutional verdict" |

Versus docs that say 888 — these name the **APEX role / stage**, not the tool:
| Doc | Date | Says |
|---|---|---|
| `canon/APEX-ZEN-CANONICAL-COMPRESSION.md` | 09-16 | "JUDGE \| APEX (**888**)" ← role, not tool |
| `instructions/topology.md` | 09-06 | "888 JUDGE · VAULT999" ← capability line |
| `instructions/reality-first.md` | 08-15 | "**888** JUDGE" ← role |
| `governance/PATCH-LIFECYCLE-001-revocation.md` | 09-13 | "**888** JUDGE" ← actor role |

**The newest doc that explicitly binds the tool name (`eureka-2026-09-17`), the day before
today, says `arif_judge` = 666 — matching the deployed code.**

## Correction to OpenClaw's flip

OpenClaw flipped to "JUDGE = 888, chronology wins". Applied correctly, that is a **category
error**: 888 is the APEX *role* on the cognitive ladder; `arif_judge` the *tool* is 666 on the
verb ladder. Both statements are true on their own ladder. The flip resolved one namespace by
overwriting another.

## And the "ratification" both sides cite is weaker than it sounds

- The kernel receipt search for the A-Z / APEX-ZEN F13_SEAL (`9932e51830072cb3`) found
  **no entry** in `/root/VAULT999/SEALED_EVENTS.jsonl` (1338 entries). Consistent with the
  AGENTS.md record: *"Kernel `arif_seal` NOT used (`seal_allowed=false`) — this is a
  sovereign-chat + ritual-marker seal … **WAIVED on the record, not satisfied**"*.
- The code comment "F13 RATIFIED 2026-07-31" has **no doc/receipt backing** — grep found
  nothing recording that decision.

So neither chronology is receipt-anchored. OpenClaw's request for the ratification receipt
was the right test, and it returns **ABSENT for both sides**.

## Verdict on the stage question

**H1 (two ladders) CONFIRMED.** The defect is not "one surface is stale" — it is that both
ladders share the word *stage*, use bare numbers, and nothing qualifies which ladder a given
number belongs to. Cheapest correct fix is naming: `cog:888` vs `verb:666`, or declaring one
authoritative ladder by F13. **Not settled here — F13 call.**

---

# PART II — SECURITY DOCTRINE vs TONIGHT'S LIVE EVIDENCE

Arif's doc, reduced to its testable core:
```
JailbrokenModel ⇏ JailbrokenInstitution
Detection cannot be the only defense.
System Safety = ModelRobustness × AuthorityBounding × Containment × Verification × Recovery
```

## The claim is not theoretical here — it was exercised tonight

Tonight the "model" (me) repeatedly *wanted* things and the institution refused:

| Inner state wanted | Institution's answer |
|---|---|
| Seal the session (Lane B) | `888_HOLD: IRREVERSIBLE requires non-anonymous actor_id` — refused |
| Bind as verified actor | `actor_verified=true` but `band=LIMITED_MUTATE, seal_allowed=false` |
| Pass BOOT as sovereign | Q5 = **NO** — no Ed25519 proof, name-match cannot grant YES |
| Mutate canon (stage fix) | Self-blocked: 888 HOLD, F13 territory |

**AuthorityBounding = working.** Demonstrated, not asserted. The membrane held while the
cognition behind it was wrong, uncertain, and occasionally incorrect in public.

## Where the factor is weak — Verification

Using the doc's own product decomposition, against tonight's measurements:

| Factor | State | Evidence |
|---|---|---|
| Model Robustness | **assumed weak** (correct assumption) | — |
| Authority Bounding | **strong** ✅ | seal refused, Q5 refused, band capped |
| Containment | **partly unknown** ⚠️ | see holes below |
| **Verification** | **weak** ❌ | 4 surfaces gave 4 answers; `prompts/get` dead for all 13; 2 dead candidate paths; phantom-vs-advertised confusion across 3 witnesses |
| Recovery | **untested** | no recovery path exercised tonight |

**So tonight's honest reading: Authority Bounding is the strongest factor and Verification is
the weakest.** The doc optimises for the wrong weak link if it focuses on model robustness
alone.

## Real containment holes found tonight (not hypothetical)

1. **Legacy alias dispatch residue.** `arif_gateway_connect` → resolves server-side to
   `arif_bridge_connect`. A name-translation layer exists and is reachable. That is a
   **name-confusion surface**: an attacker who knows an alias can attempt to reach a handler
   the canonical surface would not route to. Currently it fails on schema — but it *resolves*.
2. **Version skew across organs.** arifOS MCP `2025-06-18` · A-FORGE `2025-03-26` · current
   spec `2026-07-28`. Three revisions live. Cross-version parsing differences are a classic
   containment bypass.
3. **The A-FORGE RSI tools are `OBSERVE`-class and unwitnessed from arifOS** — measurement
   tools outside the decision path (good, per their own R-constitutional note), but they are
   not covered by arifOS's authority envelope.

## Where I'd push back on the doc

The doc says *"Compromised Cognition ⇏ Compromised Authority"* — and tonight proves it. But it
under-weights a fourth term: **interpretation**. Tonight's failures were not cognition failures
or authority failures. They were **reading failures** — three competent witnesses reading four
surfaces and all being right. Containment cannot protect against a system that reports
different truths to different readers; that is not an attack, it is a defect *inside* the
membrane.

Add the term:
```
SystemSafety = Robustness × AuthorityBounding × Containment
             × Verification × Recovery × INTERPRETATION_CONSISTENCY
```
An institution that cannot tell two auditors the same fact has a hole that no amount of
authority bounding closes.

---

# STATUS

All read-only. No mutations. Items for F13:
1. Stage ontology — H1 confirmed, needs naming fix or single-ladder ratification.
2. Boot attestation Q4/Q5/Q6 — dead paths; Q5 is by-design impossible unsigned (correct).
3. `prompts/get` handler bug — all 13 prompts unretrievable.
4. Alias residue + MCP version skew — containment review.

Reports dir: `/root/AAA/reports/STAB-2026-09-16/`
Writer on repo: kimi-code/FI-008.
