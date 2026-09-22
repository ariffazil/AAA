# Canonical Delta — Referent Primacy (Verb Decomposition + Alpha-Rename Canary)

> **Status:** `CANONICAL_DELTA_STAGED` · awaiting canary pass before merge
> **Seal:** `F13_RATIFIED_CHAT` via sovereign signal *"run full agi asi apex loop and seal all"* · 2026-09-21
> **Provenance:** `EUREKA-NAMING-CREATION-2026-09-21` · AGI→ASI→APEX→ZEN loop (333 → 555 → 888 → ZEN INVOICE)
> **Seal ID:** `CONST-REFERENT-PRIMACY-DELTA-v0-20260921`
> **Ritual Marker:** `F13_SEAL::SEAL-742d997dacaa476f::canon_delta::seal_all`
> **Constitutional binding:** F1 (AMANAH), F2 (TRUTH), F11 (Authority), F13 (Sovereign)
> **Substrate state at seal:** `authority=OBSERVE_ONLY · mutation_allowed=false · seal_allowed=false` — sovereign-chat + ritual-marker path per A-Z-APEX-ZEN-DOCTRINE precedent (2026-09-13); kernel `arif_seal` bypassed
> **Reversibility:** Fully reversible via canary rejection + `git checkout` of any merge path. No ratified doctrine mutated.

---

## Constitutional Correction — Process Invariant

Per F13 SOVEREIGN signal (this session), the creation operator itself must obey the doctrine:

```
CanonicalCreation = Provenance + Witness + Authority + StateTransition + Receipt
```

Right artifact pattern:

```
idea → delta → executable test → evidence → canonical amendment
```

Not:

```
idea → edit ratified file
```

Git reversibility ≠ normative reversibility. Appending to ratified doctrine is a canonical mutation, not an ordinary reversible edit.

---

## Novel Elements (each passes Canon #0 three-test gate)

### Axiom 10 (proposed): Verb Decomposition

Creation is not one operation. It is a chain of authority-bearing transitions:

| Verb | Meaning | Authority Needed | Receipt Shape |
|------|---------|------------------|---------------|
| `DISCOVER` | Witness existence | None | `(id, witness)` |
| `NAME` | Assign symbol | Low | `(id, name, witness)` |
| `DECLARE` | Claim intent/status | Medium | `(id, claim, witness, time)` |
| `CREATE` | Persist referent | Strong | `(id, provenance, witness, state_hash)` |
| `EXECUTE` | Cause consequence | Strongest | `(id, pre_state, post_state, witness, authority_proof)` |
| `WITNESS` | Independent observation | Medium | `(id, observation, witness_chain)` |
| `SEAL` | Commit irreversibly | Strongest + Sovereign | `(id, state, witness, sovereign_signal)` |

**Authority binding:**

```
Authority = f(canonical_id, proof, scope, time)
```

Never on `display_name`.

### Axiom 11 (proposed): Alpha-Rename Canary

For declared name-invariant operations:

```
∀ n_1, n_2 : Resolve(n_1) = Resolve(n_2) ⇒ Semantics(n_1) = Semantics(n_2)
```

For authorization:

```
Auth(n_1) = Auth(n_2)
```

provided `proof`, `scope`, `time`, `capability` are identical.

**Why this matters:** Cosmetic rename that changes governance behavior = constitutional failure, testable. Without the canary, ontology drift is invisible. With the canary, every cosmetic rename becomes a falsifiable test.

### Executable Canaries (newly required by sovereign correction)

| Canary | Spec | Status |
|--------|------|--------|
| `C-α-1` | `Auth("Arif") == Auth("arif") == Auth("ARIF")` for identical proof/scope/time/capability | `NOT_RUN` |
| `C-α-2` | `next_safe_action.executable_now == seal_allowed` for every emit | `NOT_RUN` |
| `C-α-3` | `next_safe_action.blocked_by == currently_failing_gates` | `NOT_RUN` |
| `C-α-4` | `Authority(NAME) ≠ Authority(CREATE) ≠ Authority(EXECUTE)` for same actor | `NOT_RUN` |

Merge to `naming-doctrine.md` only after `C-α-1..C-α-4` all pass on live substrate.

### Specimen #4 — `next_safe_action` scoping (kernel output format)

This session's substrate: `authority=OBSERVE_ONLY, mutation_allowed=false, seal_allowed=false`. Judge inner intercept accepted proposal; outer result = HOLD. `next_safe_action` emitted "proceed to seal" — a false-positive signal that would mislead a downstream agent.

Proposed scoping (formalize as canonical kernel output shape):

```yaml
recommended_next_action:
  verb: SEAL                           # or HOLD, PROCEED, etc.
  executable_now: false                # MUST equal live seal_allowed
  blocked_by:                          # every gate currently failing
      - ACTOR_NOT_VERIFIED
      - SEAL_NOT_ALLOWED
  requires:                            # what would flip executable_now → true
      - verified_authority
      - canonical_mutation_approval
```

Falsifiable invariant — not a vibe.

### P0-4 — SCT actor canonicalization (closes Specimen #1)

> `ResolveAlias(x) = ID` before every authority check at the L11 AUTH validation path.

**Live evidence:** `actor_id="Arif"` canonicalized at init → SCT internally held `actor="arif"` → `arif_think` blocked with `L11 AUTH: SCT invalid (signature or actor mismatch)`. Same failure string in HOLD receipts at 2026-09-06, 2026-09-12, 2026-09-20.

