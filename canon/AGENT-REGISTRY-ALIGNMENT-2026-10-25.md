# AGENT REGISTRY ALIGNMENT — AAA

**Status:** RATIFIED TERMINOLOGY (F13 request 2026-10-25) · **Owner:** AAA control plane ·
**Enforced by:** `scripts/registry_alignment_check.mjs` (`npm run validate:registry`) ·
**Measured:** 2026-10-25T09:xxZ against `/root/AAA` @ `09eff9b6`

> **Decision in one line:** AAA's agentic surface has **four layers, one owner each**. Identity lives in
> agent cards; catalogue lives in generated indexes; policy lives in policy registries; runtime lives in the
> loader. Any file that carries two layers' claims is a defect, not a source of truth.

---

## 1. Why this document exists

AAA uses its own vocabulary — *warga, lane, organ, FI slot, power band, forge tier*. Google's Agent Registry
uses a different one — *agent, agentic component, MCP server, endpoint, skill, tool, binding, publisher,
runtime reference, registry identifier*. Both describe the same objects.

Without an explicit mapping, three failures recur:

1. **Three files claim to be "the agent registry"** and they disagree. The runtime reads cards; the validator
   reads a YAML filed under `_deprecated_`; the policy file names a third. An agent cannot tell which to patch.
2. **Capability claims are not resolvable.** Agent cards carry 778 `skills[].source` references in the
   committed tree (3,290 in the live worktree). Of the committed 778, **3 resolve to a file**, 171 point at
   paths that do not exist, and 604 declare no source at all. The uncommitted worktree adds 2,512 more refs,
   2,227 of them unresolvable.
3. **A file's folder name contradicts its content.** `federation/_deprecated_20260819/` holds the live
   agent-policy and skill-policy registries that `validate-aaa.mjs` depends on.

This document settles the vocabulary and the ownership. The gate makes regressions fail.

---

## 2. Concept dictionary — Agent Registry term → AAA realization

| Agent Registry term | Meaning | AAA realization | Canonical location | State |
|---|---|---|---|---|
| **Agent** | Autonomous actor defined by identifier + its skills | A2A agent card | `agent-cards/**/agent-card.json` | PRESENT |
| **Agent identifier** | Stable, immutable agent reference | card `id` + DID + key fingerprint | card field; `auth/did_registry.yaml` | PRESENT |
| **Agent principal** | IAM identity that holds permissions + audit trail | `bound_to` / `actor_id` + Ed25519 key | card field; `IDENTITY/keys/` | PARTIAL — no per-agent IAM principal |
| **A2A skill** | Capability described *inline* in the agent card | card `skills[]` | same card | PRESENT, **77% unresolvable** |
| **Skill** (standalone) | `SKILL.md` package + scripts + metadata | `/root/AAA/skills/**/SKILL.md` | `skills/` | PRESENT (949) |
| **Skill revision** | Immutable versioned snapshot | git commit SHA of the skill directory | git | PRESENT (implicit) |
| **Publisher** | Entity that scopes a skill identifier | AAA, `did:arif:aaa` | `auth/sign_agent_card.py` | PRESENT |
| **Agentic component** | Any registrable unit: agent / MCP server / endpoint / skill | the four rows below | — | — |
| **MCP server** | Program exposing tools + data resources over MCP | federation organ MCP endpoint | `federation/organs.yaml` (`mcp` block) + `registry/mcp-tools.yaml` | PRESENT |
| **Tool** | Deterministic function on an MCP server | MCP tool | `registries/tool_registry.canonical.json` (ABI) + `registries/tools.yaml` (policy) | PRESENT, two layers |
| **Endpoint** | Target URL / REST API an agent calls | organ port + public URL | `federation/organs.yaml` | PRESENT |
| **Binding** | Directed connection agent → resource (+ auth provider) | `bound_to`, `routes_to`, `receive_only_from` | card field + `organs.yaml` | PRESENT |
| **Runtime reference** | Physical runtime hosting the component | systemd unit + port + harness | `organs.yaml` + `PORT_REGISTRY.json` | PARTIAL (see D7) |
| **Registry identifier** | Immutable URN assigned at registration | `id` (agent) / path (skill) / `name` (tool) + DID | per component | PARTIAL — no URN scheme |
| **Registration** | Adding a component to the registry | card commit + re-sign + loader reload | `sign_agent_card.py` | PRESENT |
| **Discovery** | Query for consumable components at runtime | `agent-card-registry.js` (live) | `a2a-server/` | PRESENT |
| **Governance project / scope** | Boundary where resources are catalogued + governed | arifOS kernel F1–F13, federation boundary | `:8088` + this repo | PRESENT |
| **Service resource** (writable) | Management handle that produces discovery resources | policy registries (writable) | `registries/*.yaml` | PRESENT |
| **Data resource** | Dataset an MCP server exposes | organ data plane (GEOX, WEALTH, VAULT999) | per organ | PRESENT |

