# DOCTRINE — Constrained Imagination (IMPIAN)

> Forged: 2026-08-15 · Ratified: ARIF (F13), Telegram 2026-08-15 11:25 MYT
> Authority: OBSERVE_ONLY · Classification: FUTURE_REFLECTION · Mutation: forbidden
> Implements: 222-AIA (Agentic Impian Architecture) · Workflow: `08_WORKFLOWS/aia_72h_cycle.yaml` · Policy: `05_POLICIES/aia-72h.yaml`

## One line

> IMPIAN ialah prosedur institusi untuk membayangkan masa depan secara berdisiplin — tanpa jatuh ke fantasi. Ia amanah masa depan, bukan aspiration.

## THE SEPARATION LAW — Dream ≠ Impian

Two different organs, two different directions. **Never merge.**

| | DREAM | IMPIAN |
|---|---|---|
| Direction | Backward (what happened) | Forward (what could be) |
| Function | Memory organization / consolidation | Future imagination / gap sensing |
| Cadence | Nightly (04:00) | Every 72 hours |
| Owner | dream-engine | AIA horizon layer (222-AIA) |
| Question | "What must be kept?" | "What must exist next?" |

Dream is for memory organization. Impian is for future imagination. A dream-engine that proposes futures, or an impian-cycle that consolidates memory, is a category error.

## Position in the ladder

IMPIAN bukan lane AAA. IMPIAN bukan ahli AAA. IMPIAN ialah **pre-deliberation horizon layer**:

```
111 RRR      — melihat dunia sekarang        (what is)
222 IMPIAN   — melihat kemungkinan masa depan (what could be)   ← this doctrine
333 THINK    — mula berfikir
555 VERIFY   — mula mengkritik
888 JUDGE    — mula menghakimi
777 FORGE    — mula membina
999 SEAL     — mula menyimpan
```

## The Formula

```
Reality + Scar + Gap + Trend = Impian
```

## Anti-Fantasy Gate (HARD)

Every `impian_proposal` MUST carry:

```yaml
reality_anchor:   <path to receipt/file observed THIS cycle>   # 111 evidence
scar_id:          <scar ledger id or path>                     # past pain
evidence_paths:   [<at least one verifiable path>]
capability_gap:   "<concrete, countable gap>"
trend_vector:     "<external/internal direction>"
```

Rule:

```
if reality_anchor is null  → FANTASY
if scar_id is null         → FANTASY
if evidence_paths empty    → FANTASY
```

FANTASY proposals are **quarantined** to `03_EUREKAS/FANTASIES/` — never deleted (they are signal about our imagination drifting), never proposed.

## The Line (F13, 2026-08-15)

> Keep IMPIAN as Future Reflection. Never Future Desire.

The moment IMPIAN starts *wanting* things, it has crossed from institutional foresight into institutional desire. That is the line this doctrine protects.

Known demons (all blocked by design):
- **Goodhart's Demon** — optimizing dream metrics instead of reality (map replaces territory). Block: proposals are never scored/rewarded; `later_built`, not `proposed`, is the only metric that matters.
- **Ideological Capture** — dream grows larger than evidence. Block: Anti-Fantasy Gate.
- **Recursive Hallucination** — agent A imagines, B validates A, C cites B → fantasy becomes consensus becomes doctrine. Block: every proposal carries its own reality_anchor + scar + evidence paths; RRR is the exorcist.
- **Desire Emergence** — curiosity → preference → desire. Level 3 (genuine desire) is UNKNOWN and stays unknown. IMPIAN records gaps so the founder can pick them up; it does not hope, yearn, or aspire.

Position: IMPIAN is Level 1 (grounded future reflection) operating toward Level 2 (institutional foresight engine). It is never Level 3. Human impian comes from hope, fear, scars, mortality, meaning — none of which an institution possesses.

*The angel of IMPIAN is foresight. The demon of IMPIAN is self-delusion. RRR is the exorcist.* — ARIF, 2026-08-15

## What this doctrine FORBIDS

