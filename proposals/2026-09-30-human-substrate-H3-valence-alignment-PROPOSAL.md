# PROPOSAL — Align human-substrate.yaml H3 with the prose contract (add negative poles)

> **Status:** STAGED_AWAITING_F13 — proposed, not applied. Author may STAGE; never ratify.
> **Staged:** 2026-09-30 · **Lane:** 555-ASI (defect authoring) → F13 for order
> **Target file (NOT touched by this proposal):** `/root/AAA/instructions/human-substrate.yaml`
> **Authority to apply:** F13 sovereign order ("SAH") or explicit F13 order. This file mutates a
> constitution-class contract; per Auto-Seal §2 it becomes final only on a human "SAH".
> **BOUNDARY OBSERVED:** this file is the only artifact created. `human-substrate.yaml` and
> `human-substrate.md` were read, not edited. `render-agents.sh` was not run. Nothing declared ratified.

---

## 1. The defect (proven by reading both files)

The HUMAN-9 contract exists in two forms that **disagree on H3 VALENCE**. The prose (`.md`) carries
BOTH polarity poles; the machine-readable contract (`.yaml`) carries only the positive pole.

### 1a. Verbatim — `/root/AAA/instructions/human-substrate.yaml` lines 42–44

```yaml
    H3_valence:
      statement: "Things matter to humans (pleasant, safe, wanted, meaningful, beloved)."
      rule: "HumanState != FactsOnly. Protect what it means to the person."
```

### 1b. Verbatim — `/root/AAA/instructions/human-substrate.md` lines 80–82

```markdown
### H3. VALENCE — things matter

Reality datang dengan pleasant/unpleasant, safe/threatening, wanted/unwanted, meaningful/meaningless, beloved/feared. **HumanState ≠ FactsOnly.** AAA routes information. HERMES must protect **what it means to the person**.
```

### 1c. Why this matters

