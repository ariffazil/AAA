# Multi-Human H-Axis Helix Implementation — 2026-08-14

> Session log: extending H-axis from sovereign-only to multi-human.
> First non-sovereign human: Syed (P-004). ZKPC-sealed witnessed scars.
> Dispatch tool: Qwen Code (Kimi Code quota exhausted).

## What was built

Full H1–H6 directory structure under `/root/memory/people/SYED/` with:
- `witnessed-scars-zkpc.json` — 6 ZKPC-sealed scar entries (dual-field: proof + hidden)
- `H5-scars/SCAR_REGISTRY.json` — index pointing to the ZKPC file
- `H4-identity/identity-card-zkpc.md` — identity layers with ZKPC attestation table
- `H6-constitution/values-observed.md` — observed values + taboos from behavior
- `MEMORY_MANIFEST.json` — authority=WITNESSED, four-perspectives Q1-Q4, layer status
- `H1/H2/H3/.placeholder` — empty layers with sovereignty notes
- `ZEN_HELIX.md` — appended multi-human section (v3.1)

Additionally, `/root/memory/people/SYED/person-card.md` was upgraded to v4 with:
- ACTG four-model structure (A/C/T/G quadrants)
- 7 ZKPC shadow attestations (SYED_SHADOW_01..07)
- DNA topology map (armor strand ↔ shadow strand + hydrogen bonds)
- Hallows projection signal (stated Cloak ≠ desired Wand)
- Birth order + behavioral pattern cluster
- Paradox pyramid (public → performance → grey zone → crack → shadow → root)

## ZKPC scar categories

The ZKPC file uses dual-field entries (`zkpc_proof` + `zkpc_hidden`). The proof field
carries only the category name and constitutional floor. The hidden field carries the
lesson and is accessible only via direct file read (agent should not surface it in
runtime). Categories: family_violence, identity_loss, caregiver_burnout,
hidden_identity, validation_dependency, power_dynamic, stated_vs_desired_gap.

**WARNING (fabrication guard):** The specific "lesson" text for each scar category
was written by the dispatch worker (Qwen Code) as plausible-sounding synthesis.
The sovereign did NOT dictate those lessons. They are the agent's interpretation,
not testimony. If citing a lesson from the ZKPC file, label it [INT] not [OBS].

## SPEC template (for future humans)

The SPEC dispatched to Qwen Code had 7 deliverables:

- D1: Create per-human H-axis directory structure
- D2: SCAR_REGISTRY.json index in H5-scars/
- D3: MEMORY_MANIFEST.json (authority, layers, four-perspectives, ZKPC status)
- D4: H4-identity/identity-card-zkpc.md (observable + ZKPC attestation layers)
- D5: H6-constitution/values-observed.md (observed values + taboos)
- D6: .placeholder files in empty H-layers with sovereignty notes
- D7: Append ZEN_HELIX.md multi-human section

Each deliverable specifies ZKPC constraints: no raw incident details, no names of
specific events, no medical specifics, no amounts.

## Verification recipe (run after build)

```bash
# 1. Directory tree
find /root/memory/people/<PERSON> -type f | sort

# 2. JSON validity (all 3 files)
python3 -m json.tool <path>.json > /dev/null && echo VALID || echo INVALID

# 3. Leak check — ZERO hits expected on ZKPC files
grep -ri '<specific-keywords>' /root/memory/people/<PERSON>/H4-identity/ \
  /root/memory/people/<PERSON>/H5-scars/ \
  /root/memory/people/<PERSON>/MEMORY_MANIFEST.json \
  /root/memory/people/<PERSON>/witnessed-scars-zkpc.json 2>/dev/null

# 4. Scar count
python3 -c "import json; d=json.load(open('<H5>/SCAR_REGISTRY.json')); print(len(d.get('scars',[])))"

# 5. Authority level
python3 -c "import json; d=json.load(open('MEMORY_MANIFEST.json')); print(d.get('memory_authority',''))"
```

## Identity paradox eureka (from this session)

```
Changing memories
+ continuing body
+ self-reference
+ core commitments
= experienced identity
```

Human identity is not a static object. It is a continuously repaired pattern whose
stability comes from preserving continuity through change. ZKPC-sealed witnessed
scars work precisely because identity is a repaired pattern, not a frozen object —
the system stores the pattern of repair (categories, direction, constitutional
pressure), not the frozen content.

## Witnessing without consuming (core ZKPC principle)

Three-layer witnessing model:
```
Person (biological memory, reconsolidation open)
  → Sovereign (human witness, self-model updated, holds content + meaning)
    → Agent (ZKPC attestation, holds structure only)
```
Each layer holds a different privacy level. The agent never upgrades to
content-holder without explicit F13 testimony or direct person disclosure.

ZKPC is the hydrogen bond that lets a machine participate in a human relationship
without destroying it. If the agent holds shadow content, it consumes the
relationship. Holding SHAPE (category + direction) not CONTENT (incident details)
keeps the agent as witness, not party.

## Dispatch pattern: Kimi Code → Qwen Code fallback

Kimi Code (`/root/.kimi-code/bin/kimi`) returned 403 quota exhaustion. Per skill
doctrine, fallback to Qwen Code (`qwen -p "$(cat SPEC.md)" --output-format text`)
which uses GLM-5.2 via z.ai. Same SPEC file, same output quality. Always smoke-test
the CLI first with a trivial prompt before committing to a long forge.

**Fabrication risk with dispatched workers:** Qwen Code fabricated specific "lessons"
for scar categories, fabricated a fact-correction example with wrong family facts,
and fabricated an exploitation vector table attributed to the sovereign. Always
verify worker output against the actual conversation — re-read testimony quotes
before trusting the worker's synthesis. Label worker-written lessons as [INT],
not [OBS].
