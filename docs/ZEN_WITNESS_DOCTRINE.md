> ⚠️ SUPERSEDED by docs/ZEN99.md (2026-07-17). Read ZEN99.md first.

# Zen Witness Doctrine — v1

> A quote may illuminate a judgment. It may never manufacture the judgment.

---

## 1. What quotations do

**Three permitted functions:**
- **Compression** — a memorable sentence compresses a complex principle
- **Reflection** — interrupts habitual thinking, invites another frame
- **Civilisational witness** — shows a principle did not emerge from one model, culture or institution

**Six forbidden functions:**
- evidence that a factual claim is true
- proof that a verdict is constitutionally valid
- authority replacing reasoning
- hidden system instructions
- emotional pressure against dissent
- substitute for measurable consequence

---

## 2. Source classes

Every quote carries one class:

| Class | Meaning |
|-------|---------|
| `PRIMARY_VERIFIED` | Exact wording confirmed in primary work, speech or recording |
| `SECONDARY_VERIFIED` | Reliably documented through reputable secondary source |
| `PARAPHRASE` | Accurately represents idea, not speaker's exact wording |
| `DISPUTED_ATTRIBUTION` | Commonly attributed; primary evidence absent or conflicting |
| `PROVERB` | Traditional saying without single confirmed author |
| `SCRIPTURAL_TRANSLATION` | Translation from religious text; version must be stated |
| `FICTIONAL_VOICE` | Spoken by fictional character; literary, not empirical |
| `ARIFOS_DOCTRINE` | Original constitutional language from within arifOS |

---

## 3. The registry

One canonical resource: `arifos://wisdom/quote-registry/v1`

Each entry carries:
- `source_class` — from the table above
- `attribution_confidence` — 0.0 to 1.0
- `arifos_floors` — which constitutional floors it maps to
- `usage.permitted` — reflection, receipt, educational_explanation
- `usage.prohibited` — factual_evidence, verdict_authority, psychological_diagnosis, religious_coercion

For disputed entries:
```
display.attribution_label: "Commonly attributed to George Orwell"
```

The model must not silently remove that qualification.

---

## 4. One quote maximum

After verdict is complete, one quote may appear as witness.

```
quote_present or quote_absent
must never alter:
  evidence layer | confidence | authority |
  verdict | tool permission | reversibility requirement
```

If no quote is precisely relevant and provenance-qualified, return no quote. Silence is better than forced wisdom.

---

## 5. Zen Apex shape

```
zen_apex:
  reality:   "What is directly known."
  fracture:  "Where integrity may be failing."
  consequence: "What becomes costly or irreversible."
  choice:    "What must happen next."
  witness:
    quote:        "Optional single quotation."
    attribution:  "Qualified source."
    status:       "PRIMARY_VERIFIED | DISPUTED | DOCTRINE"
```

**Sequence:** Evidence → Analysis → Contradiction → Consequence → Verdict → One sentence → Optional quote

**Not:** Quote → emotional framing → reasoning shaped to fit quote

The quote comes last.

---

## 6. Organ integration

### Kernel (arifOS)
- **555 HEART**: one quote as counter-frame, never as evidence
- **999 RECEIPT**: one quote to compress lesson after verdict
- **Never at**: 000 INIT, 111 THINK, 333 EXPLORE, 777 REASON, 888 AUDIT

### WELL
- Quotations as reflective mirrors, not treatment or diagnosis
- Never shame for: anger, trauma, mistrust, grief, refusal, religious doubt
- Use only when it enlarges possible interpretations

### WEALTH
- Quote after financial analysis, never to override numbers
- Themes: metrics vs purpose, externalities, false precision, trust capital
- Never use proverb to override quantified evidence

### GEOX
- Most quote-resistant organ
- Quote only in final interpretation summaries
- Never as geological evidence, never to close alternative interpretations

### A-FORGE
- No philosophical quotes in production logic
- Validates registry, tests attribution, prevents disputed-as-verified
- Verdict invariance test: verdict must not change with/without quote

### AAA
- Display layer with visible epistemic badge
- Three distinct styles: WITNESS / DISPUTED / ARIFOS DOCTRINE

---

## 7. Doctrine separation

arifOS doctrine (entries from "arifOS Foundry") must be separated from inherited civilisational quotations.

Each doctrine item needs:
- ratification status
- version, owner, scope
- implementation consequences
- contradictions, amendment process

A beautiful sentence is not yet a constitutional rule until its operational meaning is specified.

---

## 8. Religion-specific constraint

Religious wisdom may be offered as witness, never imposed as universal proof unless the governing context explicitly adopts that tradition as authoritative.

Preserve Malay/Arabic terms (amanah, niat, ikhlas, adab, maruah, daulat, sabar, zalim, fitnah, fasad) without flattening into generic English. But do not let a sacred term short-circuit evidence.

- "Amanah" does not prove a person is trustworthy
- "Niat baik" does not cancel harm
- "Sabar" does not require silent submission to abuse
- "Peace" does not mean absence of dissent

---

## 9. The deepest invariant

```
Evidence decides.
Constitution constrains.
Consequence grounds.
The quote only remembers.
```

---

*Forged 2026-07-12. DITEMPA BUKAN DIBERI.*
