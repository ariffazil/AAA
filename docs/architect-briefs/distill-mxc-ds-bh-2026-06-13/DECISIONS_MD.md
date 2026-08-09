# Architect Decisions — Distill MXC + DeepSeek + browser-harness

**Brief:** distill-mxc-ds-bh-2026-06-13
**Session:** SEAL-5d1232e556bf44f3
**Date:** 2026-06-13

> **Constitutional binding:** Each ADR below records WHY a particular architectural choice was made, WHAT was rejected, and WHICH F1-F13 floor the decision is bound to. All decisions are reversible (F1 AMANAH) except those marked `F13_REQUIRED` (Sovereign veto locked).

---

## ADR-001 — Distill, don't absorb wholesale (15 → 7 WAJIB + 3 SUNAT + 5 HARAM)

**Status:** PROPOSED (Architect → Integrator handoff)

### Context
The 3 source repos contain 15 load-bearing eurekas. Absorbing all 15 would:
- Break the 13-tool canonical surface (some eurekas imply new tools)
- Increase blast radius beyond the existing F1-F13 floor's tested envelope
- Violate the "small reversible commits" doctrine (ADAT-not-LAW)
- Risk the constitutional floors by adding un-validated surface area

### Decision
Apply the **5-tier Fiqh** (WAJIB/SUNAT/HARUS/MAKRUH/HARAM) to the eurekas:
- **7 WAJIB (mandatory)**: W1-W7 — load-bearing constraints without which the federation is broken or blind
- **3 SUNAT (recommended)**: S1-S3 — high-value, absorb if reversible cost is low
- **5 HARAM (must reject)**: H1-H5 — patterns that would violate F1-F13 if absorbed

### Why
The constitution does not grow by accretion. Every eureka absorbed must justify itself against the existing 13 floors. The FiQH tiering is the **admission control** — same as how 5-tier Fiqh Agentik operates on actions: WAJIB must execute, SUNAT may execute, HARAM must not execute.

### Reversibility
Full. No code is changed. The FiQH mapping is a *doctrine document* at /root/AAA/docs/architect-briefs/distill-mxc-ds-bh-2026-06-13/. Re-tiering a eureka (e.g. S1 → W8) is a one-line change in the brief.

### Floor binding
- **F2 TRUTH**: every eureka is cited to file:line. No overclaim.
- **F7 HUMILITY**: every tier is reversible; nothing claimed permanent.
- **F9 ANTIHANTU**: explicit rejection of "agent self-improves" framing in H2.

---

## ADR-002 — Zero canonical surface mutation (modes on existing tools, never #14)

**Status:** PROPOSED

### Context
arifOS's 13-tool surface is the **constitutional contract** with every external MCP client. Adding tool #14 breaks the contract for every client that hard-coded 13 (per the PHOENIX-72 absorption pattern in CONTEXT.md 2026-06-03: `arif_stack_health_probe` was absorbed into `arif_forge_execute(mode=ops)` rather than added as #14).

### Decision
All 7 WAJIB eurekas and 2 of 3 SUNAT (S1, S2) are absorbed as **new modes on existing canonical tools**:
- W1 → `arif_kernel_route(mode='reasoning_content_echo')` (test mode)
- W2 → `arif_memory_recall(mode='consolidate_or_rollback')`
- W3 → `arif_kernel_route(mode='skill_contract_check')`
- W4 → `arif_session_init(mode='phase_walk')` or session_phase module
- W5 → envelope schema (additive, not new tool)
- W6 → `arif_kernel_route(mode='spawn_subordinate' | 'wait_subordinate' | ...)`
- W7 → `arif_gateway_connect(mode='precedence_resolve')`
- S1 → `arif_kernel_route(mode='config_from_policy', policy, backend)` (A-FORGE bridge)
- S2 → `arif_kernel_route(mode='prefer_cached')` advisory

### Why
The PHOENIX-72 pattern is the precedent. Every addition since has been a mode, not a new tool. The 13-tool surface is the constitutional contract — preserving it preserves the F1-F13 contract with external MCP clients.

