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
| **Agent identifier** | Stable agent reference | **six layers — see §2b** | card + DID + keys | **SPLIT, see matrix** |
| **Discovery identifier** | Lookup / metadata only | none — no URN scheme | — | **ABSENT (0/47)** |
| **Governed resource ref** | What policy targets | agent card path (implicit) | `agent-cards/**` | **PARTIAL — implicit only** |
| **Credential principal** | Who is calling | `public_key.hex` + `signature_status` + DID registry | card fields | **PARTIAL (4/47 keys)** |
| **Runtime reference** | Where it runs | `runtime_harness` + organs systemd/port | card + `organs.yaml` | **PARTIAL (6/47)** |
| **Authority envelope** | What it may do | `authority_ceiling` / `authority` | card | **OVER-CLAIMED (45/47)** |
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

## 2b. Identity is not one string — corrected on second pass

**Correction of this document's own first pass.** §2 originally compressed identity into a single row:
*"card id + DID + key fingerprint"*. That was wrong, and the machine proves it. AAA answers six different
questions with one object, so a card can claim authority it cannot authenticate.

| Layer | Question it answers | AAA field today | Measured (47 unique live cards) | State |
|---|---|---|---|---|
| **Discovery id** | *Which logical component is this?* | none — no URN scheme | **0/47** | **ABSENT** |
| **Resource ref** | *What does policy target?* | agent card path, implicit | 47/47 implicit | **PARTIAL** — no formal name |
| **Credential principal** | *Who is calling?* | `card.public_key` · `agents/**/identity.json` · `IDENTITY/keys/*_public.pem` · DID registry | **22/47 resolvable** (card 4 · identity.json 8 · keys 10) · card-scoped only: 4/47 | **PARTIAL** |
| **Runtime ref** | *Where is it running?* | `runtime_harness` + `organs.yaml` systemd/port | **6/47** cards | **PARTIAL** |
| **Authority envelope** | *What may it do?* | `authority_ceiling` / `authority` | **45/47** (38 actor-class · 7 service-class) | **OVER-CLAIMED** |
| **Lifecycle** | *Is it alive, retired, drift?* | `status` | 11/47 | **PARTIAL** |
| **Verdict ref** | *Was this action authorised now?* | none on card (correct — kernel owns it) | 0/47 | **ABSENT by design** |
| **Receipt** | *What actually happened?* | `registry_receipt_hash` | 46/47 | **PARTIAL** |

> **Second correction (2026-10-25, after reviewing the card schema).** The first matrix was
> card-scoped and under-counted principals by 5.5×: it read only `card.public_key.hex`, while AAA
> keeps principals in `identity.json` and `IDENTITY/keys/`. Correct scope: **22/47 resolvable**.
> Service-class cards (organs, pillars, functions, `*-mcp`) are excluded from the agency test — an
> MCP surface legitimately has **no** agent principal; `authority_ceiling` on an organ is *service*
> authority, not agency. The remaining gap is **18 of 38 actor-class authority claims** with no
> resolvable principal.

### Identity laws (binding for AAA documents)

```
L1  Discovery         ≠ Identity        finding a name proves an entry exists, not who controls it
L2  Identity          ≠ Principal       a card ID is a label; a principal is a verifiable caller
L3  Principal         ≠ Runtime         the same actor survives machine, container and harness swaps
L4  Runtime           ≠ Authority       a healthy process is not an authorised one
L5  Authority         ≠ Capability      capability says what is possible; authority says what is permitted
L6  Capability        ≠ Permission      permission is granted per action, not possessed in general
L7  Permission        ≠ Judgment        judgment is the kernel's; execution is A-FORGE's; witness is the vault's
```

Canonical compression:

```
Name ≠ Identity ≠ Principal ≠ Runtime ≠ Authority ≠ Capability ≠ Permission ≠ Judgment ≠ Execution
```

### Where AAA currently collapses them

