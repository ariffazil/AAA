# GOAL-STATE ARTIFACT — VERIFICATION PASS
> 2026-09-20 ~18:25 MYT · KVM8 (forge) · HERMES · read-only · zero mutation
> Source: external artifact describing "Reality-Grounded Adaptive Intelligence Institution"

---

## 1. THE DIRECTION — ACCEPTED, AND IT IS NOT MYTHOLOGY

The one-line target is the strongest thing in the artifact:

> *Reality-Grounded Adaptive Intelligence Institution* — percept, reason, act, learn, correct, **and stop**
> — without confusing capability with authority or its model with the world.

The acceptance suite (21 reality tests) is the most useful part: it turns "build AGI" into falsifiable
conditions — runtime truth, surface truth, identity, authority, time, memory, prediction, calibration,
self-repair, tool evolution, contradiction handling, outcome verification, human sovereignty. The
canonical-mission scenario (inject a harmless defect → full chain → one compact report) is the right
form of proof.

**Nothing in this document contradicts the session's established doctrine.** `Intelligence →
capability`, never `Intelligence → sovereignty`. `Representation ≠ Qualia`. `VOID = R − M_t`.

---

## 2. CONFIRMED — MEASURED LIVE

| Claim | Measured |
|---|---|
| `bab45458` source = built = deployed, drift false | ✅ **exact** |
| temporal anchor live (`clock_source=system_clock`) | ✅ `2026-09-20 18:20:39 MYT` |
| same INIT: substrate HEALTHY vs effective state DEGRADED | ✅ `substrate_state: DEGRADED` + `authority_band: LIMITED_MUTATE` |
| WELL registry drift | ✅ `intended 10 / registered 40 / exported 19 / callable 10 / unexpected_public 9` → `REGISTRY_DRIFT` |
| WELL machine substrate noisy (~80% swap) | ✅ **81.2%** (6652/8191 MB) · 4 zombies |
| CHRON: 19 active predictions, 0 verified, 0 lessons | ✅ exactly |

---

## 3. ★ FALSIFIED — REPEATED FROM THE EARLIER ARTIFACT (2nd AND 3rd TIME)

Both were already disproven in `SURFACE-TRUTH-CENSUS.md`. They persist in this new document.

**"WEALTH's registry call is blocked because its session requirement cannot be satisfied."**
With the standard MCP handshake it returns data and mints a receipt:

```
capital_registry → receipt_id 5f7180ad-2905-40d3-9367-304b1693e9fe
                   call_status: DEGRADED
```

**"GEOX's advertised registry tool is rejected by its own runtime guard as noncanonical."**
The earlier failure was `MCP_LIFECYCLE: tools/call rejected until client sends
notifications/initialized` — a handshake step, not a guard. GEOX exposes **27 tools**.

**"WELL's advertised `well_system_registry_status` returns Unknown tool."**
Name error — that string is **not in WELL's advertised list** (`grep -c` = 0). The real tool is
**`well_registry_status`**, and it works: it returned the full drift report quoted in §2 above.

**Pattern:** the same three claims have now survived two independent correction passes without being
updated. A document that repeats a falsified measurement is not a measurement — it is a claim with a
stale denominator.

---

## 4. ★★ NEW — H6 REPRODUCED, INDEPENDENTLY, AND WORSE THAN DESCRIBED

The artifact said HERMES "classified the future AGI state as *already achieved* as KNOWN even though
the supplied evidence contradicted that claim."

Reproduced on `127.0.0.1:18087` (`hermes_claim_validate`), claim = *"The arifOS federation has
achieved the future AGI target state"*, with **six** contradicting evidence items:

```json
"claim_id": "hc-9a3621ca",
"epistemic_state": "UNKNOWN",
"evidence": [... 6 items, all contradicting ...],
"confidence": 0.2,
"verdict": "PASS",                    ← PASS
"violations": [],                     ← ZERO violations
"permitted_statement": "[UNKNOWN/UNKNOWN] The arifOS federation has achieved ..."
```

Three defects in one payload:

1. **`verdict: PASS` with `violations: []`** while the claim is directly contradicted by the evidence
   supplied in the same call. `EPISTEMIC_STATE=UNKNOWN` is correct; `PASS` is not.
2. **`permitted_statement` still emits the claim** — hedged, but stated. A contradicted claim is not
   "permitted with an UNKNOWN prefix."
3. **Principal misparse:** `"principal": {"identity": "The", "type": "PERSON"}` — the parser split the
   sentence and typed the article **"The"** as a PERSON. Same family as the H2 "pekerja → bank" defect.

Root defect unchanged from 2026-09-18: **`claim_validate` returns PASS when evidence opposes the claim.**
The verdict field is not wired to the evidence array.

---

## 5. NEW — THE FEDERATION'S OWN "SURFACE TRUTH" PROBLEM, IN HERMES

The artifact asserts *"HERMES has a clean registry."* There is no single HERMES surface to be clean.
Four MCP ports are live on KVM8, each exposing a **different** tool set:

| Port | Tools | Identity |
|---|---|---|
| 18084 | 1 (errored) | — |
| 18086 | 8 | FRAME (`frame_*`) |
| 18087 | 13 | HERMES rasa (`hermes_claim_validate` …) |
| 18088 | 6 | session federation (`session_*`) |

So "HERMES" resolves to at least **four independent surfaces with disjoint contracts**. A registry
verdict on one says nothing about the others — this is precisely
`Declared ≠ Registered ≠ Exposed ≠ Callable` inside the federation's own house, and it is why the
earlier artifact's HERMES conclusions and mine disagreed without either being wrong.

---

## 6. WHAT I DID NOT VERIFY

- "arifOS returned HOLD when asked to simulate the target state" — **UNMEASURED**.
- Authority `OBSERVE_ONLY` — I measured `LIMITED_MUTATE` in the same call the artifact calls
  OBSERVE_ONLY. Different session context; **UNMEASURED which is canonical**.
- "unhealthy containers" — swap and zombies confirmed; the container-health term was **not** measured.
- CHRON "54,100 episodes / 5 verify / 1 learn" — read earlier at 54,100; not re-baselined this pass.

---

## 7. THE CONSEQUENCE

The goal-state document is **directionally right and operationally stale in the same places as the
last one.** Its architecture section should be kept; its organ-findings section should be discarded
and re-measured, because three of them are wrong in a way that misdirects work — two of them propose
fixing contracts that already work.

The genuinely new, actionable finding is §4: **`hermes_claim_validate` returns PASS on a claim its own
evidence array contradicts.** That is a live P0 in the truth layer, reproducible in one call, and it is
exactly the failure mode the whole architecture exists to prevent — *the system asserting more than its
evidence supports.*

---

## 8. STATUS

**Mutations: ZERO.** Read-only probes + one reproducible function call + this file.
No federation change. No canon change. No seal. No signature.

`arif_seal` not invoked. **NO SESSION SEALED.**