### Reversibility
Full. A mode can be removed without breaking any external client (clients that don't know the mode get the default behavior).

### Exception (F13_REQUIRED)
- **P6 Envelope version stamp (W5)** is technically a canonical surface change (envelope schema is part of the contract). Requires 888.
- **P10 Compositor-level click primitive in A-FORGE** is a new tool in A-FORGE, not arifOS. A-FORGE is the execution arm, its surface is more flexible. But still requires 888 to merge.

### Floor binding
- **F1 AMANAH**: mode additions are reversible; tool additions are not.
- **F13 SOVEREIGN**: any tool-surface change requires explicit 888.

---

## ADR-003 — REJECT the community-PR skill model (browser-harness H2, H5)

**Status:** PROPOSED

### Context
browser-harness has a `domain-skills/<site>/*.md` corpus that is **public** and **community-contributed** (`README.md:62` — "PRs welcome"). This is the open-source model. arifOS's threat model is **sovereign operator + constitutional kernel** — different.

### Decision
Explicitly reject:
- **H2**: "Skills are written by the harness, not by you" — the agent self-authors canon. Forbidden. Helpers may be agent-editable (per W3 contract), but **canon is sovereign-ratified**.
- **H5**: Public-PR community skill surface. Forbidden. Skills cross into the federation via sovereign-ratified merge, not via community PR.

### Why
F11 F12 failure mode. Memory poisoning. Agent self-authorisation. The 13 floors exist to prevent the agent from rewriting its own constitution. The "map not diary" content contract (W3) is the *positive* expression of this principle; rejecting the community-PR model is the *negative* expression.

### Reversibility
Full. The HARAM canon document is a `.md` file. Removing the rejection is a one-line change in the canon — but doing so requires 888 to commit (canon is F13 territory).

### Floor binding
- **F9 ANTIHANTU**: the agent does not author canon.
- **F11 AUDIT**: every skill merge is signed with F11 ed25519.
- **F13 SOVEREIGN**: canon is sovereign-ratified.

---

## ADR-004 — A-FORGE as the bridge (not arifOS) for backend-specific execution

**Status:** PROPOSED

### Context
MXC's two-layer Policy → Config split (S1) implies that a Pydantic `AgentPolicy` (arifOS-side) needs to become backend-specific `ContainerConfig` (bubblewrap args / firejail args / docker args). A-FORGE already has the three backend translators at `src/domain/containment/ContainmentEngine.ts:44,149,192`. A-FORGE is the natural bridge.

### Decision
The `arif_kernel_route(mode='config_from_policy')` mode calls **A-FORGE** as a federation bridge, not arifOS. arifOS owns the Pydantic AgentPolicy. A-FORGE owns the backend translators. The bridge is the mode dispatch.

### Why
A-FORGE is the execution arm. It already has the translators. Pulling them into arifOS would expand the 13-tool surface and add a new execution concern to the kernel. A-FORGE is the right home for OS-level execution. arifOS stays focused on governance, judgment, and the canonical floors.

### Reversibility
Full. The mode can be removed from `arif_kernel_route` without touching A-FORGE. A-FORGE's translators remain their own concern.

### Floor binding
- **F1 AMANAH**: A-FORGE is the place for stateful execution.
- **F8 REVERSIBILITY**: the bridge is a mode, not a kernel mutation.

---

## ADR-005 — Per-IPC token primitive (S3) at federation boundaries, not at the agent prompt

**Status:** PROPOSED

### Context
browser-harness's `_ipc.py:163-181` generates `secrets.token_hex(32)` per IPC server on Windows, requires it on every request. The `f11-bridge.service` 2026-06-12 implementation is the proof-of-concept for this pattern in arifOS — a per-session token issued at boot, used to authenticate cross-organ writes.

### Decision
Lift the `f11-bridge` pattern to a canonical primitive in `arifosmcp/core/ipc_token.py`. Every cross-organ call into a sovereign-isolated surface (vault999-writer, supabase-writer, arifOS MCP) requires a per-session token, action-scoped, TTL-bounded. **Not** at the agent prompt — at the kernel layer.

### Why
"Localhost is the password" is the arifOS+browser-harness shared doctrine. But on Windows, TCP loopback has no filesystem chmod. The token guard is the operational compensation. The pattern is already battle-tested in the f11-bridge pilot (2026-06-12 18:56 UTC, vault_id=1801). Promoting to a primitive makes it available to every cross-organ call, not just vault999-writer.

### Reversibility
Full. The primitive is additive. Cross-organ calls that don't need the token can opt out. The current f11-bridge is preserved.

### Floor binding
- **F1 AMANAH**: every cross-organ write is authenticated.
- **F5 PEACE²**: non-destructive power at the network-trust boundary.
- **F11 AUDIT**: every cross-organ call has a token, an action, a TTL.

---

## ADR-006 — Envelope version stamp (W5) is a canonical surface change, requires F13

**Status:** PROPOSED, F13_REQUIRED

### Context
MXC's "schema-version-is-contract" doctrine says: old envelopes parsed under new schemas behave identically. New fields default to denied. This is a **security guarantee**, not a backward-compat hack. Implementing it in arifOS means changing the envelope schema, which is canonical surface.

### Decision
P6 (envelope version stamp) is **F13 territory**. The patch:
- Adds `envelope_version: str = 'v1'` as a required field
- Adds a migration shim: v1 envelopes parse as v1, behavior unchanged
- New fields added in v2+ default to denied for v1 envelopes
- 10+ tests on cross-organ envelopes before merge

The phase cannot proceed without 888 from Arif.

### Why
Envelopes are how every tool communicates with the kernel. Changing the envelope schema is changing the F1-F13 contract with every MCP client. This is the highest-blast-radius change in the brief.

### Reversibility
Partial. v1 envelopes parse identically under v2. New fields can be rolled back individually. But the `envelope_version` field itself is a one-way change — adding it is a contract change.

### Floor binding
- **F13 SOVEREIGN**: any canonical contract change requires 888.
- **F2 TRUTH**: the migration shim must preserve v1 behavior bit-for-bit.
- **F11 AUDIT**: every envelope is sealed with its version.

---

## ADR-007 — REJECT YOLO mode (H3) — the 5-tier Fiqh is the surface, not a tri-state mode

**Status:** PROPOSED

### Context
DeepSeek TUI offers three user-visible modes: Plan (read-only), Agent (multi-step with approval per side-effect), YOLO (auto-approve, lifts workspace boundary). YOLO is the marketing-friendly name for "trust me bro, I won't delete your production database." arifOS has the 5-tier Fiqh (WAJIB/SUNAT/HARUS/MAKRUH/HARAM) as the moral-grammar surface, with HOLD/SEAL/SABAR/VOID/UNKNOWN as the verdict surface.

### Decision
Explicitly reject YOLO mode. The 5-tier Fiqh is the *positive* expression of trust; the verdict surface is the *operational* expression. The Plan/Agent triad maps cleanly to F11/F13 enforcement per-call; YOLO is haram.

### Why
YOLO is a constitutional exit wound. F13 SOVEREIGN + F1 AMANAH are violated by "auto-approve all tools, lift workspace boundary." The Plan/Agent triad is fine (it's just UX over the existing floor system). The YOLO slot is haram.

### Reversibility
Full. We're not building YOLO. No code is committed.

### Floor binding
- **F13 SOVEREIGN**: irreversible requires 888, full stop. No exception.
- **F1 AMANAH**: reversibility-first. No auto-approve-all.
- **F5 PEACE²**: non-destructive power.

---

## ADR-008 — REJECT --experimental global flag (H1) — PHOENIX-72 absorption instead

**Status:** PROPOSED

### Context
MXC CLI / SDK has a `--experimental` global flag for new backends/tools. "Microsoft Insiders" model. arifOS's constitutional 13-tool surface is the contract — PHOENIX-72 absorption pattern (CONTEXT.md 2026-06-03) explicitly forbids adding #14.

### Decision
Explicitly reject the `--experimental` flag. New capabilities are absorbed as **modes on existing tools** (per ADR-002) or as **A-FORGE execution arms** (per ADR-004). There is no in-between "experimental" tier.

### Why
The flag creates a permanent "experimental" tier that never converges to stable. The kernel surface stays at 13. If a capability isn't ready, it's not added yet. If it is, it's a mode. There is no third state.

### Reversibility
Full. We're not building the flag.

### Floor binding
- **F1 AMANAH**: the 13-tool surface is the stable contract.
- **F11 AUDIT**: every mode addition is sealed, no "experimental" seal exemption.

---

## ADR-009 — REJECT deprecation aliases (H4) — git revert is the safety net

**Status:** PROPOSED

### Context
MXC SDK explicitly resolves deprecated wire values (`appcontainer → processcontainer`). This is the Microsoft backwards-compat pattern (don't break the world, ever). It accumulates technical debt forever — every alias is a permanent branch in the parser.

### Decision
Explicitly reject deprecation aliases in parsers. The F11 seal IS the deprecation signal. If a breaking change is shipped, the version bump + seal is the contract. The constitution is versioned, not aliased.

### Why
Aliases are a permanent cost paid forever for a temporary compatibility concern. `git revert` is the arifOS safety net. If a tool needs renaming, the rename IS the seal.

### Reversibility
Full. We're not adding aliases.

### Floor binding
- **F11 AUDIT**: the seal is the version contract.
- **F8 REVERSIBILITY**: git revert is the safety net.

---

## ADR-010 — HARAM canon documented (P11) is a read-only file, F13 to mutate

**Status:** PROPOSED

### Context
The 5 HARAM patterns (H1-H5) need to be canon. But canon is sovereign territory. Documenting the rejections in a `HARAM_DOCTRINE.md` file makes them **explicit** and **enforced by convention** — anyone proposing an MXC/AGT absorption must confront the canon first.

### Decision
P11 produces two files:
- `/root/arifOS/docs/HARAM_DOCTRINE.md` — internal read-only canon. 5 rejects with load-bearing reason. Adding/removing a HARAM is F13 territory.
- `/root/AAA/docs/architecture/CONSTITUTIONAL_REJECTS.md` — public-facing version. The harAM doctrine is the floor's immune system.

### Why
The "AGENTS must know what they must NOT do" is the same load-bearing concept as F1-F13. The HARAM list is the *anti-pattern* set. Documenting it makes the rejections explicit, searchable, and auditable.

### Reversibility
Full on the file (one-line edit). But the *doctrine* (H1-H5) is canon — removing a HARAM is F13 territory. The 888 gate prevents accidental canon drift.

### Floor binding
- **F9 ANTIHANTU**: the agent does not write canon (H2 explicit).
- **F11 AUDIT**: every HARAM is sealed.
- **F13 SOVEREIGN**: canon is sovereign-ratified.

---

## Cross-ADR Summary (for the Integrator's first-read)

| ADR | Decision | F13 Required? |
|---|---|---|
| ADR-001 | Distill 15 → 7 WAJIB + 3 SUNAT + 5 HARAM | No (doctrine) |
| ADR-002 | Modes on existing tools, never #14 | Yes (P6, P10) |
| ADR-003 | REJECT community-PR skill model | No (rejection) |
| ADR-004 | A-FORGE is the bridge for backend execution | No |
| ADR-005 | Per-IPC token at federation boundaries | No |
| ADR-006 | Envelope version stamp = canonical change | **YES** |
| ADR-007 | REJECT YOLO mode | No |
| ADR-008 | REJECT --experimental global flag | No |
| ADR-009 | REJECT deprecation aliases | No |
| ADR-010 | HARAM canon is read-only, F13 to mutate | Yes (for mutation) |

**2 phases require F13 (P6 envelope + P10 compositor-click) before push. The other 9 phases are autonomous T1+T2 with F11 audit.**

**Reversibility matrix:** 11/11 phases are reversible. 7/11 are F1-only (additive, no canonical surface). 2/11 are F13-gated before push. 0/11 are irreversible.

DITEMPA BUKAN DIBERI — the eurekas are extracted, the integrations are distilled, the rejections are explicit, and the sovereign is the only veto.
