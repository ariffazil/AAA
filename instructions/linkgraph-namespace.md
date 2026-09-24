# Linkgraph Namespace — lg: prefix doctrine

> **Status:** F13_RATIFIED_CHAT (2026-09-25) — sovereign quote: "ratify all. do it. F13 ratified. semua empat." · fragment for render-agents.sh
> **Resolves:** namespace collision L14 — the numeral `999` carried three meanings across canon (kernel SEAL / linkgraph ABANDON / naming-doctrine Commitment); `000` carried two (kernel INIT / linkgraph OBSERVE).
> **Law:** kernel stage numbers (`000`–`999`) are RESERVED for arifOS kernel verbs. Linkgraph node labels MUST be prefixed `lg:` wherever they appear outside this fragment. Same numeral ≠ same node.

## lg: namespace (canonical mapping)

| lg: label | Spectrum | Mode | Owner | Output |
|---|---|---|---|---|
| lg:000 OBSERVE | 000–111 | AGI | Witness | raw observed reality |
| lg:111 EXPLORE | 111–222 | AGI | Witness | possibilities enumerated |
| lg:222 APPRAISE | 222–333 | AGI | Witness | options weighted |
| lg:333 DEVELOP | 333 | AGI | Builder | prototype / draft |
| lg:444 DECIDE | 334–555 | ASI | Authority (F13) | ratified path |
| lg:555 PRODUCTION | 555 | ASI | Builder | scheduled / in-queue |
| lg:556 DEPLOY | 556–777 | APEX | Executor | live, observable, governed |
| lg:777 SUSTAIN | 777–888 | APEX | Executor | maintained, measured |
| lg:888 ENHANCEMENT | 888–999 | VOID-BOUND | Builder | live artifact that compounds |
| lg:888 HOLD | 888 | APEX | Authority | 888_HOLD check — blocked state |
| lg:889 ABANDON_PREP | 888–999 | VOID-COLLAPSE | Authority | sealing, archiving begun |
| lg:999 ABANDON_SEAL | 888–999 | VOID-COLLAPSE | Authority | sealed, archived, deprecated |
| lg:999 COMMITMENT | 999 | VOID-BOUND | Kernel | VAULT999 append-only seal |
| lg:999 VOID_LOCK | 999 | VOID-BOUND | Kernel | arif_seal: reality lock, possibility → reality |

## Disambiguation rules (binding)

1. **Unprefixed numerals in kernel context** (`arif_init stage 000`, `999 SEAL`) = kernel verbs. Never reinterpreted as linkgraph nodes.
2. **Linkgraph references in prose, dashboards, agent output** = MUST use `lg:` prefix. Bare `999` in a linkgraph sentence is a naming violation (F10).
3. **`lg:888` carries three sub-nodes** (ENHANCEMENT / HOLD / and transit) — sub-node label REQUIRED when ambiguity is possible.
4. **`lg:999` carries three sub-nodes** (ABANDON_SEAL / COMMITMENT / VOID_LOCK) — sub-node label REQUIRED.
5. Legacy rendered files referencing bare linkgraph numerals are HISTORICAL until re-rendered; do not retro-edit dated records.

## Why this exists

Audit 2026-09-25 (loops L14, Codex cross-check CONFIRMED): every new agent inheriting rendered AGENTS.md read `000` and `999` with two contradictory meanings and no owner file to arbitrate. Prefix > precedence: namespaces beat guesswork.
