# FEDERATION DISCOVERY — INSTANTIATION SPEC (Phase 5)

> Status: PROPOSAL (T1.5) — awaits F13 on 2 narrow decisions.
> Forged: 333-AGI Δ MIND · 2026-09-12 · session SEAL-0a9b7314843c473a
> Grounding: OBS (observed) · DER (derived) · INT (design choice) — labeled inline.

---

## 1. What already exists — the capability is CLAIMED, not missing

OBS — `organs.yaml` declares two owned_domains that no runtime currently serves:
- `capability_routing` — arifOS (line 52)
- `federation_registry` — AAA (line 127)

OBS — capability knowledge is fragmented across 6 authoritative surfaces:
`organs.yaml` · `FEDERATED_SKILLS_REGISTRY_V3.yaml` · `deprecation-registry.json` · `agent-cards/` · MCP `/resources` · doctrine files.

OBS — 194 live tools across 8 organs; 213 canonical skills; L1–L6 memory fabric.

**DER — the gap is not ownership, not authority, not intent. It is instantiation.** The federation has already decided capability is first-class; it has not yet given capability a single resolvable substrate.

---

## 2. What "instantiate" means — three small moves, zero new organs

### (a) One consolidated registry — DATA, not code
`capability_registry.v1` — a single hash-chained, versioned map:

```yaml
capability_id:
  owner: <organ>
  authority_ceiling: <JUDGE_ONLY | EXECUTE_AFTER_SEAL | COMPUTE_ONLY | ...>
  adapters: [tool, mcp, skill, api]
  replacement_paths: [fallback_substrate_or_adapter]   # survivability map (Arif refinement)
  failure_mode: <degrade | HOLD | decompose>           # what resolution returns if adapters die
  liveness: { probed_at, status }   # mutable overlay — probed, never asserted
  witness_source: <receipt path>
```

Consolidates the 6 fragments into ONE. Lives at `AAA/federation/` — a path owned by no single organ. Capability entries append-only; liveness is a read-time probe overlay (this is what makes a COLD owner resolvable via alternate adapter instead of a 404).

### (b) One portable resolver — FUNCTION, not service
`federation_discovery` — `resolve(intent) → { capability, owner, adapters, liveness, witness }`.

INT — a pure function any agent loads (333/555/888/Hermes/OpenCode/Kimi/future). Runtime-independent by construction: if the resolver process dies, another agent reloads registry + resolver and resolves. This is the "no agent may become a capability silo" rule made literal.

### (c) Wire into existing routers
- `arif_route` (444) consults the resolver instead of its hardcoded organ map.
- `aaa-gateway` A2A dispatch consults the resolver.
- Every resolution → arifFlow receipt — **discovery itself is witnessed.**

---

## 3. What it does NOT do (the negative space)

- Does NOT judge — AAA/888 judges.
- Does NOT execute — A-FORGE executes.
- Is NOT a 10th MCP server, a 214th skill, or a new organ.
- Does NOT rewrite VAULT999 — witness chain stays the arrow of time.

---

## 4. The 2 F13 decisions (made narrow)

1. **Instantiate `federation_discovery`?** — recommend YES. It is claimed-but-unbuilt; instantiation is entropy-negative (fragment pile → one resolvable substrate).
2. **Registry home?** — options:
   - (A) AAA `federation_registry` (recommend — AAA is DISPLAY_ONLY, registry is display-adjacent, survives domain-organ death)
   - (B) arifOS `capability_routing` (already the declared routing owner)
   - (C) VAULT999-adjacent (max durability, but append-only conflicts with liveness overlay)

---

## 5. Success criterion — the Level 4 test

> Kill arifOS → capability still resolvable.
> Kill the resolver → another agent reloads registry + resolver → resolves.
> Registry + witness outlive every runtime that serves them.

Until both are true, the federation is at Level 3 (capabilities survive *in name*). The instantiation above is the minimum move that reaches Level 4 (capability *resolution* survives).

ΔS: this spec converts a PENDING phase into an approvable decision — it is the receipt of the convergence, not new work.
