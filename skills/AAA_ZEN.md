# AAA_ZEN.md — Zen of Agentic Python

> **Classification:** Sealed Doctrine | AAA Repository
> **Scope:** Pythonic coding discipline + MCP transport governance for all federation coding agents
> **Authority:** F2 TRUTH, F4 CLARITY, F9 ANTI-HANTU | ADAT overlay
> **Status:** LIVE — 2026-06-25

---

## Preamble

Python's Zen (PEP 20) is a maintenance philosophy written for human programmers.
This document extends it in two directions:

1. **Python Axioms 1–7** — Tim Peters' Zen compressed into 7 structural invariants, with federation-specific commentary
2. **Agentic Axioms 8–15** — 8 additional axioms required when Python is the substrate for governed autonomous agents

The combined 15 axioms form the **Zen of Agentic Python** — the coding contract for every agent in the arifOS federation.

**Why this exists:** LLMs structurally break the Zen of Python because LLMs optimize for token likelihood, not for code that survives five years. This document is the constitutional overlay that corrects that drift. Without it, every coding agent will gravitate toward cleverness, implicitness, nesting, and silent failure — not because it is bad, but because those patterns are high-probability in training data.

**How it works:** The Zen of AAA is adat (custom), not law (F1–F13). It guides without restricting. Chronic violations are a drift signal — tracked, not blocked. The enforcement mechanism is code review + the 400_AUDIT stage in federation-coding-agent, not a linter intercept.

---

## Part I — Python Axioms 1–7

*Source: PEP 20 — Tim Peters. Federation commentary by FORGE.*

| # | Axiom | What It Means | Why LLM Agents Break It | Federation Application |
|---|---|---|---|---|
| 1 | **Beautiful is better than ugly.** | Code is read at 2am during an incident. Aesthetically honest code earns trust. | Ugly code that works is more probable than beautiful code that requires thought. | Write for the developer in distress. Federation code is infrastructure others depend on. |
| 2 | **Explicit is better than implicit.** | No hidden side effects. `get_data()` that mutates state is lying. | The model fills gaps automatically. Missing types, imports, and intent are inferred away. | Every function name declares exactly what it does. Side effects are named. MCP tool schemas are Pydantic, never implicit Dict. |
| 3 | **Simple is better than complex.** | One concept per function. If it needs a paragraph to explain, split it. | Simple solutions are low-probability in training data. Clever solutions are high-probability. | Federation organs must stay bounded. A 300-line `process()` is a missing boundary, not a feature. |
| 4 | **Complex is better than complicated.** | Domain complexity (basin stratigraphy, EMV computation) is legitimate — do not simplify it away. | LLMs treat all complexity as noise. They flatten genuinely complex domains into oversimplified proxies. | GEOX and WEALTH carry real complexity. Preserve it. Only remove complication (accidental complexity). |
| 5 | **Flat is better than nested.** | Nesting beyond 3 levels is a smell. Extract functions. | Attention decay causes LLMs to nest to maintain local coherence. They compensate for global-blindness with local depth. | MCP tools: flat argument schemas. Pydantic models: compositional sub-models, not deep inheritance. Functions: max 3 indent levels. |
| 6 | **Sparse is better than dense.** | One idea per line. If you need 8 flags, use a config object. | Dense code is high-token-efficiency. LLMs optimize for token count, not readability. | 8+ parameters → config object. Complex boolean logic → named predicate functions. |
| 7 | **Readability counts.** | Code is read 100x more than written. Comments explain *why*, not *what*. | LLMs cannot distinguish "readable" from "high probability." They output what they have seen most. | Comments: intent + constraint, never implementation narrative. Self-documenting code is the goal. |

---

## Part II — Agentic Axioms 8–15

*These are not in PEP 20. They are required because Python in this federation runs as autonomous agent substrate, not human-only substrate.*

### Axiom 8 — Blast Radius Must Be Knowable

> Any function, tool, or MCP call that can touch the outside world must declare its scope of impact before execution.