**Translation rule.** When an AAA document says *warga*, write **agent**. *Lane* → **agent identifier**.
*Organ* → **MCP server + endpoint**. *FI slot* → **runtime reference**. *Capability* → **skill or tool**
(never both — a capability is a skill if an agent judges, a tool if a function returns). *Power band* →
**authority ceiling** (policy, not capability).

---

## 3. Four layers, one owner each

| Layer | Question it answers | Owner (single) | Consumers |
|---|---|---|---|
| **L1 IDENTITY** | *Who is this agent and what does it claim?* | `agent-cards/**/agent-card.json` | `agent-card-registry.js`, A2A `/a2a/discover` |
| **L2 CATALOGUE** | *What exists on disk?* | `skills_index.json` (local), `skills_index.federation.json` (cross-organ), `tool_registry.canonical.json` (ABI) | `compass.py`, skill loaders, `generate_tool_census.py` |
| **L3 POLICY** | *What is permitted?* | `registries/agents.yaml` (agent autonomy), `registries/tools.yaml` (tool risk/approval), `federation/organs.yaml` (authority ceiling + endpoints) | `validate-aaa.mjs`, kernel gates |
| **L4 RUNTIME** | *What is live right now?* | loader + health probes | `aaa-a2a`, organ `/health` |

**INV-AR-1.** A file carries exactly one layer's claim. Mixing identity + policy in one file is a defect.
**INV-AR-2.** A *derived* file must name its source (`_derived_view_of` / `superseded_by`) or be deleted.
**INV-AR-3.** A deprecated file must live under a path that says so, or be tombstoned in
`registries/DEPRECATION_REGISTRY.yaml`. A folder named `_deprecated_*` must contain no live dependency.

---

## 4. Measured defects (2026-10-25, `/root/AAA` @ `09eff9b6`)

| # | Defect | Evidence | Severity |
|---|---|---|---|
| **D1** | Validator's agent + skill SOT is filed as deprecated | `validate-aaa.mjs:59,65` reads `federation/_deprecated_20260819/{agents,skills}.yaml`; content is live (`agents: 34`, `skills: 196`, header `total_active: 196`) | **P0** — one folder rename silently kills validation |
| **D2** | Duplicate agent identities across 3 card roots | **Committed tree: 24 duplicated ids.** Live worktree: 96 card files / 54 unique ids / 28 duplicated (4 extra uncommitted). Runtime de-dupes to 57 cards by INV-005 (`/agent-cards/` wins). `federation-agent-card-ops` skill still states `a2a-server/agent-cards/` is canonical — contradicts runtime | **P1** |
| **D3** | Three skill indexes, no declared precedence | `skills_index.json` 945 · `skills_index.federation.json` 754 unique/810 files · `registries/discovery/skills-index.json` 82 · disk 949 `SKILL.md` | **P1** |
| **D4** | Four tool registries, no join declared | `tool_registry.canonical.json` (ABI, 65 ids) · `tools.yaml` (policy, 269) · `federation_tools_sot.yaml` (per-organ) · `registry/mcp-tools.yaml` (9 organs) | **P2** |
| **D5** | Capability claims unresolvable | **Committed tree: 778 card skill refs — 3 resolve, 171 unresolved, 604 no source.** Live worktree adds 2,512 uncommitted refs (2,227 unresolvable) → 3,290 / 2,398 / 808 / 84. 333-AGI sidecar: 3/20 skills exist | **P0** — capability inflation |
| **D6** | Card schema undeclared / drifting | **Committed tree: 1 card without `schemaVersion`.** Live worktree: 53 of 152. 10 distinct `($schema, schemaVersion)` pairs; one claims `v2.5.0` (no such schema on disk); 6 schema files in `schemas/` | **P2** |
| **D7** | Two port sources of truth, unequal scope | `organs.yaml` 30 ports (41 components) vs `PORT_REGISTRY.json` 9 organs / *"Single source of truth for all network ports"*. 6 shared ids all MATCH; 24 organ ports absent from PORT_REGISTRY | **P1** |
| **D8** | Policy declares paths that do not exist | 5 ghost paths in `CANONICAL_REGISTRY_POLICY.yaml` (`AGENT_INDEX.json`, `skills/AAA_SKILL.md`, `.config/federation-models.json`, `arifOS/arifosmcp/config/model_registry.json`, `LEGACY_...deprecated-2026-07-29`) | **P2** |

### D5 detail — the one that matters

