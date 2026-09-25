# PHOENIX-72 Cooling Doctrine — The 72-Hour Threshold

> **Status:** F13_ORDER (2026-09-26) — sovereign directive: *"formalize the 72h threshold in cooling doctrine"* + *"reality impact improvement that recursively improve and self heal the entire system, always learning"*
> **Closes:** `FEDERATION_EUREKA_DISTILLATION_REPORT.md` #15 (Verdict: SEAL — "formalize 72h threshold in cooling doctrine", 2026-07-26). Original target `ARIFFLOWKERNELCANON.md` never existed — **this document is its canonical replacement.**
> **Evidence base:** `/root/memory/.archive-2026-07/72-hours-research.md` (644 lines, cross-domain, 2026-05-15)
> **Companions:** `W3-HYSTERESIS-DOCTRINE-2026-09-20` (seal precondition) · `SCAR_AUTHORITY` (cooling = learning) · `CHRON-V2-BARRIER-DOCTRINE` (barrier dynamics) · `COOLING_RECEIPT_SPEC` (measurement envelope) · J-38 Field Propagation eureka (τ half-lives)
> **Kernel anchors:** F2 (truth) · F3 (witness) · F7 (humility) · F8 (metabolism) · F13 (sovereign)
> **Motto:** DITEMPA BUKAN DIBERI ⚒️

---

## 1. The Threshold (normative)

**72 hours is the canonical cooling period between the creation of a candidate and its SEAL or VOID.**

A candidate is anything the system may want to make durable: a memory, an EUREKA, a scar-derived policy, a constitutional amendment, a VOID finalization, a high-novelty verdict. While cooling, it is revisable. After cooling, it is gate-checked, then either sealed or voided. **There is no path to SEAL that skips the clock.**

- **72h is the DEFAULT, not the ceiling.** Risk tiers (`cooldown_engine.py`): `low=24h · medium=72h · high=168h · critical=720h`. Any cooling period shorter than 72h must name its tier and carry the risk justification; silence defaults to 72.
- **Why 72 (evidence, condensed):** three sleep cycles are the minimum unit of systemic biological reorganization — amygdala depotentiation + hippocampal-cortical transfer + HPA-axis recalibration (Sterpenich 2007 fMRI: night-1 sleep loss leaves amygdala reactivity uncooled even after two recovery nights). Convergent boundaries: innate→adaptive immune transition, p53 repair→apoptosis decision, 3-day legal cooling-off, crisis-debrief window. Full evidence with citations: `72-hours-research.md`.
- **Doctrine origin line:** *"Phoenix-72 cooling is the kinetic brake. It prevents High-Speed Error from becoming Immutable Harm by forcing the silicon impulse to wait for the biological heartbeat."* (`000_FOUNDATIONS.md` / `K000_ROOT.md`)
- **Iron law:** *"Truth must cool before it rules — no immediate sealing of critical amendments."* (`000_ARCHITECTURE.md` §Phoenix-72 Law)

## 2. The Seal Precondition (W³, unchanged)

From `W3-HYSTERESIS-DOCTRINE-2026-09-20`:

```
Seal(M) = (t − t₀ ≥ 72h) ∧ (ψ > 0) ∧ W_H ∧ W_AI ∧ W_E ∧ ¬H ∧ ¬V
```

Per-witness minimums: H ≥ 0.42, AI ≥ 0.32, Ext ≥ 0.26 (`056_TRI_WITNESS_SPECIFICATION`). W³ ≥ 0.95 remains the constitutional SEAL gate. The 72h clause is a **necessary, never sufficient** condition: the clock opening does not seal — it only makes sealing *possible*.

## 3. The Cooling Loop — cool → gate → measure → learn → heal → adjust

The threshold is not a timer. It is one turn of a **recursive metabolism** whose output is reality-impact improvement:

```
   CANDIDATE ──[ 72h COOLING · t₀+72h · revisable ]──┐
                                                     ▼
                                          GATE (ψ · W³ · floors)
                                          ┌─────────┴─────────┐
                                        SEALED               VOID
                                          │                    │
                                          ▼                    ▼
   MEASURE ── post-seal reality observation: predicted vs actual (ΔR)
              receipt or falsifiable prediction, within τ window
                                          │
                                          ▼
   LEARN ───── CHRON calibration (Brier/accuracy) · scar ΔS · lesson extraction
                                          │
                                          ▼
   HEAL ────── phoenix72.sh RED(challenge)→BLUE(repair)→GOLD(preserve)
              arifFlow cooling watchdog (60s) · jitu-guard brake on lanes
                                          │
                                          ▼
   ADJUST ──── proposals → arif_judge → (adopt | reject | defer)
              never self-deploy (COOLING_RECEIPT governance.self_deploy = false)
                                          │
                                          └──→ next candidate enters COOL
```

### Loop invariants

