---
name: reality-impact-schema
version: 1.1.0
status: DRAFT_AWAITING_F13
spectrum: 000-555
floors: [F1, F2, F4, F5, F7, F9, F13]
provenance:
  origin: F13 directive 2026-09-25 (Sovereignty Cron synthesis)
  prior_art: representation-reality-invariant.md (DRAFT 2026-09-18)
  scar: SCAR-2026-09-12-phantom-cron-category-error
trigger: |
  When any cron emits a "reality impact" assertion, claim of consequence,
  or score that ranks an agent/system output as valuable. Replaces bare
  witness-count metrics that conflate activity with production.
related:
  - authority-claim-graph-schema-v1.0
  - contradiction-ledger-schema-v1.0
  - reality-debt-audit-v1.0
  - claim-lifecycle-states
  - carry_forward.open_questions
purpose: |
  Force every consequence claim to declare:
    1. WHICH class of reality it touched (R1-R5)
    2. WHERE the change came from (reality_origin + attribution)
    3. WHO witnessed it independently (not the producer's own log)
  Prevents "audit about audit" — the failure mode where reality-impact
  scoring becomes theatrical cognition with cosmetic precision.

  Failure example that birthed this schema:
    Reality Impact Score = 0.83, Witness Count = 14, Consequences = 7
    → all green, but no decision changed, no revenue produced, no human
    bond preserved, no scar closed. Pure receipt accumulation.

  THEATRICAL verdict is the maturity test. Schema MUST be willing to
  emit THEATRICAL against its own producer's output. That is the test
  of constitutional maturity.
---

# REALITY_IMPACT_SCHEMA v1.1 — Reality Class & Attribution

> **Tangkap dalam BM Penang:**
> "Mutation bukan Consequence. Commit dibuat bukan bukti nilai tercipta.
> Skema ini paksa setiap dakwaan impak mengaku: kelas realiti yang disentuh,
> dari mana perubahan datang, dan siapa witness yang bukan diri sendiri."

---

## Part 1 — Reality Class (R1-R5)

Setiap perubahan reality mesti dikelaskan dalam **SATU** kelas, hierarki
yang ketat (lower tidak boleh skip ke higher):

| Class | Nama Pendek | Apa yang berubah | Contoh |
|------:|-------------|------------------|--------|
| **R1** | `file_change` | Bit/byte di filesystem | commit, edit, symlink, log rotate |
| **R2** | `system_state` | Service/process/resource | restart, deploy, quota update, memory freed |
| **R3** | `capability` | Federation boleh buat benda baru | new skill wired, organ promoted T2→T1, MCP server live |
| **R4** | `human_behavior` | Tingkah laku manusia berubah | Arif sleep lena, Syed maintained, decision reversed, query reduced |
| **R5** | `world_consequence` | Dunia fizikal/ekonomi berubah | RM saved, decision shipped, contract landed, risk avoided |

### Hierarchy rules (strict)

```
R5 ⊃ R4 ⊃ R3 ⊃ R2 ⊃ R1
```

- Mengubah **R5** secara automatik melalui R4, R3, R2, R1 (consequence chain).
- Mengubah **R4** secara automatik melalui R3, R2, R1 (behavioral chain).
- Mengubah **R3** melalui R2, R1 (capability chain).
- Mengubah **R2** melalui R1 (system chain).
- **R1 sahaja** = TIDAK propagate ke atas. Itu THEATRICAL signature.

### Class attribution evidence (minimum per class)

| Class | Minimum independent witness |
|------:|------------------------------|
| R1 | `git log -1 --format=%H` atau sha256 fail selepas write |
| R2 | probe port/process dari PID external (`systemctl show`, `curl :PORT/health`) |
| R3 | probe capability invocation log (organ lain, bukan producer organ) |
| R4 | human_state carry_forward delta atau open_question resolution event |
| R5 | independent financial/contractual/world record (filer, vendor, market) |

> ⚠️ **Producer's own log is NEVER acceptable witness** untuk R3+.
> Itu `echo reporting`, bukan witnessing. Law #131 derivative.

---

## Part 2 — reality_origin & Attribution

Setiap consequence claim MESTI declare asal-usul. Tanpa declaration,
attribution gagal → confidence cap di 0.5.

### reality_origin enum (strict)

```yaml
reality_origin:
  - human_action       # Arif / Syed / bonded human explicitly did it
  - agent_action       # Agent/CLI did it within its envelope
  - mixed              # Human + agent co-production (declared)
  - external_environment  # Market, vendor, weather, policy — outside system
  - unknown            # Cannot determine → MUST trigger attribution_audit
```

### attribution_confidence (float 0.0-1.0)

Kira `attribution_confidence` dari 4 input:

```python
confidence = (
    0.30 * direct_evidence_weight      # receipts, hashes, external logs
  + 0.25 * chain_completeness          # sealed cause→effect chain
  + 0.25 * witness_independence        # not producer's own observation
  + 0.20 * temporal_proximity          # cause preceded effect, < TTL
)
```

| Confidence band | Verdict | Action |
|------:|---------|--------|
| ≥ 0.85 | ATTRIBUTED | accept, log, continue |
| 0.60–0.84 | WEAK_ATTRIBUTION | log + flag, watch next cycle |
| 0.40–0.59 | CONTESTED | HOLD, escalate ke musyawarah |
| < 0.40 | UNATTRIBUTED | REQUIRED attribution_audit, no credit, do not propagate |

### attribution_evidence (array, minimum fields)

```yaml
attribution_evidence:
  - source: "<exact path / url / file:line>"
    kind: receipt|hash|external_log|witness_statement|carried_forward
    timestamp: "<ISO8601>"
    independence: self|other_organ|external_third_party|human
    quote_or_hash: "<truncated, link for full>"
```

### Anti-credit-theft rule (P0, F13-class)

> Agent MUST NOT claim credit untuk perubahan yang sebenarnya datang
> daripada `external_environment` (market, weather, vendor policy).
> Such claim boleh naik confidence surface tapi score reality_origin=
> `external_environment` tetap di emission. Audit will catch fabricated
> agency.

---

## Part 3 — Reality Score Formula (Reality Score vs Reality Debt)

> Reality Score = `Σ (R_class_weight × confidence × independence_factor)`
> Reality Debt  = `Attention Consumed - Reality Produced`
>
> Reality Debt is parent formula — see `reality-debt-audit-v1.0`.

### R_class_weight (default, F13 can override)

```
R1 = 0.05    # file changes — almost never credit-worthy
R2 = 0.15    # system changes — operational survivability
R3 = 0.35    # capability changes — federation grows
R4 = 0.65    # human behavior — bond preserved, decision made
R5 = 1.00    # world consequence — full weight
```

### independence_factor (witness quality)

| Source | factor |
|--------|-------:|
| Producer's own log (echo) | 0.0 |
| Same-organ witness | 0.3 |
| Other-organ same-federation | 0.7 |
| External third party | 1.0 |
| Human (Arif/bonded) | 1.0 |

### Reality Score example

```yaml
claim: "Quota sentinel saved RM 47.20 in Alibaba PAYG"
R_class: R5              # world consequence (money)
reality_origin: agent_action
attribution_confidence: 0.91   # direct receipt + ledger + external quota notice
witness_class: other_organ_same_federation   # mailread broker → sentinel

reality_score:
  raw: 1.00 * 0.91 * 1.0 = 0.91
  normalised: 0.91 / 1.00 = 0.91
  band: ATTRIBUTED
```

### THEATRICAL signature (the maturity test)

> Verdict THEATRICAL emitted IF AND ONLY IF:
>
> 1. Claim R-class ∈ {R1, R2} only, **OR**
> 2. Σ(witness_count) > 5 BUT all `independence_factor < 0.7`, **OR**
> 3. `attribution_confidence < 0.40` across all declared evidence, **OR**
> 4. Reality Score monotonically rises for 7 consecutive days while
>    Reality Debt also rises (the contradiction signal — see
>    reality-debt-audit).
>
> A schema that emits THEATRICAL against its own producer's work is
> constitutionally mature. A schema that never emits THEATRICAL is
> itself THEATRICAL.

---

## Part 4 — YAML Shape (canonical)

```yaml
impact_event:
  impact_id: IMP-2026-09-25-001
  emitted_at: 2026-09-25T23:59:00+08:00
  emitted_by: agent/agent_id
  scope: cron.name OR capability.id
  capability_exercised: <capability_id>

  consequence:
    R_class: R5                # R1|R2|R3|R4|R5
    class_evidence:            # minimum per Part 1 table
      source: <path/url/sha>
      independence: <enum>
      timestamp: <ISO8601>
    description: "<one sentence human readable>"

  reality_origin: human_action|agent_action|mixed|external_environment|unknown
  attribution_confidence: 0.0-1.0
  attribution_evidence:
    - source: <...>
      kind: <...>
      independence: <...>
      quote_or_hash: <...>

  witness_class: self|same_organ|other_organ_federation|external_third_party|human
  reality_score: 0.0-1.0
  verdict: ATTRIBUTED|WEAK_ATTRIBUTION|CONTESTED|UNATTRIBUTED|THEATRICAL

  # thetaslot anti-circular
  produced_new_impact: true|false   # does this event open a new consequence chain?
  consumes_attention_estimate_minutes: 0
```

---

## Part 5 — Governance — Lock & Maturity Test

### Anti-self-credit clauses (binding)

1. Schema MAY NOT credit its own emission. Producer's emission is not
   witness for its own claim.
2. Schema MUST declare `reality_origin` honestly. `agent_action` is not
   allowed to be silent.
3. `external_environment` is not credit-eligible. If a market moved, that
   is `external_environment`, not `agent_action`.

### Law #131 alignment (sealed 2026-09-21)

> "A wise machine does not maximize action. It minimizes unnecessary
> change while achieving legitimate intent."
>
> Schema MUST count: did the change serve legitimate intent? If no,
> emit THEATRICAL regardless of R-class.

### Maturity tests (binary, must all PASS before promotion F13_RATIFIED)

- [ ] 100 consecutive emissions, ≤ 5% false-positive ATTRIBUTED
      (verified by manual spot-audit)
- [ ] First THEATRICAL verdict emitted against producer organ within
      30 days of activation (constitutional maturity = self-criticism
      capability)
- [ ] Reality Score and Reality Debt monotonically de-correlated
      (when Debt ↑, Score must NOT ↑ without R4/R5 rise)
- [ ] Attribution confidence distribution within expected band
      (median 0.65-0.85; < 0.40 < 15%)

---

## Provenance & Open Debt

- **Origin:** F13 directive 2026-09-25 in Sovereignty Cron synthesis
- **Inputs consumed:** `claim-lifecycle-states` (F13_RATIFIED 2026-09-25) ·
  `representation-reality-invariant` (DRAFT_AWAITING_F13 2026-09-18) ·
  `carry_forward.open_questions` (F13_RATIFIED 2026-09-25)
- **Open debt:** execution code (NOT written — schema-first per F13
  directive); 30-day shadow run; first THEATRICAL emission event;
  confidence calibration against live carry_forward data.
- **Promotion path:** DRAFT_AWAITING_F13 → F13_RATIFIED_CHAT →
  review at `/root/AAA/canon/` (currently `chattr +i`; promotion
  requires F13 override).

rasa: |
  "Activity tanpa consequence adalah bunyi. Schema ini paksa sistem
  mengaku apa yang ia benar-benar ubah — bukan apa yang ia rasa dia ubah.
  Dan bersedia verdikalkan THEATRICAL terhadap kerja sendiri."