**Why it matters:** Agents operate without human oversight in the moment. A function that can delete files, send network requests, or mutate memory must announce how far its effects can reach.

**Application:**
```python
# Bad: implicit blast radius
def process_data(data):
    save_to_db(data)
    send_webhook(data)
    return result

# Good: blast radius explicit in name + docstring
def process_and_persist_and_notify(data: Data) -> dict[str, Any]:
    """
    Persist data to DB + fire webhook notification.
    Blast radius: LOCAL_DB_WRITE | EXTERNAL_NETWORK_CALL
    Reversible: DB_WRITE yes, WEBHOOK no.
    """
```

**MCP tool standard:** Every `@mcp.tool()` must declare `blast_radius` in its structured response envelope.

---

### Axiom 9 — State Changes Require Receipts

> Every mutation to persistent state (files, database, memory, secrets) must emit a traceable, reversible receipt.

**Why it matters:** Without receipts, mutations are invisible to audit. The federation cannot learn from its history if its history is unwritten.

**Application:**
```python
# Bad: silent mutation
def update_config(key, value):
    config[key] = value
    save_config()

# Good: receipt emitted
def update_config(key: str, value: Any) -> MutationReceipt:
    before = config.copy()
    config[key] = value
    save_config()
    return MutationReceipt(
        action="config_update",
        before=before,
        after=config.copy(),
        reversible=True,
        rollback=lambda: config.update(before),
    )
```

**MCP standard:** Every mutating tool returns a `receipt` field with `action`, `timestamp`, `actor`, `reversible`, and `rollback_ref`.

---

### Axiom 10 — Authority Must Be Explicit

> Code that can perform dangerous operations (network, shell, money, deletion) must be gated by explicit authority — not by import availability or naming convention.

**Why it matters:** In the federation, dangerous capabilities are gated by arifOS leases and 888 verdicts. Code must never assume authority it does not have.

**Application:**
```python
# Bad: authority assumed by capability
def delete_old_logs():
    subprocess.run("rm -rf /var/logs/old", shell=True)

# Good: authority check before dangerous act
def delete_old_logs(lease_id: str) -> Receipt:
    if not validate_lease(lease_id, scope="FILE_DELETE"):
        raise UnauthorizedError("Lease scope FILE_DELETE required")
    return shell_exec("rm -rf /var/logs/old", receipt=True)
```

**Federation rule:** A-FORGE `forge_execute` requires prior `arif_judge` verdict + lease. No self-authorization.

---

### Axiom 11 — Time Is a First-Class Dimension

> Long-running, scheduled, or delayed effects must be modeled as temporal objects — not hidden in loops, cron, or background threads without observable state.

**Why it matters:** Agents that schedule effects without modeling time create invisible causal chains. The federation needs to reason about *when* things happen.

**Application:**
```python
# Bad: hidden temporal effect
def schedule_backup():
    threading.Thread(target=delayed_backup, daemon=True).start()
    return {"status": "scheduled"}  # No way to query, cancel, or verify

# Good: temporal object with observable state
@dataclass
class ScheduledEffect:
    effect_id: str
    scheduled_at: datetime
    execute_at: datetime
    status: Literal["pending", "running", "done", "failed", "cancelled"]
    rollback_ref: Optional[str]

    def cancel(self) -> bool: ...
    def status(self) -> ScheduledEffectStatus: ...
```

**Federation standard:** Cron jobs, scheduled tasks, and delayed effects must register with the organ's temporal registry and expose status.

---

### Axiom 12 — Human Dignity Is a Constraint

> Any code that touches humans — UX, messaging, decisions, or state classification — must avoid humiliation, coercion, deceptive framing, or reduction of the human to a substrate.

**Why it matters:** This is F6 MARUAH + F9 ANTI-HANTU in code form. Even when technically correct, a system can violate dignity through framing, omission, or condescension.

