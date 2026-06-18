# Session: 2026-06-07 09:53–10:01 UTC — T3 Forge Spec: MCP-UI-DECLARATIVE-FIRST-v1

## Context

Arif dropped a YouTube link in direct Telegram (msg #39103, 09:47:29 UTC):
https://youtu.be/hCMrEfPG2Yg — *"Beyond Components: Designing Generative UI for MCP Apps"* by Ruben Casas (Postman), AI Engineer Summit 2026-06-03, 17 min.

OPENCLAW identified the talk's relevance to the AAA cockpit question (federation-wide UI tiering), offered 4 options (T1 transcript / T2 skim / T3 forge spec / T4 bookmark).

Arif chose T3 (msg #39106, 09:51:32 UTC), then delivered the full T3 spec as a single burst of messages (#39106, #39107, #39108) — the canonical sections 1-8 of the forge spec.

OPENCLAW compiled, added value (F2 risks, consolidation, metadata, 5 forge-task descriptions), and wrote to `forge_work/`.

## Files written

- `/root/.openclaw/workspace/forge_work/MCP-UI-DECLARATIVE-FIRST-v1.md` — **20,044 bytes, 500 lines, 11 sections** (final consolidated version)
- `/root/.openclaw/workspace/memory/2026-06-07-0956-mcp-ui-declarative-first.md` (this file)
- `/root/.openclaw/workspace/HEARTBEAT.md` — new history entry on top

## Spec structure (11 sections)

1. **TL;DR / Verdict** — Declarative-first, not Generative-first. Real endpoint: governed shared cockpit, not "chat with dashboards."
2. **The 3 tiers** (Static / Declarative / Generative) — pattern from Casas talk.
3. **Per-organ mapping** — arifOS (Static+Declarative), GEOX (Declarative-first + Generative sandbox), WEALTH (Declarative for decisions + Generated for explanation), WELL (Static+Declarative, hard wall on dignity).
4. **AAA L7 architecture** — 3 lanes (L7-S / L7-D / L7-G), flow diagram, kill switch.
5. **Canonical envelope upgrade** — `_meta.ui.resourceUri` + descriptor + allowed/forbidden actions + `requires_888_hold`.
6. **Renderer contract** — `aaa.ui.descriptor.v1` schema with `action_policy: {inspect: allowed, simulate: allowed, draft: allowed, mutate: hold_required, seal: arifOS_only}`.
7. **Trust boundary** — double-iframe mapped to arifOS: outer (AAA cockpit, owns identity/session/action/9-signal), middle (MCP app host, renders approved UI), inner (generated/sandbox, no authority).
8. **5 forge tasks** — Forge 1 (descriptor schema), Forge 2 (`_meta.ui.resourceUri` per tool), Forge 3 (4 renderer packs), Forge 4 (sandbox lane), Forge 5 (visual governance tags).
9. **Build order (7 steps)** — 1. Static shell + 2. Descriptor schema + 3-5. Renderer packs + 6. Generative sandbox + 7. Collaborative canvas (future).
10. **F2-honest risks (10 items)** — R1–R10 with severity + mitigation.
11. **References** — 6 sources (talk + BigGo recap, MCP-UI GitHub, 3 GEOX precedents, Constitution Chapter 6).
12. **Carry-forward** — sovereign review, re-verify WEALTH+WELL, schedule Forge 1 if GREEN-SEAL.

## What I added beyond Arif's draft

- **Section 9 (F2 risks)** — 10 items, not in Arif's original. R2 (sandbox escape), R3 (F6 maruah manipulation), R6 (GEOX generative mis-citation watermark), R7 (WELL consent bypass in Telegram), R9 (organ-health dependency), R10 (step-7 scope creep) are non-obvious.
- **F2 runtime caveats** on WEALTH + WELL — flagged in §2.3 and §2.4 that their health was not fresh-verified; mapping is design-contract.
- **Metadata header** — proper forge_work/ header with authoring actor, lane, stage, decision class, precedent, source.
- **5 forge-task descriptions** — expanded each forge into a scoped, reversible unit (Forges 1-5 in §7).
- **Carry-forward section** — explicit checklist for sovereign review.
- **Real references** — [1] = Casas talk + BigGo recap, [2] = MCP-UI GitHub (URLs verified, no placeholders).
- **UI Law #0 carry-forward** at the end, in spirit of GEOX-UI-READINESS.

## What I preserved from Arif's draft

- The 3-lane model (L7-S / L7-D / L7-G).
- Per-organ `forbidden` lists.
- The verdict: Declarative-first, not Generative-first.
- The "boring where decisions matter" principle.
- The double-iframe trust boundary (outer/middle/inner) — kept verbatim.
- The 5 forge tasks — kept verbatim.
- The 7-step build order — kept verbatim.
- The action_policy safety surface (`inspect/simulate/draft/mutate/seal`) — kept verbatim.

## Constitutional posture

- **No irreversible action.** This is a forge proposal (HOLD), not a doctrine seal.
- **UI Law #0** (from GEOX-UI-READINESS.md) preserved as a hard invariant.
- **F6 Maruah** built into the kernel-side check, not the renderer.
- **Reversibility** explicit in every forge step.
- **No live code touched.** No `_meta.ui` schema change in the live envelope.
- **No VAULT999 seal.**

## What I did NOT do (deferred for sovereign review)

- Edit any live MCP or AAA code.
- Add `_meta.ui` to the live FederationEnvelope schema.
- Seal to VAULT999.
- Invoke any forge tools that would mutate state.
- Watch the 17-min Casas talk in full.

## Carry-forward to next session

- [ ] Sovereign review of the spec.
- [ ] **R0.1 WEALTH recovery** — diagnose why `wealth_system_registry_status` fails. Read service logs, inspect connector at :18082, check Pydantic schema vs live return.
- [ ] **R0.2 WELL identity restoration** — identify 4 missing tools (registered=13, canonical=17), re-register, verify identity invariant returns valid=true.
- [ ] **R0.3 Vault write-path check** — synthetic SEAL probe to confirm write path still works.
- [ ] If R0 fails on any organ: HOLD entire spec, do not start Forge 1.
- [ ] If GREEN-SEAL: schedule Forge 1 (descriptor schema) as next AGI task.
- [ ] If REJECT: log lesson, close forge.
- [ ] Reference in any future AAA cockpit work.

## Update: 10:07Z — Pre-flight gate added

Sovereign correction (msg #39111, 09:54:05Z): "arifOS GUI is not production-ready yet. MCP federation is partially ready, not fully healthy." Per-organ truth: arifOS ready as governed kernel; GEOX healthy; WELL degraded (identity invariant failed, possible corruption); WEALTH not verified healthy (registry/health call fails); AAA/GUI not ready.

Live diagnostic at 10:05:07Z confirms. Three concrete findings:
1. **WEALTH**: `wealth_system_registry_status(mode='health')` returns MCP error -32600 (output schema vs structured content mismatch). Service alive; tool broken.
2. **WELL**: `well_assess_reliability(mode='health')` returns `identity_valid: false`, `authority_boundary: compromised`, `registered=13 / canonical=17`, `state_age_hours: 6.41`, `delta_s: -1`. Verdict reason: *"Organ may be corrupted or impersonated."* This is an F11 floor flag.
3. **Vault**: last SEAL 53.4h ago.

Spec updated to add §0 Pre-flight Gate + Forge 0 (R0.1/R0.2/R0.3, operational, not a forge-task). Promotion criteria to §7: WEALTH registry returns PASS; WELL identity_valid=true + authority_boundary=intact + registered==canonical; vault freshness<24h.

R9 risk in §9 was "if WEALTH or WELL is unhealthy at forge time, the mapping breaks" — it has now become a present condition. R9 promoted from risk to gate.

## F1 confession / F2 truth / F7 humility

- The Casas talk is ~17 min. I have NOT watched it in full. I have the title, description, timestamps, the Japanese recap (BigGo), and the existing GEOX-UI-READINESS.md precedent.
- The runtime caveats on WEALTH + WELL are real. The mapping for those two is design-contract, not runtime-verified.
- The 5 forge tasks (Arif-authored) assume the current organ health; R9 in §9 surfaces this.

## Reversal test

`rm /root/.openclaw/workspace/forge_work/MCP-UI-DECLARATIVE-FIRST-v1.md && rm /root/.openclaw/workspace/memory/2026-06-07-0956-mcp-ui-declarative-first.md` — full reversal, no live state touched.