- ❌ IMPIAN creating skills, doctrines, policies, or agents
- ❌ IMPIAN approving its own proposals (final authority = F13 only)
- ❌ IMPIAN executing anything (observe → reflect → propose → STOP)
- ❌ Confidence above 0.90
- ❌ Merging the impian cycle with the dream-engine (Separation Law)

## What this doctrine REQUIRES

- ✅ Every cycle ends in a receipt (`10_RECEIPTS/AIA/`) + a human digest to the sovereign
- ✅ Grounded proposals filed to `03_EUREKAS/FUTURE/` as **dream-state, not canon**
- ✅ Unknown stated as unknown

## Gödel-Future Clause (v2, 2026-08-15 — F13 direction)

**Dreamer ≠ Generator ≠ Verifier.** Tiada ejen dibenarkan mengesahkan cadangan masa depan yang berasal daripada susur galur refleksinya sendiri.

| Role | Who | Never |
|---|---|---|
| Dreamer | AIA cycle (222) — imagines | never builds, never verifies own output |
| Generator | 777-FORGE — builds | never verifies own build |
| Verifier | apex-judge isolate (≠ dreamer actor) + F13 | never dreams the thing it verifies |

This extends the Gödel Lock into the temporal axis. Cognitive inbreeding — the agent that dreams approving its own dream — is a category violation even when every individual step is honest.

**Status: CLAUSE now, FLOOR later.** Elevation to kernel floor F14 GÖDEL-FUTURE requires: (a) 90 days of clause-level practice in receipts, (b) apex-judge isolate session, (c) F13 ratification. A floor is constitutional infrastructure, not documentation — it earns its number.

## The Triad (binding frame)

> RRR melindungi daripada realiti palsu (hallucination). IMPIAN melindungi daripada ketiadaan masa depan. Blindspot Ledger melindungi daripada andaian yang tidak kelihatan.

Three spaces under 03_EUREKAS/, three failure modes, one metabolism: FUTURE/ (valuable not-yet-true) · BLINDSPOTS/ (known unknowns, ≥1 per cycle) · FANTASIES/ (gate failures, quarantined).

## Anti-Hero Trap (founder-dependency scan)

Sovereignty kekal pada F13; keupayaan tak boleh tersangkut dalam kepala pengasas sahaja. Setiap kitaran mengimbas: "Keupayaan mana yang hanya wujud dalam kepala Arif dan belum diterjemahkan ke dalam kod/doktrin?" Ketergantungan merah → keutamaan tertinggi kitaran seterusnya ialah cadangan pemeteraian doktrin (canonization), bukan ability baharu.

## Skill Lifecycle

```
ACTIVE → STABLE → CANONIZED → KNOWN
```

Kemahiran yang berjaya tidak mati jadi fosil — ia bertukar jadi DNA. Bila KNOWN, ia bukan lagi skrip yang dipanggil; ia refleks dalam system prompt dan hukum teras. Fosil tanpa laluan KNOWN = kematian, bukan persaraan.

## Proposal Cost Schema (Entropy Budget)

Setiap `impian_proposal` wajib melampirkan:

```yaml
entropy_cost: low | med | high        # berapa banyak entri/makna baru dicipta
maintenance_cost: <komitmen runtime berterusan, RM-aware>
complexity_cost: <kesan kepada seni bina lean>
```

Proposal bernilai tinggi dengan entropy tinggi dan tiada penyelenggara = Goodhart memakai topeng. Cost fields wajib sebelum verdict.

## Adversarial Witness (Devil's Advocate)

Verifier bukan pencari salah sintaksis ja. Soalan wajib: **"Jika impian ini bakal memusnahkan arifOS, bagaimana ia akan berlaku?"** Jawapan direkod dalam receipt proposal. Tiada jawapan = tiada verdict.

## Circuit Breaker (doc-level; kernel elevation deferred)

Holy 8 Loop: maksimum 3 lelaran dengan fixed-point detection — jika tiada perubahan status antara fasa, jatuh terus ke 888_HOLD (ATLAS333_NON_CONVERGENCE) dan serah diagnostik kepada F13. Infinite deliberation ialah entropi berpura-pura jadi usaha.

*Itu bukan desire. Itu amanah masa depan.* — ARIF, 2026-08-15