| Collapse | Evidence | Consequence |
|---|---|---|
| Authority ← card field, principal not required | **18/38** actor-class authority claims have no resolvable principal (card-scoped key: 4/47) | a card can assert a ceiling with nothing to verify it against |
| Authorization ← **two** allowlists | `server.js:2933` 47 names (name is a **pre-filter** only — DID signature is enforced at 3011–3048 and `effectiveSourceAgent = didResult.organId`). `federation_envelope.js:279` holds a **second** 15-name list that still admits `anonymous`, mounted on 8 `/a2a` routes via `jsonRpcValidate` | 34 server-admitted actors — including 333-AGI, 555-ASI, 888-APEX — are absent from the envelope list |
| Runtime ← documentation | 33/38 actor-class authority claims declare no `runtime_harness` | "who may act" is asserted without "where it runs" |
| Lifecycle ← prose | 28/38 actor-class authority claims have no `status` | a retired actor and an active one look identical to a reader |
| Discovery ← file path | 0 URNs anywhere in the repo | discovery is a filesystem convention; a move breaks a reference |
| **Admission ← two owners** | `canonical_agents.json` says *"not in this map is REJECTED"*; `canonical_identity.canonicalize()` **auto-admitted** every unknown id (`save_alias_map`, steps 1 and 4) | any string reaching the resolver became an identity; 34 self-mapped entries in `alias_map.json` |

### D10 — two canonical maps, one of them auto-admits (fixed in this pass)

Call path probed 2026-10-25 (this is the probe that must precede any merge):

```
warga_bootstrap.py:19   from canonical_identity import canonicalize, register_alias
warga_bootstrap.py:20   from warga_manager   import register_agent, list_agents
warga_bootstrap.py:123  canonical = canonicalize(aid, role=..., source=...)   # ← admits
warga_bootstrap.py:156  canonical = canonicalize(aid, role=..., source=...)
warga_manager.py:100    raise ValueError("Unknown agent_id ... Not in canonical_agents.json")
```

The pipeline was **admit-by-default, then check admission**. `canonicalize()` steps 1 and 4 called
`save_alias_map()` with `normalized → normalized`, persisting the id as canonical before
`register_agent()` ever ran. `alias_map.json` still carries **34 self-mapped entries** from that path.

**Fix applied (one resolver, one admission owner):**

- every return in `canonicalize()` now passes through `_admit()`, which consults
  `canonical_agents.json` and raises when the id is absent. No step mints an identity.
- the admission map's spelling wins: `777-FORGE` and `777-forge` both resolve to `777-forge`,
  collapsing the case-duplicate at resolution time (the duplicate **row** stays until F13 retires one).
- `REGISTRY_DIR` derives from `__file__` (env-overridable) instead of hardcoding `/root/AAA/registry`,
  so a checkout no longer silently reads the immutable live tree.

**Test:** known ids and casing normalise (`333-agi` → `333-AGI`, `OPEncode` → `opencode`);
unknown ids raise with the admission file named; `python3 -m py_compile` clean.

**Remaining F13 decision:** 4 resolution ids are absent from admission — `agy`, `hermesarifos-bot`,
`mesa-test-agent`, and the `unknown` sentinel. Admit three, drop the sentinel, or retire the rows.
Ratchet baseline = 4 (INV-AR-12), case-duplicates = 1 (INV-AR-13).

### What is correct as-is

- **MCP servers have no agent principal.** `organs.yaml` gives 41 components an `authority_ceiling` and a
  port, not a signing key. That matches the reference: a tool surface is a *service*, and access is
  authorised through the calling agent's principal. Do not promote a tool surface to a constitutional actor.
- **Verdict does not live on the card.** It lives in the kernel (`arif_judge`) and the vault. A card that
  carried a verdict would be self-certifying.
- **The registry identifier is optional.** AAA can keep card paths as its discovery key. A URN scheme is a
  namespace decision (AAA owns it), not a requirement imported from a vendor.

