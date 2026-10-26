# Architecture-vs-Liveness Audit — "is this subsystem alive?"
> **Provenance:** recovered 2026-10-23 from KVM4 (`/root/.hermes/skills/software-development/live-probe-audit-pattern/SKILL.md`) by `skills-catalog-drift.py`.
> This section existed on KVM4 and was **absent from the whole KVM8 tree** — a casualty of
> consolidation-by-heading rather than consolidation-by-content. Body is verbatim; nothing
> added. KVM8-side home chosen by subject, not by the peer's folder layout.

## Architecture-vs-Liveness Audit ("is this subsystem alive?")

**Signal:** A report (or Arif) claims a subsystem exists with impressive architecture — state machines, gates, leases, sandboxes, promotion pipelines. The question is not "do the files exist?" but "is any agent actually using this end-to-end?"

**Scar (2026-08-02):** Arif shared an external agent's Eureka narrative about A-FORGE's ephemeral capability pipeline. The narrative was architecturally correct — 20+ real files, 1,100+ line canonical engine, bwrap sandbox, 10+ tests, 5 built-in templates, evidence-based promotion gate. But the system was operationally dormant: zero production calls, no agent configured to invoke it, and the promotion gate was mathematically unreachable (score defaults to 0.0, threshold requires 0.80, the code that populates the score isn't wired).

**The 10-question liveness probe (run ALL before any "it works" verdict):**

```
Q1. Does the tool appear in the live MCP surface?
    → grep registration in core.ts / server setup; check tools/list

Q2. Are the domain files real implementations or stubs?
    → wc -l each file; check for actual logic vs print/banner stubs
    → (see deployment-claim-verification pitfall #31 for stub detection)

Q3. Is the sandbox/execution backend actually installed?
    → which bwrap; bwrap --version; testBackend() equivalent

Q4. Do templates/recipes exist and are they usable?
    → grep registerBuiltinTemplates / seedTemplates; count entries

Q5. Is there test coverage?
    → find test/ -name "*ephemeral*" -o -name "*sandbox*" etc.

Q6. Is any agent CONFIGURED to call this tool?
    → grep -rn "tool_name" ~/.hermes/ ~/.claude/ ~/.opencode* /root/HERMES/
    → This is the most commonly missed check. A tool nobody calls is dormant.

Q7. Are promotion/retirement gates mathematically reachable?
    → Read the threshold constants AND the default values of their inputs.
    → If input defaults to 0.0 and threshold requires 0.80, and the code
      that populates the input says "P2; defaults to 0.0 until then" —
      the gate is DEAD BY CONSTRUCTION. No entity can ever pass it.

Q8. Are cross-module dependencies actually wired?
    → grep -rn "import.*ModuleB" ModuleA.ts
    → A file can exist with beautiful spec but zero imports from the
      canonical engine. Existence ≠ integration.

Q9. Is the MCP transport network-reachable or stdio-only?
    → ss -tlnp | grep <port>; ps aux | grep <process>
    → stdio transport = library waiting to be spawned, not a live server.

Q10. Has the full lifecycle ever been exercised end-to-end?
    → Search logs, session history, VAULT999 for any production invocation.
    → "No permanent promotion test yet" = the promote→seal path is theory.
```

**Three dormancy patterns (proven 2026-08-02):**

| Pattern | Tell | Example |
|---------|------|---------|
| **No consumer** | Tool registered, zero agent configs reference it | forge_ephemeral not in any Hermes/Claude/OpenCode config |
| **Dead gate** | Threshold requires X, input defaults to 0, populator says "P2" | empirical_capability_score=0.0 forever, threshold=0.80 |
| **Unwired module** | File exists, canonical engine doesn't import it | worldModelTraining.ts + multiModelEvaluator.ts: grep returns zero imports from EphemeralGenesis.ts |

**Verdict template:**

```
Architecture: REAL / STUB / PARTIAL
  [evidence: file count, line count, test count]

Operationally: LIVE / DORMANT / PARTIAL
  [evidence: production calls, agent configs, gate reachability]

Gates: REACHABLE / DEAD BY CONSTRUCTION
  [evidence: threshold vs default value, populator wiring status]

Cross-module wiring: WIRED / UNWIRED
  [evidence: grep imports between modules]
```

**Key discriminator:** "Architecture real, operationally dormant" is a VALID and COMMON verdict. Don't collapse it to "it works" (files exist) or "it's fake" (nobody uses it). Report both halves honestly.

Full worked example: `references/aforge-ephemeral-liveness-audit-2026-08-02.md`.

