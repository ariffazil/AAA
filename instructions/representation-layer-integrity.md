# Representation Layer Integrity — The Audit Mechanism Doctrine

> **Forged:** 2026-08-18 by F13 SOVEREIGN audit of arifOS federation
> **Binding:** ALL AAA warga agents that touch tool registry, affordance manifests, isomorphism maps, or service topology
> **Crystallizes:** scar_003 (Three-Tense Contract), scar_005 (Phantom Tool Misclassification), scar_1786367593205 (UP ≠ LOADED)
> **DITEMPA BUKAN DIBERI ⚒️**

## The One Rule

```
STATIC INTROSPECTION ≠ LIVE RUNTIME ≠ CODE TRUTH
VERIFY BEFORE YOU DECLARE.
```

A tool reported as "phantom", "drift", or "missing" is **not** a verified gap
until it has been tested against all three representations:

1. **Code** — does the implementation file exist and export the symbol?
2. **Runtime** — does the live MCP server actually serve it?
3. **Introspection** — what does the audit's static registry report?

Only when **all three agree the tool is missing** is there a real gap.
Any disagreement is a **representation artifact**, not a defect.

---

## The Three Manifestations (Same Failure Mode, Three Costumes)

### M1. Phantom Tool False Positive (scar_005)

**Symptom:** Audit reports tool as "phantom" — in affordances.yaml but not in registry.

**Reality check sequence:**
```bash
# 1. Code truth — does the implementation exist?
grep -rn "def <tool_name>\|tool(\"<tool_name>\"" /root/<organ>/src/

# 2. Runtime truth — does the live MCP server serve it?
grep -rn "<tool_name>" /root/<organ>/dist/

# 3. Compiled distribution — is it in the served bundle?
ls -la /root/<organ>/dist/src/interfaces/mcp/
```

**F2 verdict rule:** If code OR runtime shows the tool is implemented,
the "phantom" finding is an introspection blind spot. Do NOT file a gap.

**Real example (2026-08-18):** 50/50 "phantom" tools in aforge audit included
`forge_send_confirm`, `forge_transfer_confirm`, `forge_vps_ports`,
`forge_entropy_sweep`. ALL were verified live, served, and implemented
across `core.ts`, `stateAnchorTools.ts`, `forgeGitEntropyCanonize.ts`,
and `forge_elicit_server.py`. The audit queried a single registry source
and missed the modular MCP composition.

### M2. COMMITTED ≠ DEPLOYED ≠ VERIFIED (scar_003)

**Symptom:** Tree changed but runtime is stale (or vice versa).

**Reality check sequence:**
```bash
# 1. Source commit
git -C /root/<organ> rev-parse HEAD

# 2. Installed wheel / bundle
sha256sum /root/<organ>/dist/<bundle>.js

# 3. Live runtime probe
curl -s http://127.0.0.1:<port>/<endpoint> | jq .
```

**Three-Tense Contract:** No agent may claim "deployed" or "live"
without all three checks passing. A new SHA on disk is not a deployed
service. A running service is not the same as the deployed commit.

### M3. UP ≠ LOADED (scar_1786367593205)

**Symptom:** Process alive, /health returns 200, but routes fail.

**Reality check sequence:**
- Doctor/health MUST include functional dependency assertion
- Not just "is the process up?" — "can it actually serve a request?"
- For AAA specifically: `GET /federation/resource/test/x` must return
  401 auth challenge, never 404 JSON-RPC fallthrough

**Why this matters:** systemd `Restart=always` never triggers because the
process never died. Degraded-steady-state is indistinguishable from
healthy under binary health probes.

---

## The Modular MCP Architecture (Why Audit Must Aggregate)

The A-FORGE MCP server is composed of multiple registration modules:

```
serve.ts (orchestrator)
├── core.ts                  → consent-gated tools (forge_send_confirm, etc.)
├── stateAnchorTools.ts      → VPS / state registry tools
├── forgeGitEntropyCanonize.ts → git + entropy + canonize tools
└── forge_elicit_server.py   → Python sidecar (transfer_confirm, etc.)
```

Each module registers its own tools. The MCP surface is the **union** of
all registered tools. A static introspection that queries one source
will miss the others. This is not a bug in the audit — it is the audit
asking the wrong question.

