# CHRON Task Grammar — Function-Based, Not Artifact-Based

> **Status:** DESIGN REFERENCE — canonical naming doctrine for all CHRON-native agents
> **Authority:** F13 sovereign analysis, 2026-09-18
> **Derived from:** CHRON_REALITY_TASK_FINAL_DOSSIER_2026-09-18.pdf, CHRON-TEMPORAL-SUBSTRATE-ARCHITECTURE.md, chron_spine_gate.py
> **Law:** "Seal the arrows, not the artwork."

---

## 0. The Naming Doctrine

**DO NOT** name tasks by their output artifacts:

```text
❌ Generate Executive Briefing
❌ Create Morning Card
❌ Run News Feed
❌ Send Economic Digest
❌ Create GEOX Update
```

**DO** name tasks by their position in the CHRON causal spine:

```text
✅ Observe material change
✅ Prioritize what deserves attention
✅ Predict what we expect
✅ Verify predictions against outcomes
✅ Extract lessons from errors
```

**Why:** Artifact-based naming makes agents optimize for the renderer.
Function-based naming makes agents optimize for the causal arrow.

---

## 1. The Seven Functions

| Function | Causal Arrow | Question | Output | Renderer |
|----------|-------------|----------|--------|----------|
| `observe` | WORLD → OBSERVE | What materially changed? | change candidates | any |
| `prioritize` | OBSERVE → SELECT | What deserves attention now? | ranked signals | any |
| `predict` | SELECT → EXPECTATION | What do we expect next? | prediction + verify_at | any |
| `verify` | OUTCOME → COMPARE | Were we right? | expected vs observed + error | any |
| `learn` | COMPARE → MEMORY | Which error deserves to survive? | lesson candidate / scar | any |
| `reconcile` | MEMORY → ATTENTION | What deserves attention now given what we learned? | revised ranking | any |
| `reflect` | ATTENTION → CALIBRATION | What should carry into tomorrow? | forward context | any |

---

## 2. Canonical Task Shape

```yaml
chron_task:
  task_id: CHRON-XXXX

  function:
    observe |
    prioritize |
    predict |
    verify |
    learn |
    reconcile |
    reflect

  principal:
    arif | syed | federation

  question:
    "What changed?"    # natural-language, the actual question

  audience:
    private | shared | internal

  delivery_policy:
    ALWAYS | MATERIAL_ONLY | SILENT_OK

  output:
    full | pulse | silent

  renderer:
    text | png | pdf | voice | dashboard | none
```

---

## 3. Existing Tasks → Function Mapping

### Currently ALIVE

| Current Name | Function | Question | Output |
|-------------|----------|----------|--------|
| Morning Brief (pagi) | `observe` | What changed overnight? | pulse |
| Alpha-Zen Card (pagi) | `prioritize` | What matters today? | pulse |
| Evening Brief (malam) | `reconcile` | What deserves attention now? | full |
| Alpha-Zen Card (malam) | `prioritize` | What mattered today? | pulse |
| Iron Radar | `observe` | What changed in energy/metals? | pulse |
| Geo-Econ | `observe` | What changed in geopolitics + economy? | pulse |
| Malaysia Intel | `observe` | What changed in Malaysia? | pulse |
| Niat | `reflect` | What should carry into tomorrow? | full |

### Currently UNBUILT (the 3 missing arrows)

| Future Name | Function | Question | Required |
|------------|----------|----------|----------|
| Prediction Appointment | `predict` | What do we expect next? | prediction + verify_at |
| Reality Reckoning | `verify` | Were we right? | expected + observed + error |
| Scar Formation | `learn` | Which error deserves to survive? | error + lesson_candidate |

---

## 4. Renderer Independence

The same ChronPacket can be rendered as:

| Renderer | When |
|----------|------|
| `text` | Telegram message, quick pulse |
| `png` | Visual card, daily summary |
| `pdf` | Formal briefing, weekly reckoning |
| `voice` | Audio brief, hands-free |
| `dashboard` | Persistent surface, trend view |
| `none` | SILENT — an intelligent action |

**Rule:** The function determines the content. The renderer determines the shape.
Never let the renderer determine the content.

---

## 5. The Proving Query

If CHRON can answer this correctly from evidence, it has moved beyond RAG:

> "Show me everything we believed about X at time T, why we believed it, what contradicted it, what we did because of it, what happened afterward, and what changed our belief."

This query requires:
- ChronEpisode (temporal identity)
- Bitemporal storage (valid_time + transaction_time)
- Prediction → verification → calibration (measured learning)
- Supersession/retraction (belief evolution)

None of these exist at runtime yet. This is the target.

---

## 6. Compression

> CHRON is not a content system. CHRON is a reality→attention→expectation→action→outcome→memory→calibration→better_attention pipeline. All outputs are projections from a canonical ChronPacket. Name the function, not the artifact.

---

DITEMPA BUKAN DIBERI ⚒️