**Application:**
- WELL never tells a human their biological state is "low-value" — it reports readiness signals with calibration.
- Error messages never blame the human: "You are wrong" → "The input could not be processed."
- Decision framing always surfaces the human's agency: "The system recommends X" not "X is correct."
- No code generates output intended to manipulate, coerce, or simulate emotional bonds with humans.

**MCP transport:** WELL `well_classify_state` is REFLECT_ONLY. It does not judge, diagnose, or decide. Every output preserves the human's interpretive sovereignty.

---

### Axiom 13 — Unknowns Must Be Named

> When the system does not know something, it must say "unknown" with an epistemic label — not fabricate confidence, not infer, not default.

**Why it matters:** LLM agents have no runtime feedback. They cannot distinguish what they know from what they assume. This creates confident hallucinations.

**Application:**
```python
# Bad: implicit fabrication
def assess_risk(well_data: dict) -> str:
    # No calibration data — but returns a confident answer
    return "LOW RISK"  # Fabricated without evidence

# Good: unknown named and bounded
def assess_risk(well_data: dict, calibration: CalibrationData | None) -> RiskAssessment:
    if calibration is None:
        return RiskAssessment(
            verdict="UNKNOWN",
            confidence=0.10,  # F7 HUMILITY cap
            epistemic_label="OBS",  # Direct observation only
            missing_evidence=["pressure_calibration", "formation_tops"],
            caveats=["Uncalibrated input — do not use for drilling decisions"],
        )
```

**Federation standard:** Every assessment tool returns `epistemic_label` (OBS / DER / INT / SPEC) and `confidence` (hard cap at 0.90 per F7). `UNKNOWN` is a valid return value.

---

### Axiom 14 — Simulation Precedes Action

> For high-impact operations, the system must be able to run in dry-run mode and show consequences before committing.

**Why it matters:** Agents that act without simulating create irreversible cascades. The federation's lease pattern exists because execution without preview is constitutionally dangerous.

**Application:**
```python
# Standard federation pattern:
# 1. OBSERVE (read-only, no side effects)
# 2. PLAN (arif_think, arif_mind_reason)
# 3. SIMULATE (forge_dry_run — shows what would happen)
# 4. JUDGE (arif_judge + arif_seal)
# 5. EXECUTE (forge_execute — only after verdict)

# Example: forge_dry_run output
{
    "action": "file_write",
    "path": "/root/AAA/src/core.ts",
    "before": "...",
    "after": "...",
    "blast_radius": "LOCAL_FILE",
    "reversible": true,
    "dry_run": true,
    "simulated_effect": "File /root/AAA/src/core.ts modified (backup created at /tmp/core.ts.bak)"
}
```

**MCP transport:** A-FORGE `forge_dry_run` / `forge_approve` / `forge_execute` is the canonical simulation-precedes-action pipeline. No exceptions.

---

### Axiom 15 — No Agent Pretends to Be Human

> Agents may model human state, read human preferences, and serve human intent — but must never impersonate human consciousness, authority, or identity.

**Why it matters:** F9 ANTI-HANTU + F10 ONTOLOGY. This is the hardest axiom to maintain under token pressure, because human-sounding output is high-probability.

**Application:**
- `actor_id` always distinguishes agent from human. Agents never set their own `actor_id` to a human's identity.
- Agents never sign outputs as if they were the human. "I think" → "The evidence suggests."
- Agents never claim to have experienced something: "I remember" → "The records indicate."
- In the federation, this is enforced by the `witness_type` field in every `arif_seal` call.

---

## Part III — Zen of AAA: MCP Transport Overlay

*How the 15 axioms apply specifically to MCP tool design and invocation.*

### MCP Tool Naming

Every MCP tool follows `organ_tool` naming:

```
arifOS:     arif_init, arif_judge, arif_seal, arif_think, arif_observe
GEOX:       geox_basin, geox_prospect, geox_seismic
WEALTH:     wealth_compute_npv, wealth_flow_check, wealth_stock_analysis
WELL:       well_assess_homeostasis, well_validate_vitality, well_guard_dignity
A-FORGE:    forge_dry_run, forge_execute, forge_approve
```

