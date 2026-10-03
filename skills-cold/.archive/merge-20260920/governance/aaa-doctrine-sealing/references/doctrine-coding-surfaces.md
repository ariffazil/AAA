# Doctrine Coding Surfaces — Worked Recipe

Companion to `aaa-doctrine-sealing` (carried **live** from the retired `canon-doctrine-sealing`, now mode
M3 / M5 / M8 of that skill). Use when the finding is settled and the job is to land it across the
federation surfaces.

## 1. Fragment skeleton

Path: `<aaa>/instructions/<slug>.md` (the slug becomes the footer entry and the `ref:` name).

```markdown
# <Title> — <one-line law>

> **Forged:** <date> (<lane/session>) — <what produced it>.
> **Supersedes / extends:** <path or fragment name>.
> **Status:** F13_RATIFIED_CHAT (<date>) — sovereign-directed: "<his words>"   <-- REQUIRED by the commit gate
> **Binding:** all warga on <the surface this applies to>.
> **Kernel anchor:** <F-numbers this operationalises.>

## One Rule

> <the compressed law, one or two sentences.>

## The Model        <-- the formal shape, if there is one

## N Laws           <-- numbered, imperative, each with its WHY

## The Gate (operational)   <-- pass/block examples the agent can pattern-match

## What Is Lawful   <-- the allowed moves

## Profile Application  <-- kernel / state / agents — which surface each part lands on

## Correction Log (do not re-import these errors)   <-- see SKILL.md

DITEMPA BUKAN DIBERI
```

A gate section with a PASS and a BLOCK example is what makes a doctrine runnable; a rules list without one gets cited and ignored.

## 2. Membrane floor append

In the membrane's floors block:

```
C15 <NAME>: <the rule in one sentence, including the required label or verdict.>
C16 <NAME>: <ditto.>
```

Bump the heading's range (`C1-C14` → `C1-C16`) in the same edit — a stale range is the tell that the append was cosmetic.

## 3. Always-on line

One paragraph into `<aaa>/instructions/base.md`, near the other operative rules. It must stand alone: the model may see this line and never load the fragment.

```
**<Name> Law (<date>):** <formula in one clause> — <what it forbids in one clause>; <what it requires instead>. Full doctrine: `<aaa>/instructions/<slug>.md`
```

## 4. Eureka artifact + ledger row

Markdown artifact: title, session title, evidence list, the numbered eurekas (E1..En), a SEAL line, and a `CORRECTIONS CARRIED` section.

JSONL row appended to `<aaa>/eurekas/eureka-entries.jsonl`:

```json
{"ts": "<ISO-8601 UTC>", "agent": "<who>", "session": "<session id>", "eureka": "<compressed law + what changed in canon>", "evidence": ["<artifact paths>"], "truth_class": "DER", "actor": "<human+agent>", "verdict": "<e.g. DOCTRINE_LAYER_SEALED_KERNEL_WIRING_PENDING>"}
```

Append, never rewrite the file — other sessions write to it.

## 5. Verification sweep

```bash
grep -c '<new C-numbers>' <membrane file>            # floors landed
grep -n '<slug>' /root/AGENTS.md                     # footer entry (auto) present
/root/scripts/render-agents.sh                       # re-render, then confirm no drift
git -C <aaa> log --oneline -1 && git -C <arifos> log --oneline -1
git -C <aaa> status -sb | head -2                    # pushed, no ahead-count
```

## 6. Report shape

Four beats, no more: **what changed on which surface** → **commit hashes per repo** → **what is proposed vs live** (the amendment is not wired until a floor exists) → **the one-line compression**. The open debt belongs in the report, not in a footnote — a sealing report that hides the unwired part is a false receipt.
