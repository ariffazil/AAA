# A2A Canonical Surface — AAA Federation

> **Status:** OBSERVE RECEIPT · 2026-09-13 · session `SEAL-7ee1801260d74b43`
> **Not a kernel SEAL.** `seal_allowed=false`. Public interoperability is **not** claimed.
> **Supersedes the “all 7 gaps closed” line** in `A2A_ALIGNMENT_SPEC.md` (epoch 2026-07-17).
> **DITEMPA BUKAN DIBERI**

## 1. Official protocol truth (OBS)

| Item | Value | Source |
|---|---|---|
| Latest **spec** on `a2a-protocol.org/latest` | **1.0.0** | [Specification](https://a2a-protocol.org/latest/specification/) |
| Latest **GitHub release tag** | **v1.0.1** (2026-05-26) | [a2aproject/A2A releases](https://github.com/a2aproject/A2A/releases/tag/v1.0.1) |
| Production-ready announcement | v1.0, 2026-03-12 | [Announcing 1.0](https://a2a-protocol.org/latest/announcing-1.0/) |
| Governance | Linux Foundation → **AAIF Growth Stage** (2026-08-27) | [AAIF join](https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/) |
| Normative source | `spec/a2a.proto` | Spec §1.4 |
| Bindings | JSON-RPC 2.0, gRPC, HTTP+JSON/REST | Spec §1.3 / §9–11 |
| Companion protocol | **MCP = vertical tools**; **A2A = horizontal agents** | [A2A and MCP](https://a2a-protocol.org/latest/topics/a2a-and-mcp/) |

Do **not** advertise `protocolVersion: "1.2"` as an upstream A2A version. That string is a federation-private leak. Upstream A2A is 1.0 / 1.0.1.

v1.0.1 bugfixes (OBS, release notes): prefer `application/a2a+json` in HTTP binding; transcoding errors; TaskStatus values in the spec.

## 2. Two different “A2A”s (do not mix)

| Name | What it is | Where |
|---|---|---|
| **A2A protocol** | Linux Foundation Agent2Agent | JSON-RPC / Agent Card / tasks |
| **A2A room** | Agent-to-agent Telegram compartment | AAA group `-1003753855708` |

A2H / A2A / A2M rooms are **social compartments** (`instructions/agent-compartment.md`). They are not the protocol.

## 3. Federation placement (APEX stack)

Intelligence is a stack. A2A is the **horizontal envelope**, not the mind.

```
L3 CIVILIZATION (ASI)     Hermes + AAA control plane
        │ A2A: delegate accountable work between agents
L2 GOVERNED EXECUTION     arifOS judges · A-FORGE actuates via MCP/ACT
        │ MCP: invoke bounded tools
L1 SUBSTRATE              GEOX · WEALTH · WELL  (evidence, not authority)
```

| Construct | Protocol role | Must not become |
|---|---|---|
| **arifOS** | Constitutional kernel (F1–F13, `arif_judge`, VAULT999) | Public A2A “mind” |
| **AAA** | Canonical A2A **federation edge** + discovery | Judge or actuator |
| **Hermes** | Principal orchestrator agent | Raw unrestricted authority |
| **GEOX / WEALTH / WELL** | Specialist agents (evidence / advisory / reflect) | Transaction or field control |
| **arifFlow** | Workflow / Reality Graph binding | Transport protocol |
| **FED** | Trust / capability / health intelligence | Authorization |
| **FRAME** | Anomaly / contrast observer (`:18085`) | Verdict |
| **A-FORGE** | MCP/ACT bounded actuator | Public autonomous A2A peer (default) |
| **VAULT999** | Receipt ledger | Agent Card skill |

Official complementarity: A2A delegates work to another agent; MCP invokes a tool; ACT changes the world. A2A completion ≠ effect authorization.

## 4. Live surface (OBS 2026-09-13T06:15Z)

| Probe | Result |
|---|---|
| `GET https://aaa.arif-fazil.com/.well-known/agent-card.json` | 200 JSON, 14839 bytes, disk via Caddy `file_server` |
| `GET http://127.0.0.1:3001/.well-known/agent-card.json` | 200 JSON, **9817 bytes** — **not the same card** |
| Card `supportedInterfaces[0].url` | `https://aaa.arif-fazil.com/a2a` (no trailing slash) |
| `POST https://aaa.arif-fazil.com/a2a` + `A2A-Version: 1.0` | **405** — Caddy `handle /a2a/*` does **not** match exact `/a2a`; SPA wins |
| `POST https://aaa.arif-fazil.com/a2a/` + `A2A-Version: 1.0` | **200** JSON-RPC (`tasks/list` → `{tasks:[], total:0}`) |
| `POST http://127.0.0.1:3001/a2a` without `A2A-Version` | 400 `A2A-Version header is required. Set A2A-Version: 1.0` |
| `message/send` (loopback) | 403 `EMD_VALIDATION_BLOCKED` (W3=0.1 < 0.3) |
| `agent/getAuthenticatedExtendedCard` | 400 method-not-found. Advertised available: `agent/getCard`, `agent/listSkills`, `tasks/send`, `tasks/get`, `tasks/cancel`, `tasks/list` |
| Organ public cards | arifOS **stub** `{"id","name"}`; GEOX **404**; WEALTH **HTML**; WELL **HTML**; `a-forge` **404**; `forge` **404** |
| `now --json` | arifOS/FORGE/GEOX/WEALTH/FLOW/FRAME/FED **UP**; WELL **DEGRADED**; FED `:4000/health` **timeout** (liveliness `"I'm alive!"`) |
| AAA gateway health `:3001/health` | healthy, `deployed_commit=ccb0f48`, `authority_ceiling=DISPLAY_ONLY`, protocol A2A `v2026.07.24` |

Caddy (`Caddyfile.live` `aaa.arif-fazil.com`):

- `handle /a2a/*` → `127.0.0.1:3001` (JSON-RPC)
- exact `/a2a` falls through to SPA root `/var/www/html/aaa`
- `/.well-known/agent-card.json` served **from disk**, not from `:3001`

**Caddy matcher / reload = T3 888_HOLD.** Do not “fix live” from this session.

## 5. Wire mapping (keep official states)

Official TaskState (spec §4.1.3): `UNSPECIFIED`, `SUBMITTED`, `WORKING`, `COMPLETED`, `FAILED`, `CANCELED`, `REJECTED`, `INPUT_REQUIRED`, **`AUTH_REQUIRED`**.

| arifOS verdict | A2A wire | Note |
|---|---|---|
| SEAL | `TASK_STATE_COMPLETED` | Artifact + receipt. Completion ≠ world-effect. |
| SABAR | `TASK_STATE_INPUT_REQUIRED` | Missing evidence / clarification |
| HOLD / 888_HOLD | **`TASK_STATE_AUTH_REQUIRED`** | Sovereign / credential gap |
| VOID (policy deny) | `TASK_STATE_REJECTED` | Do not collapse into FAILED |
| VOID (crash) | `TASK_STATE_FAILED` | Non-sensitive diagnostic only |
| abort | `TASK_STATE_CANCELED` | |

**Shadow in code:** `src/gateway/schema.ts` and `schema-v1.ts` omit `TASK_STATE_AUTH_REQUIRED`. `schema-v1.ts` maps legacy `auth-required` → `INPUT_REQUIRED`. `a2a-server/ALIGNMENT_MD.md` maps HOLD → `INPUT_REQUIRED`. That hides F13 from the wire.

## 6. Official JSON-RPC verbs vs live dispatcher

Official (spec operations → JSON-RPC): `message/send`, `message/stream`, `tasks/get`, `tasks/list`, `tasks/cancel`, `tasks/resubscribe`, `tasks/pushNotificationConfig/{set,get,list,delete}`, `agent/getAuthenticatedExtendedCard`.

Live `:3001` still answers a **legacy set** (`tasks/send`, `agent/getCard`, `agent/listSkills`) while a second path accepts `message/send` (then EMD-blocks). Dual dispatcher = dual truth.

`tasks/list` result shape `{tasks, total}` is **not** `{tasks, nextPageToken, pageSize, totalSize}`. Extra `_membrane` on every JSON-RPC body is a private extension; it must be negotiated via `A2A-Extensions`, not injected into the core envelope.

## 7. Public vs extended card (APEX-ZEN)

Public card **must** stay small: identity, HTTPS interface, protocolVersion **1.0**, streaming/push/extended flags, MIME modes, security **schemes + `security` (not `securityRequirements`)**, JWS `signatures` (`protected` + `signature`), minimal public skills.

Public card **must not** publish: internal ports (`8088`, `7071`), sovereign key fingerprint, nonce flow, organ skill maps, Telegram IDs, cron topology, Reality Graph contents, Merkle material.

Use `capabilities.extendedAgentCard` + authenticated `agent/getAuthenticatedExtendedCard` for tenant skills and federation routing. That is already the official pattern.

Live public card (OBS): `protocolVersion: "1.2"` at root; `securityRequirements` (non-normative name); `Ed25519Signature2020` instead of JWS; `authenticated_extended_card` **and** `extendedAgentCard`; extensions dump kernel ports, organ map, key fingerprint. **Signed-card key rotation remains 888_HOLD.**

## 8. APEX-ZEN application (real dials, not a slogan)

APEX T000:

`G = (A · P · E · X)^(1/4)` with **A=AKAL, P=PRESENT AUTHORITY, E=ENTROPY×ENERGY, X=EXPLORATION×AMANAH**.

FRAME: `G` is a **coordinate in a declared frame**, not authorization. Anomaly-first: contrast the advertised Agent Card against live verbs, card bytes, and organ discovery.

A-Z breath: inhale = `arif_judge` stop; exhale = witness/release. Do not treat “gateway healthy” as a SEAL of interoperability.

| Dial | This probe |
|---|---|
| A AKAL | Live falsifiers exist (405 on advertised URL; verb drift; dual cards). Truth before “aligned.” |
| P AUTHORITY | AAA ceiling DISPLAY_ONLY. arifOS judges. A-FORGE executes. F13 seals. `seal_allowed=false` here. |
| E ENTROPY | Dual card (disk 14839 vs runtime 9817); `protocolVersion` 1.2 vs 1.0; legacy verbs; `_membrane` leak. |
| X AMANAH | WELL degraded. Do not widen public mesh. Money / deploy / Caddy reload / key material stay HOLD. |

## 9. FRAME + Reality Graph + FED

A2A says a task moved. It does not say the artifact is true.

```
Principal → A2A Task → Agent/Organ → MCP Tool
                ↓
            Artifact → Claim ⇄ Evidence ← FRAME contrast
                ↓
            APEX receipt → policy version / F1–F13
```

Reality Graph (`canon/REALITY_GRAPH.md`): **name SEALED**; cryptographically ordered belief revision **CLAIMED**; L2 graph **HOLD**. Do not advertise it as a live A2A skill until lineage reconstruction has a receipt.

FRAME `:18085` health `ok` (OBS). FED liveliness up; `/health` timeout (OBS). FRAME output is evidence, never a verdict.

## 10. Holds (remain locked)

1. **Caddy reload** to make exact `/a2a` proxy — T3.
2. **Merkle / signing-key rotation** to JWS Agent Cards — F13.
3. **WELL telemetry** on public/extended cards.
4. **93 held loops** — health ≠ release.
5. **Money, deploy, destructive ops, external publish** — A2A `COMPLETED` is not ACT.

## 11. Smallest next seals (after HOLD review)

1. Point the **advertised** interface URL at a path that actually JSON-RPCs (`/a2a/` **or** Caddy exact-match — latter is T3).
2. One card generator; stop serving a different disk card than `:3001`.
3. Strike `protocolVersion: "1.2"` from deployable cards. Pin `1.0` on interfaces.
4. Restore `TASK_STATE_AUTH_REQUIRED` on the wire. Stop mapping HOLD → INPUT_REQUIRED.
5. Official verb table only on the public dispatcher; wrap `_membrane` as an optional extension.
6. Organ public cards: stub/404/HTML are FRAME anomalies. Either publish honest public cards or stop listing `card_url`s.

Option **B** remains the architecture: one canonical AAA A2A edge, internal organ agents, MCP-bound tools, A-FORGE as guarded actuator. Option C (every organ a public A2A server) is forbidden until B is proven against upstream v1 schema **and** live verbs.