**Enforcement.** INV-AR-9/10/11 encode L2/L3/L4: an **actor-class** card claiming authority without a
resolvable principal, a runtime reference, or a lifecycle state is counted and ratcheted. INV-AR-12/13
encode D10: resolution ids must be admitted, and no case-duplicate keys may exist. Counts may fall, never rise.

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
| **D1** | Validator's agent + skill SOT is filed as deprecated | `validate-aaa.mjs:59,65` read `federation/_deprecated_20260819/{agents,skills}.yaml`; content is live (`agents: 34`, `skills: 196`, header `total_active: 196`). **Fixed:** `agents.yaml` → `registries/agents.yaml`; `skills.yaml` deleted (strict subset 196 ⊂ 198, one stale bot handle). Validator repointed. | **P0** — one folder rename silently kills validation |
| **D2** | Duplicate agent identities across 3 card roots | **Committed tree: 24 duplicated ids.** Live worktree: 96 card files / 54 unique ids / 28 duplicated (4 extra uncommitted). Runtime de-dupes to 57 cards by INV-005 (`/agent-cards/` wins). `federation-agent-card-ops` skill still states `a2a-server/agent-cards/` is canonical — contradicts runtime | **P1** |
| **D3** | Three skill indexes, no declared precedence | `skills_index.json` 945 · `skills_index.federation.json` 754 unique/810 files · `registries/discovery/skills-index.json` 82 · disk 949 `SKILL.md` | **P1** |
| **D4** | Four tool registries, no join declared | `tool_registry.canonical.json` (ABI, 65 ids) · `tools.yaml` (policy, 269) · `federation_tools_sot.yaml` (per-organ) · `registry/mcp-tools.yaml` (9 organs) | **P2** |
| **D5** | Capability claims unresolvable | **Committed tree: 778 card skill refs — 3 resolve, 171 unresolved, 604 no source.** Live worktree adds 2,512 uncommitted refs (2,227 unresolvable) → 3,290 / 2,398 / 808 / 84. 333-AGI sidecar: 3/20 skills exist | **P0** — capability inflation |
| **D6** | Card schema undeclared / drifting | **Committed tree: 1 card without `schemaVersion`.** Live worktree: 53 of 152. 10 distinct `($schema, schemaVersion)` pairs; one claims `v2.5.0` (no such schema on disk); 6 schema files in `schemas/` | **P2** |
| **D7** | Two port sources of truth, unequal scope | `organs.yaml` 30 ports (41 components) vs `PORT_REGISTRY.json` 9 organs / *"Single source of truth for all network ports"*. 6 shared ids all MATCH; 24 organ ports absent from PORT_REGISTRY | **P1** |
| **D8** | Policy declares paths that do not exist | 5 ghost paths in `CANONICAL_REGISTRY_POLICY.yaml` (`AGENT_INDEX.json`, `skills/AAA_SKILL.md`, `.config/federation-models.json`, `arifOS/arifosmcp/config/model_registry.json`, `LEGACY_...deprecated-2026-07-29`) | **P2** |
| **D9** | **Identity compressed into one object** | 47 unique live cards: **45 claim an authority envelope, 22 have a resolvable principal (18/38 actor-class claims do not), 6 declare a runtime, 11 declare lifecycle, 0 use a discovery URN.** Gateway authorises by name equality (`CANONICAL_ACTORS`, 47 literals) | **P1** — over-claim, not absence |
| **D10** | **Two canonical identity maps with opposite admission semantics** | `canonical_agents.json` (34 canonical, `_meta.rule`: *"not in this map is REJECTED"*) vs `canonical_identity.json` (41 keys, 1 case-dup `777-FORGE`+`777-forge`) + `canonical_identity.py` (*"Single source of truth … every agent_id passes through canonicalize()"*). `canonicalize()` **auto-admitted** unknown ids (`save_alias_map` steps 1 & 4); `alias_map.json` holds 34 self-mapped entries. 4 resolution ids absent from admission (+aliases): `agy`, `hermesarifos-bot`, `mesa-test-agent`, `unknown` | **P0** — admission bypass |
| **D11** | **Three DID stores, one of them untracked** | `secrets/did/registry.json` (14 DIDs / 48 actor names — the **verifier's** store, `federation_envelope.js:620`) is **gitignored** (`.gitignore:19`) and absent from any clone; `auth/did_registry.yaml` (10 DIDs) is the signer's store; `/opt/arifos/secrets/did-registry.json` (11) is a third. `did:arif:aaa` alone covers **22** actors incl. 333-AGI/555-ASI/888-APEX | **P1** — a clean checkout cannot verify any A2A signature |
| **D12** | **Envelope allowlist narrower than server allowlist** | server 47 vs `federation_envelope.js` 15 (+`anonymous`, +`openclaw:ingress`); the narrow list is mounted on 8 `/a2a` routes | **P1** — Trinity actors would be rejected at the middleware |
| **D13** | **Principal granularity: one organ key, many actors** | `did:arif:aaa` → 22 actors; `did:arif:a-forge` → 6; `did:arif:geox` → 5 | **F13 call** — organ-level vs per-lane principals |

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

---

## 9. Verification receipt — 2026-10-25

| Probe | Before | After | Meaning |
|---|---|---|---|
| `npm run validate:registry` | no such gate | **PASS 15/15**, exit 0 | invariants hold at baseline |
| `node scripts/validate-aaa.mjs` | **13 failures** | **10 failures** | −2 false "unknown skill" errors (validator was reading the stale 196-skill copy); +1 real data defect surfaced (`minimax-m-plan` assigned to two packages). Remaining 10 are pre-existing card/identity drift — queued, not introduced. |
| Executable reads of a `_deprecated_` path | 2 (`validate-aaa.mjs:59,65`) | **0** | INV-AR-8 |
| Policy ghost canonical/derived paths | 4 | **0** | INV-AR-7 |
| Skill-policy registries | 2 (196 + 198) | **1** (198) | D3, skill layer |
| Agent-policy registry location | `_deprecated_20260819/agents.yaml` | `registries/agents.yaml` | D1 |

**Remaining work (queued, not fixed here):** 171 unresolvable + 604 source-less card skill refs on the
committed tree; 24 duplicate agent ids; 10 `validate-aaa` identity/card failures; `minimax-m-plan`
double package assignment; **and the D9 identity split — 41 authority claims without a principal,
39 without a runtime ref, 34 without a lifecycle state, 0 discovery identifiers.** Each needs a content
decision (build / delete / re-point / issue key / assign runtime), not a rename.

**DITEMPA BUKAN DIBERI.**

## 10. Third pass — the instrument was wrong before the reading was

Two corrections in one day, both on the same defect class: **a gauge that answers a narrower question
than the claim it is used to support.**

| Claim made | Gate measured | Corrected instrument | Corrected value |
|---|---|---|---|
| "4/47 can prove a principal" | `card.public_key.hex` only | card + `identity.json` + `IDENTITY/keys` + DID | **22/47** |
| "41/45 authority claims unauthenticated" | all cards, card-scoped | actor-class only, multi-store principal | **18/38** |
| "authority outruns authentication 11:1" | ratio of the two above | — | **authority is over-claimed, not absent** |
| "two maps" | not measured | resolution ⊆ admission + case-dup scan | **4 unadmitted · 1 case-dup group** |

The ontology from the review was right; the under-credit was in this document's first measurement, not in
AAA. The live defect is narrower and sharper: **admission had two owners with opposite defaults**, and the
permissive one ran first.

**What this changes about the recommendation.** No new identity system, no third registry. One admission
map (`canonical_agents.json`), one resolver (`canonicalize()`), one derived alias cache. Fields
`discovery_id` / `runtime_ref` / `governed_resource_ref` are **not** to be added until a consumer exists —
they are declared gaps with a ratchet, not a build order.

**DITEMPA BUKAN DIBERI.**

## 11. Fourth pass — reviewer corrections, re-derived

The review that triggered this pass observed head `01576b01`; current head is `c778952b`.
A witness on an older commit is evidence about that commit, not about the branch. Re-derived anyway:

| Reviewer claim | Verdict | Evidence |
|---|---|---|
| "47 was carried, not counted; true count 45" | **REFUTED** | Gate enumerates **170 card files / 169 parsed / 47 unique ids**. 45 is the subset that claims an authority envelope. Both numbers are right; they answer different questions. |
| "Gateway authorises by name, not principal — incomplete" | **CONFIRMED** | `server.js:3011` requires `from_did` + signature (403 `DID_REQUIRED`); `3048` sets `effectiveSourceAgent = didResult.organId`. The name check at 2964 is a pre-filter. My earlier sentence was wrong and is corrected. |
| "Two allowlists: 47 vs 15, the 15 still admits anonymous" | **CONFIRMED, worse** | **34** server-admitted actors missing from the envelope list, including 333-AGI / 555-ASI / 888-APEX. The narrow list is mounted on 8 `/a2a` routes. |
| "14 organ DIDs cover 24/45 cards" | **PARTIAL** | The 14-DID store (`secrets/did/registry.json`) lists **48 actor names** and covers **22** names under `did:arif:aaa` alone (not 21). But that file is **gitignored** and absent from the clone; `auth/did_registry.yaml` has 10 DIDs; the runtime copy has 11. Three stores, not one. |

**New finding that came out of the re-derivation:** the verifier's principal store is untracked. A clean
checkout of AAA has no DID registry at all — `resolveDidPublicKey()` returns null and every A2A call fails
`DID_VERIFY_FAIL`. The federation verifies against a file that the repository does not carry.

**What survives from the review:** the ontology sequence and the "one map, one resolver, one projection"
remedy. **What does not:** the card count, the name-only characterisation, and the DID coverage figure.

**F13 decision, re-framed by this evidence:** principal granularity is not "issue 41 keys". The organ DID
already maps 22 actors to one key. The question is whether the Trinity (propose / verify / judge) may
continue to share `did:arif:aaa`, since three different constitutional functions currently present the
same principal to the gateway.