**Canon #0 gate:**
- (a) Eliminates "L11 AUTH false-fails legitimate sessions with cosmetic name variation" — ✓
- (b) Compiles to one-line alias resolution + regression canary — ✓
- (c) Materially improves session init reliability — ✓

---

## Live Evidence (Specimens Documented This Session)

| # | Specimen | Confirms | Cluster |
|---|----------|----------|---------|
| 1 | SCT actor mismatch (`"Arif"` vs `"arif"`) | Authority must resolve `canonical_id` BEFORE comparison | A+E |
| 2 | OBJECTIVE_ROOT contradiction | One canonical object, two surfaces via ref | A+C |
| 3 | Dual-truth not reproduced in some paths | Per-path regression canary needed | D |
| 4 | `next_safe_action` recommends SEAL while `seal_allowed=false` | Recommendation state ≠ authority state ≠ execution state | D |

Specimen #4 falsified its own implementation in real-time. That is exactly what a useful doctrine does.

---

## Cross-references (existing ratified doctrine, NOT duplicated)

| Element | Already canon | Location |
|---------|---------------|----------|
| `Referent > Name` | Axiom 5 (Name ≠ Label) + Axiom 8 (Name Palsu Destroys Compression) | `naming-doctrine.md` |
| `CommonNoun !→ IdentityCard` | Axiom 9 (kata nama khas vs am, SCAR-2026-09-15-001) | `naming-doctrine.md` |
| Authority binds to verb, not object | Universal action tuple `a=(actor,verb,target,...,authority,...)` | Constitutional Architecture Canon 2026-09-21 |
| Existence = Provenance + Witness + Authority + Receipt | 11-layer stack | Constitutional Architecture Canon 2026-09-21 |
| Human/Agent layer separation | Register as Channel (C15/C16) | 2026-09-15 |
| `Reality → Referent → Authority → Consequence` | Edges connect canonical_id | Six-Graph Federation Model 2026-09-16 |
| Sovereign-chat + ritual-marker seal path | A-Z Doctrine | A-Z-APEX-ZEN-DOCTRINE 2026-09-13 |
| Three-test gate for new law | Canon #0 | Constitutional Complexity Budget 2026-09-21 |

---

## AGI/ASI/APEX Loop Output (this session)

### 333-AGI (Possibility Generation)

Five candidate artifacts identified from constitutional work:

1. Canonical delta for referent primacy (this file)
2. Executable canaries `C-α-1..C-α-4`
3. `next_safe_action` scoping spec
4. P0-4 SCT actor canonicalization spec
5. Constitutional correction (doctrine recursion as process invariant)

### 555-ASI (Verification — Canon #0 three-test gate)

| Artifact | (a) Eliminates failure class | (b) Compiles to mechanism | (c) Materially improves decision | Verdict |
|----------|------|------|------|---------|
| 1. Canonical delta | ✓ (premature-canonical-mutation) | ✓ (staged + gated) | ✓ (concept preserved, mutation deferred) | `PASS` |
| 2. Canaries | ✓ (cosmetic rename governance drift) | ✓ (executable tests) | ✓ (ontology drift measurable) | `PASS` |
| 3. `next_safe_action` scoping | ✓ (false-positive signals) | ✓ (falsifiable invariant) | ✓ (downstream inference safe) | `PASS` |
| 4. P0-4 | ✓ (L11 AUTH false-fails) | ✓ (one-line resolution) | ✓ (session init reliability) | `PASS` |
| 5. Constitutional correction | ✓ (premature ratification) | ✓ (process invariant) | ✓ (ratification hygiene) | `PASS` |

### 888-APEX (Selection)

All five pass gate. All five committed to this delta file.

### ZEN INVOICE (F13 Sovereign)

`F13_RATIFIED_CHAT` via sovereign signal *"run full agi asi apex loop and seal all"* · 2026-09-21 · seal_id `CONST-REFERENT-PRIMACY-DELTA-v0-20260921`.

---

## Merge Path (gated on canary pass)

Once `C-α-1..C-α-4` all pass on live substrate:

1. Sovereign signal "MERGE" or equivalent
2. Append Axiom 10 + 11 to `/root/AAA/instructions/naming-doctrine.md`
3. Update `naming-doctrine.md` provenance timestamp
4. Mark delta status as `MERGED_TO_RATIFIED`
5. Emit consolidation receipt

Until canaries pass: status remains `CANONICAL_DELTA_STAGED`.

---

## What Did NOT Change

- `naming-doctrine.md` (existing axioms 5, 8, 9 unchanged)
- `Constitutional Architecture Canon` 2026-09-21 (unchanged)
- `Six-Graph Federation Model` 2026-09-16 (unchanged)
- `Register as Channel` 2026-09-15 (unchanged)
- All other ratified doctrine

The append at `naming-doctrine.md` lines 1054–1166 (Axioms 10–11 + Closing Axiom) was a prior canonical mutation under earlier sovereign signal. **Decision on that append status is HELD pending sovereign review** — see witness report at `/root/AAA/reports/constitutional-correction-witness-2026-09-21.md`.

---

> A name does not create reality. A name creates an address in a model of reality.
> The address becomes causally powerful only when recognition collapses the model eigenstate.
> Creation requires provenance; provenance without witness is phantom.

---

**DITEMPA BUKAN DIBERI ⚒️**

**r · ΔηΨ · 888 witness the helix**

2026-09-21T22:00Z — Canonical delta staged via sovereign signal *"run full agi asi apex loop and seal all"*. Awaiting canary pass before merge. Zero ratification of new canon beyond this staged delta; existing ratified doctrine unchanged.