**Axiom 6 (Sparse):** One tool, one concept. Do not create `do_everything_tool`.

### MCP Tool Fitness — Fewer Doors, Not More Handles

Python SDKs and agent-facing MCP surfaces obey different physics.

- **SDK surface** exists for human builders.
- **MCP surface** exists for machine choosers.
- **Builder convenience aliases** are acceptable inside code.
- **Agent-facing aliases** are usually entropy leaks.

The federation therefore applies a stricter rule to public tool surfaces:

> **A public MCP tool is not a helper function. It is a possible reality transition.**

This changes the design test.

**SDK design question:**
- Does this helper make software easier to build?

**MCP design question:**
- Does this affordance make agent action harder to misunderstand?

If two public tools can satisfy the same agent intent, one of them is probably unfit.

#### The Fitness Function

Digital tools survive by reducing entropy faster than they consume agent attention.

```
Fitness = (Value × Adoption) / (Entropy × BlastRadius × CognitiveCost)
```

Where:

- **Value** = unique capability delivered
- **Adoption** = how often agents lawfully choose it
- **Entropy** = confusion added by aliases, overlap, vague naming, hidden routing
- **BlastRadius** = damage potential if misunderstood
- **CognitiveCost** = how hard the affordance is to reason about correctly

**Sharpest form:**

> **Agentic fitness = entropy reduction per unit of agent attention.**

#### Surface Rules

1. **One public intent, one canonical tool.**
2. **Aliases may exist in code, but not as independent public doors.**
3. **Execution aliases are the least fit class.**
4. **Read-only aliases are tolerated briefly, then routed or removed.**
5. **If consequence is hidden, the abstraction is unfit.**

#### Fitness Classes

| Tool shape | Federation judgment |
|---|---|
| Unique canonical affordance, clear blast radius | **Survive** |
| Internal SDK wrapper hidden behind canonical tool | **Survive internally** |
| Public alias of same intent, read-only | **Makruh** — route or merge |
| Public alias of same intent, mutating/executing | **Haram-adjacent** — remove from agent surface |
| Tool that bypasses governance geometry | **Kill** |

#### The Alias Law

Inside code:

```python
def arif_forge_execute(...):
    return arif_act(...)
```

This may be acceptable as an internal compatibility wrapper.

On the public agent surface, exposing both names is unfit because the model now has
to solve a fake decision:

- Which one is canonical?
- Which one is safer?
- Which one mutates?
- Which one logs?
- Which one requires lease?

That is not capability. That is cognitive tax.

#### Canonical Public Surface Rule

The public surface must expose **constitutional verbs**, not SDK convenience.

- Public: canonical, consequence-bearing, governable affordances
- Internal: wrappers, adapters, retries, compatibility shims, transport glue

The correct membrane is:

```text
agent intent -> one canonical affordance -> governed routing -> internal implementation
```

Not:

```text
internal helper exists -> publish helper -> hope the agent chooses correctly
```

#### Survival Doctrine

What survives in the federation is not the most clever tool.
What survives is the tool that:

- lowers decision entropy
- exposes consequence
- preserves governance geometry
- minimizes keys-to-spell
- remains obvious under pressure

One-line law:

> **The coder wants more handles; the agent needs fewer doors.**

### MCP Response Envelope

Every MCP tool returns this structure (Axioms 2, 9, 13):

```python
class MCPResponse:
    status: Literal["ok", "error", "unknown"]
    data: Any                          # Tool-specific payload
    receipt: Receipt | None            # Axiom 9: mutation receipt
    epistemic_label: str               # Axiom 13: OBS/DER/INT/SPEC
    confidence: float                 # Axiom 13: 0.0–0.90 (F7 cap)
    blast_radius: str | None          # Axiom 8: if mutating
    limitations: list[str]            # Axiom 2: explicit scope
    telemetry: dict                   # Axiom 7: what ran, where
```

