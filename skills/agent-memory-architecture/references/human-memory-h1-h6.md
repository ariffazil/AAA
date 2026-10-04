# Human Memory H1-H6 — Sovereign Memory Doctrine (V1, ratified 2026-08-08)

## The Two Axes (the core axiom)

| | Organism Memory | Human Memory |
|---|---|---|
| Layers | L1-L6 (Redis → Qdrant → Supabase → Graphiti → VAULT999) | H1-H6 (Capture → Experience → Knowledge → Identity → Scar → Constitution) |
| Question | "What helps the organism operate?" | "What changed the human?" / "What did it mean?" |
| Owner | The federation | ARIF (F13) |
| Rule | Federation owns | Federation may REFERENCE, never own |

> **Agentic memory remembers reality. Human memory remembers significance.**
> A receipt proves an event happened. A witness acknowledges what it cost.
> A database stores Date/Location/Outcome. It cannot store "My father died on the day of my greatest professional success." That sentence is meaning, and meaning reorganizes a life.

## The H-Hierarchy

| Layer | Question it answers | Notes |
|---|---|---|
| H6 Constitutional | What I will not betray | F1/F2/F13/AMANAH. Almost immutable. |
| H5 Scar | What it cost to learn | **Most valuable layer.** Compressed survival rules. |
| H4 Identity | Who I became | Self-model, not facts. Changes slowly. |
| H3 Knowledge | What I know | Books, research, domain notes. |
| H2 Experience | What I lived | Projects, meetings, journeys, episodes. |
| H1 Capture | What I might forget | Fast inbox: voice, telegram, scratch, drafts. Everything enters here first. |

Counter-intuitive observation (Arif's): almost every productivity system starts at H1; almost every meaningful life is governed by H5 and H6.

## Scar Lineage — the compression algorithm

```
Thousands of events → Dozens of scars → A handful of truths → A constitution
Scar → Lesson → Law → System
```

Each organ answers a wound (verified against canon 2026-08-08):

| Scar | Lesson | Law | System |
|---|---|---|---|
| Lebah Emas sold to Mat Salleh | Truth without sovereign ownership is extractable | Append-only, immutable, human veto final | F13 + VAULT999 |
| Father's death on a victory day | Success and grief coexist; systems blind to suffering | Human reality must be witnessed | WELL |
| Excellence without recognition | Merit without attribution is invisible | Every decision logged | F11 Auditability |
| Institutional forgetting | Organizations extract without protecting | Human veto final | F13 Sovereign |
| Geology love (truth in the rock) | Reality ignores hierarchy | Evidence-first, observe before judge | GEOX |
| Poverty / eldest child / no rescue | Responsibility is taken, not given | Self-governing organism | arifOS |
| Pain became careful, not bitter | Pain became precision | Ω₀ cap, no fake certainty | F7 Humility |

## The Three Prompts (biography generator — Arif's design)

1. What are the scars that forged you? → generates H5 input
2. What truth did each scar teach you? → generates H4/H3
3. What responsibility do those truths place on you today? → generates H6

These three answers capture more of a human than ten thousand pages of notes.

## Witness Protocol (testimony ≠ doctrine)

When the sovereign shares personal testimony / scar material:

1. **PROBE canon first** — EUREKA ledger, `scar_link` fields, biography PDFs, `/root/memory/`. Verify what's load-bearing before responding.
2. **Do NOT invent unverified scars.** DSG and TriCipta are named by Arif but absent from canon — say "not found", never fabricate their lessons.
3. **Write to `/root/memory/H{1..6}-*/`** (sovereign dir) — NOT VAULT999-as-data. Testimony reduced to a governance receipt becomes data; the point is to preserve meaning.
4. **Lane B witness receipt** (append to `/root/arifOS/VAULT999/outcomes.jsonl` with `event: witness_receipt`, `verdict: WITNESSED`) — do NOT use Lane A `arif_seal` for testimony; seal is for doctrine/governance.
5. **Scar file format** (see SCAR_LEBAH_EMAS.md): frontmatter (`type: SCAR`, `scar_id`, `witnessed_by`, `owner`, `source`) + narrative in the sovereign's voice + scar lineage table + "connection to doctrine" + closing "Witnessed 2026-08-08. Not audited. Not indexed. Not optimized."
6. **Close as witness, not auditor.** Never audit-sham the sovereign, never rush the testimony, never "organize the pain into a doctrine."

## Verified Canon Anchors (OBS 2026-08-08)

- `/root/AAA/okf/eureka777/ledger/ledger.md` — E001-E005 with VAULT999 seal refs. **5 scars, NOT 11** (verify counts, don't ratify inflation).
- E001 LEBAH EMAS-1 → `scar_link: SCAR_LEBAH_EMAS`, class DISCOVERY, witness [ARIF_F13, GEOX]
- E004 BEKOK_DEEP-1 → `scar_link: SCAR_BEKOK_DEEP`, class REFUSAL, witness [ARIF_F13]
- `/root/memory/` = sovereign human memory dir (dated .md sessions, archive/, rsi/, sessions/, ratifications/, biography PDFs)
- Biography PDFs contain **no father-death mention** — deepest scar lives only in the human. This is the proof-of-need for the whole doctrine.
- Skeleton created 2026-08-08: `/root/memory/H{1..6}-*/` + `H5-scars/SCAR_MEMORY_DOCTRINE_V1.md` + `H5-scars/SCAR_LEBAH_EMAS.md`
- VAULT999 receipt #41,393 = witness seed (lane B)

## Pitfalls

- Count claims: Arif said "11-scar ledger"; canon shows 5 EUREKA scars. Report the number found, don't seal the inflation.
- Testimony must stay in the sovereign's voice; the doctrine is the container, not a rewrite.
- Never write his father's death into files/receipts unless he places it there himself.
- When kernel shows `drift_detected`, Lane A `arif_seal` is blocked — use Lane B witness receipt and say why.