1. **Reality impact is measured, not narrated.** A sealed object must acquire at least one post-seal reality observation (receipt, drift measurement, or falsifiable prediction) inside its relevance window. MEASURED outranks DERIVED; a sealed object with zero post-seal observation is not learning — it is stockpiling.
2. **Learning adjusts parameters through governance only.** CHRON lessons and COOLING_RECEIPT improvements route to `arif_judge`. No loop stage edits its own thresholds. The system improves the grammar it is built with only through an external validator — without one, recursion degenerates into self-confirmation (Grammar Doctrine; R ∉ S).
3. **The 72h value itself changes only by F13.** The loop tunes tiers, ψ, W³ bands, decay rates — the threshold is constitutional.
4. **Fail-closed healing.** Missing evidence / authority / rollback → HOLD. The watchdog (`arifflow-cooling-watchdog.timer`, 60s) detects *stalled* cooling and re-runs the phase; it never skips the gate. A corrupt cycle state is backed up and reborn from the sealed baseline, not patched in place (`phoenix72.sh`).
5. **Always learning = every cycle deposits at least one falsifiable record** (episode, prediction, or lesson). Unclassified outcomes and blind lessons count as OPEN debt, not learning.
6. **Cooling is entry-gate; τ is exit-decay.** 72h decides when a candidate *may* become durable. τ half-lives (arifFlow: FEEL=10 · LIVE=10 · MEASURE=100 · WITNESS=250, J-38 eureka) decide when durable content *stops* counting as live evidence. Both are required; neither substitutes for the other.

## 4. Enforcement inventory (live-verified 2026-09-26)

| Mechanism | Location | State |
|---|---|---|
| `COOLING_HOURS = 72` state machine (CANDIDATE→COOLING→SEALED\|VOID, ψ>0, tri-witness) | `arifosmcp/runtime/phoenix_72.py` | **LIVE** — wired via `memory_store.py` |
| `COOLDOWN_DEFAULT_HOURS = 72` + risk tiers 24/72/168/720 | `arifosmcp/core/cooldown_engine.py` | **LIVE** — used by ops/forge/judge/vault/memory tools |
| SABAR cooldown verification window (default 72h) | `arifOS/core/shared/types.py:562` | **LIVE** |
| Memory consolidation, `OnUnitActiveSec=72h` | `arif-dream.timer` (systemd) | **LIVE** — next run 2026-09-27 |
| Reasoning distillation → DreamCandidates, 72h+15m | `arif-dream-distill.timer` | **LIVE** |
| Daily RED→BLUE→GOLD repair cycle, rebirth from sealed baseline | `phoenix72.sh` cron `0 3 * * *` | **LIVE** — cycle PHX-20260924-009, 6 scars |
| Cooling watchdog, 60s stalled-cycle detection | `arifflow-cooling-watchdog.timer` | **LIVE** |
| Calibration (LEARN): accuracy 0.54, Brier 0.21; FULL_LOOP 78,676 episodes | CHRON :18102 | **LIVE** |
| AIA Impian 72h future-imagination + Void rotation "Phoenix 72" (72h full rotation, 3 agents) | Hermes crons | **LIVE** (Dream/Impian separation law, F13 2026-08-15) |
| Ephemeral artifacts auto-purge after 72h unless promoted | `FEDERATION-SUBSTRATE-RULES.md` §85 | **CANON** |

## 5. Shadow — OPEN gaps (honest, not hidden)

| Gap | State | Owner |
|---|---|---|
| `COOLING_RECEIPT` spec is **PROPOSED** — MEASURE stage exists on paper, not in VAULT999 ingress | Spec checklist unimplemented since 2026-07-13 | arifOS vault lane (T3 — needs F13 ack) |
| CHRON `lessons_total=2`, `blind_lesson_share=1.0` — LEARN stage is thin | Loop runs, lessons barely extracted | CHRON loop |
| Theory tier table (`000_ARCHITECTURE.md`: 0h/42h/72h/168h) ≠ code tiers (`cooldown_engine`: 24/72/168/720) | 42h has no code counterpart; 720h missing from theory | theory-doc reconciliation pass |
| `ARIFFLOWKERNELCANON.md` (distillation #15 target) never existed | **Superseded by this document** | closed here |
| **Naming collision:** archived PHOENIX-72 MCP spec (72-tool target) vs living cooling cycle | This doctrine owns the *cooling* meaning; the tool-count spec stays archived as cautionary monument | F10 ontology — resolved by this document |

## 6. Falsifiability — how to attack this doctrine

1. Seal a candidate at t₀+1h → must fail with `cooldown incomplete` (`is_cooldown_complete`).
2. `grep COOLDOWN_DEFAULT_HOURS arifosmcp/core/cooldown_engine.py` → must read `72`.
3. `systemctl cat arif-dream.timer` → must read `OnUnitActiveSec=72h`.
4. A COOLING entry past t₀+72h with `psi_utility ≤ 0` → must VOID, never SEAL.
5. A loop cycle that seals something without a post-seal observation inside its τ window → violates invariant 1 (currently *expected to fail* until COOLING_RECEIPT ships — see §5).

## 7. Compression

```
72h = when reaction becomes commitment.
Silicon memory forms as biological memory forms:
not at the event, but after three nights —
when the charge is gone and only the structure remains.

COOL the candidate. GATE on witness. MEASURE against reality.
LEARN the delta. HEAL the stall. ADJUST through governance.
Never skip the clock. Never self-authorize the loop.
The threshold itself: F13 alone.
```

---

**Receipt:** canonized via canon-mutate cycle (trace `trc-phx72-cooling-20260926`), lock restored, receipt in `/var/lib/arifos/canon_mutations.jsonl`. Distillation #15 status: **EXECUTED 2026-09-26**.

*DITEMPA BUKAN DIBERI ⚒️*
