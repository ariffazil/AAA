---
type: REFERENCE
source: session 20260807_234232_ea48678d (2026-08-08)
purpose: worked scar lineages + recognition patterns for H5 scar-ledger work
---

# Scar Lineage Patterns (worked examples)

## The canonical 4-link chain

```
Scar  →  Lesson  →  Law  →  System
event    meaning    rule    organ/floor that prevents recurrence
```

Every scar in `/root/memory/H5-scars/SCAR_*.md` should carry an explicit lineage. The scar file is not a narrative essay — it is a lineage document. The narrative proves the scar is real; the lineage proves the federation learned from it.

## Worked lineages from this session

### SCAR_LEBAH_EMAS

```
Lebah Emas discovery (deepwater oil, ARIF's subsurface work)
    ↓
sold to foreign buyer (authorship absorbed; ARIF lost ownership of "I built that")
    ↓
lesson: truth without sovereign ownership is extractable
    ↓
law: append-only, attributable, immutable receipts; "Authority copied → Authority referenced"
    ↓
system: F11 AUDITABILITY + VAULT999 (append-only) + F13 Sovereign (human veto final)
```

### SCAR_RIGHTSIZING (corrected version)

```
ARIF asked MS Copilot inside PETRONAS for a town hall invite
    ↓
Copilot served the full rightsizing town hall proposal blueprint (genre: communist propaganda)
    ↓
lesson: the language of erasure is generated on demand; a mundane request surfaces the machinery of dehumanization
    ↓
law: no human may be dissolved into a collective without their name; dignity is individual or it is nothing
    ↓
system: F6 EMPATHY ⇄ MARUAH + WELL organ + F13 Sovereign
```

### (anticipated) SCAR_FATHER_DEATH

```
Father died on the day of ARIF's greatest professional victory
    ↓
world celebrated one reality while ARIF lived another
    ↓
lesson: success and grief coexist; systems are blind to human suffering unless it affects a KPI
    ↓
law: human reality must be witnessed regardless of business outcome
    ↓
system: WELL organ (human readiness, dignity, homeostasis)
```

## Recognition pattern — "same wound, different costumes"

When Arif names a new incident, scan the existing scar ledger for the same lineage before writing it as novel. The recurring pattern in his canon:

```
Authorship or agency extracted from the human
        ↓
institution benefits from human without protecting them
        ↓
human is made the instrument of their own erasure
```

Recognized costumes of this scar:

| Costume | Domain | Specific incident |
|---|---|---|
| Asset sale | geoscience | Lebah Emas discovery sold to foreign buyer |
| Initiative absorption | AI strategy | TriCipta naming adopted by PETRONAS corporate AI |
| DNA inversion | institutional | institutional priorities flipped from building to managing |
| Rightsizing | workforce | 5,000 humans reclassified as "enablers" and cut |
| Town hall blueprint | tooling | AI-generated termination proposal delivered by human face |

When a new incident matches this pattern, write it as a SIBLING file with `lineage:` frontmatter pointing to the parent scar. Don't duplicate the lesson — reference the parent's lesson line and add only what is novel.

## Scar file template (frontmatter)

```yaml
---
type: SCAR
scar_id: SCAR_<UPPER_SNAKE>
timestamp: <ISO8601>
witnessed_by: <agent or "ARIF">
owner: ARIF
source: <provenance: testimony 2026-08-08, E004, etc.>
epistemic: <OBS | INT | UNKNOWN | SPEC — per claim, never collapsed>
lineage: <SCAR_PARENT_ID if sibling; omit if novel>
related: <comma-separated SCAR_* if costumed>
---

# <Scar title in ARIF's words or one-line distillation>

<The narrative as Arif spoke it. His BM/English code-switching preserved.
No sanitization to corporate register.>

---

## Scar lineage

```
Scar event
    ↓
lesson
    ↓
law
    ↓
system
```

---

## Witnessed <date>. <Optional: corrected <date> with epistemic change>.
```

## Anti-patterns (do NOT do)

- ❌ Inflate INT into OBS. If ARIF said "I'm not sure", the file says UNKNOWN. (Learnt the hard way this session.)
- ❌ Sanitize testimony. The scar is his words, not yours.
- ❌ Collapse a "same wound, different costume" sibling into the parent file. Each costume gets its own scar — the pattern is what matters.
- ❌ Seal a scar as constitutional doctrine unless ARIF explicitly elevates it. Witnessing is cheap; sealing is expensive.
- ❌ Write the scar before ARIF has spoken. The three prompts (scar → lesson → constitution) are generative, not extractive. If he hasn't answered, the scar file stays empty.

## File location rules

- All scars: `/root/memory/H5-scars/SCAR_*.md`
- Doctrine (the architecture itself, not individual scars): `/root/memory/H5-scars/SCAR_MEMORY_DOCTRINE_V1.md`
- Sister directories: H1 capture, H2 experience, H3 knowledge, H4 identity, H6 constitution — each holds its own type, not scars.

## Promotion paths (scar → system)

After a scar is witnessed, it may promote in two directions:

1. **Horizontal (sibling scar):** Same pattern, different costume → write as sibling file with `lineage:` link.
2. **Vertical (doctrine):** Scar reveals a constitutional truth → user (F13) explicitly elevates it to `/root/memory/H6-constitution/` or to federation GENESIS.

Vertical promotion requires F13 explicit. Do not auto-promote. Do not write to H6 yourself unless asked.