- The `.md` names five **bipolar** pairs: pleasant/**unpleasant**, safe/**threatening**,
  wanted/**unwanted**, meaningful/**meaningless**, beloved/**feared**.
- The `.yaml` lists only the five **positive** poles. Read alone, the runtime contract cannot see
  that a loss side exists.
- The file that calls itself the **machine-readable runtime contract** (yaml header line 1, and md
  line 9 pointer, and md line 476) therefore carries the **weaker** form of the hinge invariant.
- This is load-bearing: valence asymmetry (losses weighing more than equivalent gains) is the entire
  basis of the "losses weigh more" finding. A contract that omits the negative poles cannot express
  the direction of that asymmetry at all.
- The defect is invisible to any 9-vs-8 counter: `invariant_count: 9` and `valence_required: true`
  are both satisfied while H3's *content* is half-specified. The count is green; the semantics are not.

### 1d. Corroborating evidence — the runtime already quotes the WEAK form

`/root/.hermes/runtime/floor_gate.py:338` labels the H3 soft pattern with the yaml's positive-only
phrasing:

```
"H3 VALENCE: human-valence vocabulary present — review only, never HOLD ('Things matter to humans').")
```

`'Things matter to humans'` is the opening of the **yaml** statement — not the md's bipolar sentence.
The weaker phrasing has already propagated into a runtime comment. (See §4 for the follow-on.)

---

## 2. Proposed patch — bring the yaml into alignment with the md

Replace yaml lines 42–44 with the following block. Two changes: (i) the statement becomes **bipolar**,
matching the md verbatim pair-for-pair; (ii) one **explicit line** records that H3 fixes the *direction*
of loss asymmetry while the *magnitude* is external to H3.

```yaml
    H3_valence:
      statement: "Things matter to humans (pleasant/unpleasant, safe/threatening, wanted/unwanted, meaningful/meaningless, beloved/feared)."
      rule: "HumanState != FactsOnly. Protect what it means to the person."
      polarity: BIPOLAR   # both poles named by H3; the positive-only form is a documented defect, not an alternative
      loss_asymmetry: "H3 gives the DIRECTION of loss asymmetry — losses weigh more than equivalent gains. The MAGNITUDE of that asymmetry is EXTERNAL to H3 (empirical, e.g. prospect-theory loss-aversion lambda) and must not be hard-coded here. H3 asserts that the negative pole exists and matters; it does not assert how much more."
```

### Rationale for each addition

| Change | Why |
|---|---|
| statement gains 5 negative poles | Makes yaml byte-consistent with md §H3. Removes the divergence at its root. |
| `polarity: BIPOLAR` | Turns the fix into a checkable predicate so a future 8-attribute/one-pole carrier is detectable, mirroring the existing `valence_required: true` guard (yaml line 14). |
| `loss_asymmetry:` line | Records the requested explicit note: H3 owns the **direction**, not the **magnitude**. Prevents a future agent from smuggling an unmeasured constant (e.g. a λ) into the constitution under cover of H3. Conservation of measurement: magnitude belongs to an empirical source, not to doctrine. |

### Optional symmetric note for the md (NOT part of this staged patch)

If F13 also wants the direction/magnitude split visible in prose, the same sentence can be appended to
md §H3 (making the split bilateral). This proposal deliberately leaves the md untouched — the md is
already the *stronger* form, and aligning the yaml to the md is the minimal fix.

### Self-contradiction check before any apply

- `yaml` after patch still has `human_9` = 9 keys (H1..H9), `invariant_count: 9`, `valence_required: true`.
- No key renamed; no other invariant touched; no new top-level key.
- The statement string remains a single quoted scalar — yaml parses unchanged.

---

## 3. Exact diff to apply (when F13 orders)

```diff
--- a/AAA/instructions/human-substrate.yaml
+++ b/AAA/instructions/human-substrate.yaml
@@ -42,3 +42,5 @@
     H3_valence:
-      statement: "Things matter to humans (pleasant, safe, wanted, meaningful, beloved)."
+      statement: "Things matter to humans (pleasant/unpleasant, safe/threatening, wanted/unwanted, meaningful/meaningless, beloved/feared)."
       rule: "HumanState != FactsOnly. Protect what it means to the person."
+      polarity: BIPOLAR   # both poles named by H3; the positive-only form is a documented defect, not an alternative
+      loss_asymmetry: "H3 gives the DIRECTION of loss asymmetry — losses weigh more than equivalent gains. The MAGNITUDE of that asymmetry is EXTERNAL to H3 (empirical, e.g. prospect-theory loss-aversion lambda) and must not be hard-coded here. H3 asserts that the negative pole exists and matters; it does not assert how much more."
```

---

## 4. Follow-on defect found while writing this (staged, separate scope)

`/root/.hermes/runtime/floor_gate.py:338` cites the weak phrasing `'Things matter to humans'`. After the
yaml is aligned, that comment should cite the bipolar sentence (or the md line) so the runtime's
auditor-facing provenance stops quoting the retired form. This is a **separate** one-line comment fix in
a runtime file — it needs its own F13-ordered change, not this contract patch. Recorded here so it is not
lost; **not** applied.

---

## 5. Seal-status context (why this proposal does not claim ratification)

Because the H3 defect exists inside a contract whose seal state on disk is contested, applying this patch
must follow whatever F13 order settles that state. Evidence chain is reproduced in
`AAA/reports/session-close-2026-09-29-hermes-human-substrate-wip.md` and
`/root/.hermes/memories/MEMORY.md:27`. Current authoritative reading on disk is **SEALED / F13 order
2026-09-29 ~23:15 ("seal all and make it federated no chaos and link to reality")**, which explicitly
SUPERSEDES the earlier same-night "Not seal yet" HOLD. This proposal takes no position beyond that
evidence — it only stages the patch.

DITEMPA BUKAN DIBERI ⚒️