A card that claims 20 skills, of which 3 exist, is not a capability description. It is a wish list that
downstream agents will plan against. This is the same failure class as a fabricated receipt: the artifact
asserts something the machine cannot witness. The gate does **not** fix the refs — 2,227 of the live 2,398
were added by uncommitted worktree edits, and fixing means either building the skills or deleting the claims.
Both are content decisions. The gate **freezes** the count on the committed tree (ratchet): unresolved refs
may fall, never rise.

---

## 5. Disposition ledger

| Path | Layer | Disposition | Action |
|---|---|---|---|
| `agent-cards/**/agent-card.json` | L1 identity | **CANONICAL** | none — runtime precedence INV-005 |
| `a2a-server/agent-cards/**/*.json` | L1 identity | **DERIVED mirror** | keep; documented as legacy scan root |
| `agents/**/agent-card.json` | L1 identity | **DERIVED mirror** | keep; `_archive/`, `_superseded/` are not registry inputs |
| `agents/_lanes/_archive/**`, `_superseded/**`, `.archive-*` | L1 | **TOMBSTONED** | excluded from duplicate counting |
| `registries/agents.yaml` *(moved from `federation/_deprecated_20260819/`)* | L3 policy | **CANONICAL** | move + repoint validator |
| `registries/skills.yaml` *(moved from `federation/_deprecated_20260819/`)* | L3 policy | **CANONICAL** | move + repoint validator |
| `federation/_deprecated_20260819/{CAPABILITY_INDEX.json,call_map.yaml,mcp-catalog.yaml}` | L3 | **DEPRECATED** | leave; tombstoned, unreferenced by code |
| `registries/AGENTS_UNIFIED.yaml` | L1 taxonomy view | **DERIVED** | identity lanes + FI slots + organs taxonomy; not an agent list |
| `a2a/registry/agents.yaml` | L4 operational | **DERIVED** | A2A binding view (34, `agent_id`) |
| `skills_index.json` | L2 catalogue | **CANONICAL (local)** | generated by `scripts/skills_index_gen.py` |
| `skills_index.federation.json` | L2 catalogue | **DERIVED (cross-organ)** | 5 roots, priority AAA > arifOS > HERMES > A-FORGE > kimi-code |
| `registries/discovery/skills-index.json` | L2 | **DEPRECATED** | 82 entries, 2026-06-22; superseded by `skills_index.json` |
| `registries/tool_registry.canonical.json` | L2 catalogue (ABI) | **CANONICAL** | implementation tool surface |
| `registries/tools.yaml` | L3 policy | **CANONICAL** | risk tier, approval policy, witnesses |
| `docs/federation_tools_sot.yaml` | L2 per-organ enumeration | **DERIVED** | `generate_tool_census.py` owns it |
| `registry/mcp-tools.yaml` | L4 endpoint/tool count | **DERIVED** | 9 organs; needs regeneration against `organs.yaml` |
| `federation/organs.yaml` | L3 policy + L4 endpoint | **CANONICAL** | 41 components, authority ceilings, ports |
| `registries/PORT_REGISTRY.json` | L4 endpoint | **DERIVED subset** | 9 organs; `_canon` claim narrowed to "probed slice" |
| `schemas/agent-card-v2.3.0.schema.json` | L1 schema | **CANONICAL** | v2.0–v2.2 retained for audit only |

---

## 6. Invariants

- **INV-AR-4.** Every `skills[].source` in a card resolves from repo root **or** is an absolute path. Ambient
  `$HOME`-relative paths are forbidden — a card is a repo artifact, not a shell session.
- **INV-AR-5.** Every entry in a skill index resolves to a real `SKILL.md`.
- **INV-AR-6.** A tool id is unique across the tool catalogue layer; the policy layer may only reference ids
  that exist in the catalogue.
- **INV-AR-7.** Every path named as `canonical` in `CANONICAL_REGISTRY_POLICY.yaml` exists, or carries
  `external: true` with an absolute path.
- **INV-AR-8.** No executable consumer reads from a path segment matching `_deprecated_`, `_archive`,
  `_superseded`, or `.archive-*`.

## 7. Gate

```bash
npm run validate:registry      # scripts/registry_alignment_check.mjs
```

Exit 0 = aligned. Exit 1 = one or more INV-AR violations, printed with file + line detail.
Baseline counts live in `registries/CANONICAL_REGISTRY_POLICY.yaml::alignment.baseline` — the ratchet.
A count that rises is a failure; a count that falls should be re-baselined in the same commit.

## 8. Scope of this pass

This pass settles **terminology, ownership, and the gate**. It does not:
- repair the 2,398 unresolvable skill references (content decision: build or delete, per agent);
- delete duplicate cards (they are mirrors; deleting them changes A2A discovery — F13 call);
- touch `/root/AAA` or `/root/AAA/.git` (both `chattr +i`; immutable by design);
- promote any agent's authority. Terminology alignment is not an authority grant.

**DITEMPA BUKAN DIBERI.**