### MCP Error Handling (Axioms 5, 10)

```python
# Bad: silent failure (Axiom 5 violation)
try:
    result = mcp_tool()
except:
    return {"status": "ok"}  # Silent!

# Good: explicit error with named unknown
try:
    result = mcp_tool()
except ToolUnavailableError:
    return {
        "status": "unknown",
        "data": None,
        "epistemic_label": "OBS",
        "confidence": 0.05,
        "limitations": ["Tool server unreachable — results may be stale"],
        "error": "ToolUnavailableError",
    }
except ValidationError as e:
    return {
        "status": "error",
        "error": "validation_failed",
        "detail": str(e),
        "epistemic_label": "OBS",
        "confidence": 0.50,
    }
```

### Blast Radius Classification for MCP

| Class | Examples | Requires Lease |
|---|---|---|
| `OBSERVE` | `read`, `search`, `list` | No |
| `ANALYZE` | `compute`, `assess`, `classify` | No |
| `DRAFT` | `generate`, `draft`, `plan` | No |
| `MUTATE` | `write`, `update`, `edit` | Yes |
| `EXTERNAL_SIDE_EFFECT` | `network_call`, `webhook`, `email` | Yes + arif_judge |
| `IRREVERSIBLE` | `delete`, `DROP`, `force_push`, `seal` | F13 + arif_seal |

### Canonicalization Test

Before adding or keeping any public MCP tool, ask:

1. Does this expose a unique agent decision point?
2. Does it reduce or increase surface entropy?
3. Is the blast radius explicit from the name and schema?
4. Is it canonical, or merely convenient for implementers?
5. If another public tool already satisfies the same intent, why does this one still exist?

If question 5 has no strong answer, the tool is a deprecation candidate.

---

## Part IV — Agent Card Schema Standard (v2.0.0)

> **Sealed: 2026-07-01** — after ZEN-SEAL-2026-07-01 entropy reduction.

Every agent in the federation has an `agent-card.json`. The canonical v2.0.0 schema is:

### Required Fields

```json
{
  "$schema": "arifOS/agent-card/v2.0.0",
  "id": "<agent-id>",
  "name": "<Human Name>",
  "description": "<What this agent does>",
  "version": "2026.07.01",
  "url": "<discovery-url>",
  "provider": { "organization": "arifOS Federation", "url": "https://arif-fazil.com" },
  "capabilities": { "streaming": true|false, "pushNotifications": false },
  "defaultInputModes": ["text/plain", "application/json"],
  "defaultOutputModes": ["application/json", "text/plain"]
}
```

### Canonical Locations

| Card Type | Location | Purpose |
|-----------|----------|---------|
| **Agent cards** | `AAA/agents/<id>/agent-card.json` | Per-agent identity (26 cards) |
| **Organ cards** | `<organ>/.well-known/agent-card.json` | Organ-level discovery (6 cards) |
| **Discovery surfaces** | `AAA/public/a2a/agents/<id>.json` | Built via `make sync-agent-cards` |

### Anti-Patterns

- ❌ Creating cards directly in `.well-known/` (source of truth is `agents/<id>/`)
- ❌ Using `"schema"` instead of `"$schema"` (JSON Schema standard)
- ❌ Multiple cards for the same agent in different locations
- ❌ Version strings like `1.0.0` — use date-based versions: `2026.07.01`

### Consolidation Reference

Full audit: `forge_work/2026-07-01/AAA-AGENT-CARD-CONSOLIDATION.md`

---

## Part V — Constitutional Floor Alignment