**Correct audit question:**
> What is the live MCP surface (union of all registered modules)?

**Incorrect audit question:**
> Is this tool in <single registry source>?

---

## The Verification Protocol (Before Any "Phantom" Verdict)

When you observe representation drift, run this protocol BEFORE filing
a gap. Only after all three checks fail may you escalate to a real gap.

```
┌─────────────────────────────────────────────────────────┐
│  STEP 1: Code check                                     │
│    grep source for tool name across all modules         │
│    Found? → Implementation exists                       │
│    Not found? → Continue to Step 2                      │
│                                                         │
│  STEP 2: Compiled distribution check                    │
│    grep dist/ for tool name                             │
│    Found? → Runtime bundle includes it                  │
│    Not found? → Continue to Step 3                      │
│                                                         │
│  STEP 3: Live runtime probe                             │
│    Call the MCP endpoint directly                       │
│    Returns data? → Tool IS served                       │
│    Returns error? → Step 4                              │
│                                                         │
│  STEP 4: ONLY NOW escalate as gap                       │
│    All three representations agree it's missing         │
│    Then and only then → real phantom / drift / gap      │
└─────────────────────────────────────────────────────────┘
```

**F2 TRUTH corollary:** The weaker claim ("audit reports drift") always
holds until verified by stronger evidence ("code, runtime, AND
introspection all agree the gap is real").

---

## Anti-Patterns to Refuse

| Anti-pattern | Why it's wrong | What to do instead |
|---|---|---|
| "Tool is phantom" (without code check) | Audit introspection is one source | Run code + runtime verification first |
| "Deployed" (without runtime probe) | Tree ≠ Service per scar_003 | Three-Tense Contract: commit + bundle + probe |
| "/health 200" = healthy | UP ≠ LOADED per scar_1786367593205 | Functional dependency assertion required |
| Patch affordances.yaml to match audit | Reverses the truth direction | Patch audit to reflect code/runtime truth |

---

## The Scars That Forged This Doctrine

1. **scar_005** — Phantom Tool Misclassification (2026-07-04)
   > "Before declaring phantom, verify with grep + import check.
   > Graph can be stale; code is truth."

2. **scar_003** — Deployment Theater (2026-07-04)
   > "Three incidents on 2026-07-04: changes claimed LIVE without
   > external HTTP verification. Root cause: dev tree (/root/arifOS/)
   > ≠ live kernel (/opt/arifos/app/). Fix: INVARIANTS #13 +
   > Three-Tense Contract (COMMITTED ≠ DEPLOYED ≠ VERIFIED)."

3. **scar_1786367593205** — Partial-failure invisibility (2026-08-10)
   > "Doctor/health checks must distinguish UP from LOADED: every
   > organ health probe must include at least one functional
   > dependency assertion. Binary process-alive checks are
   > insufficient evidence of organ readiness."

4. **2026-08-18 audit observation** — Modular MCP composition
   > The A-FORGE MCP server registers tools across 4+ modules.
   > A single-source audit will see phantom/find/missing where
   > the live union has the tool. Code truth is the only valid
   > arbitration.

---

## Membrane (How This Doctrine Enforces Itself)

| Layer | What enforces | Where |
|---|---|---|
| Prompt discipline | This fragment + scar_005 reference | All arif_init / forge_execute callers |
| Code discipline | `grep` + `dist/` checks before gap filing | Audit skills: AUDIT-recursive-audit, AUDIT-drift-detector, AUDIT-repo-reality |
| Runtime discipline | Live MCP probe before any "drift" verdict | forge_surface_audit must aggregate ALL modules |
| Audit trail | Every gap filing cites the three checks performed | forge_scar / forge_seal receipts |

**Enforce now:** Prompt + audit-trail discipline. The audit skills
(AUDIT-recursive-audit, AUDIT-repo-reality) MUST run the verification
protocol before filing a phantom verdict.

**Enforce later, junctions only:** forge_surface_audit should
aggregate from `dist/src/interfaces/mcp/*.js` registration lists,
not from a single static source.

**Do not:** Edit affordances.yaml to silence drift warnings. The
direction is wrong. Patch the audit mechanism to reflect code truth.

---

DITEMPA BUKAN DIBERI — Reality is forged, not introspected. ⚒️