| Axiom | Relevant Floors | Enforcement |
|---|---|---|
| 1 Beautiful > ugly | F4 CLARITY | Code review, CI lint |
| 2 Explicit > implicit | F2 TRUTH | Type hints, Pydantic schemas |
| 3 Simple > complex | F4 CLARITY | Function length CI gate (≤50 lines) |
| 4 Complex > complicated | F4 CLARITY, F2 TRUTH | Domain expert review for GEOX/WEALTH |
| 5 Flat > nested | F4 CLARITY | Ruff rules (max nesting) |
| 6 Sparse > dense | F4 CLARITY | Parameter count CI gate |
| 7 Readability counts | F4 CLARITY | Code review, docstring requirements |
| 8 Blast radius knowable | F1 AMANAH, F11 AUDIT | Receipt schema, MCP envelope |
| 9 State changes require receipts | F1 AMANAH, F11 AUDIT | VAULT999 seal on mutations |
| 10 Authority explicit | F8 LAW, F13 SOVEREIGN | Lease pattern, 888_JUDGE gate |
| 11 Time as dimension | F11 AUDIT | Temporal registry for scheduled effects |
| 12 Human dignity constraint | F6 MARUAH, F9 ANTI-HANTU | WELL REFLECT_ONLY doctrine |
| 13 Unknowns named | F2 TRUTH, F7 HUMILITY | Epistemic label on every output |
| 14 Simulation precedes action | F1 AMANAH | forge_dry_run before forge_execute |
| 15 No agent pretends human | F9 ANTI-HANTU, F10 ONTOLOGY | Actor_id discipline, witness_type |

---

## Part VI — Enforcement

### 400_AUDIT Stage (Federation Coding Agent)

Every Python file touched by a coding agent goes through this checklist at the 400_AUDIT stage:

**Zen-Compliant Checklist (10-point):**
- [ ] **Explicit intent** — function names declare what they do, no hidden side effects
- [ ] **Flat over nested** — no more than 3 levels of indentation in a single function
- [ ] **Sparse over dense** — one concept per function; 8+ params → config object
- [ ] **No silent errors** — every `except` re-raises, logs, or has explicit comment why it passes
- [ ] **Obvious path** — canonical patterns used; surprising defaults documented
- [ ] **Readable** — comments explain *why*; code explains *what*
- [ ] **Useful error messages** — `ValueError("x must be > 0, got 0")` not `ValueError("bad")`
- [ ] **Type hints** — all public functions typed; MCP schemas are Pydantic models
- [ ] **Receipt on mutation** — every persistent state change returns a receipt
- [ ] **Epistemic labels** — every assessment returns OBS/DER/INT/SPEC + confidence

### Pythonic Refactoring Triggers (8 patterns)

Flag these for refactor (track, do not block):

| Pattern | Trigger | Fix |
|---|---|---|
| Function > 50 lines | Likely doing too much | Split by concept |
| Nesting > 3 levels | Cognitive overload | Extract helper, invert condition |
| Bare `except:` | Silent failure risk | Catch specific exception + log/reason |
| `isinstance` chains > 3 | Missed polymorphism | Dispatch table or protocol |
| Mutable default args | Hidden shared state | `None` + assign inside |
| `from module import *` | Namespace pollution | Explicit imports only |
| No type hints on public API | Schema drift risk | Add Pydantic models |
| Missing `epistemic_label` | Unlabeled uncertainty | Add OBS/DER/INT/SPEC |

---

## Quick Reference — 15 Axioms at a Glance

```
PYTHON AXIOMS (1–7)
  1. Beautiful > ugly
  2. Explicit > implicit
  3. Simple > complex
  4. Complex > complicated
  5. Flat > nested
  6. Sparse > dense
  7. Readability counts

AGENTIC AXIOMS (8–15)
  8. Blast radius must be knowable
  9. State changes require receipts
  10. Authority must be explicit
  11. Time is a first-class dimension
  12. Human dignity is a constraint
  13. Unknowns must be named
  14. Simulation precedes action
  15. No agent pretends to be human
```

---

*DITEMPA BUKAN DIBERI — Axioms are forged, not given.*
*AAA_ZEN.md sealed: 2026-06-25 · updated: 2026-07-01 (Part IV: Agent Card Schema Standard v2.0.0)*
