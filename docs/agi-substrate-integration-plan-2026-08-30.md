# AGI Substrate Integration Plan — Night Shift 2026-08-30

> Generated autonomously while F13 sleeps. All changes are additive, non-destructive, git-committed.

## Context

Arif requested all systems move closer to "AGI substrate readiness" while he sleeps. The core deliverable is the **human-meaning-membrane** doctrine (15 substrate invariants + inference protocol) — forged from a 4-hour live analysis session covering somatic anthropology, sexual physics, cross-cultural epistemology, and agentic governance.

This plan maps the doctrine to concrete system components.

## Systems Map

| System | Location | Current State | Target State |
|---|---|---|---|
| **AAA** (governance) | `/root/AAA/` | human-meaning-membrane skill created + committed | Skill indexed, referenced in AGENTS.md, inference schema validated |
| **Hermes Agent** (ASI) | `~/.hermes/` | SOUL.md governs interface; skills loaded on demand | human-meaning-membrane in skill index with proper trigger; inference protocol accessible to Hermes during human interpretation |
| **A-FORGE** (coding) | `/root/A-FORGE/` | Production coding agent | Could implement MCP inference tool as governed module |
| **OpenClaw** (adapter) | OpenClaw config | Coding agent bridge, needs integration | Load human-meaning-membrane for code review tasks; add inference protocol to PR review checklists |
| **MCP servers** | Various ports | Individual organ MCPs | New MCP tool: `human_inference` that implements the inference protocol schema |
| **GitHub repos** | `ariffazil/*` | Multiple repos | human-meaning-membrane referenced in repo docs where human modeling occurs |

## Task Breakdown

### T1: AAA Integration (DONE)
- [x] Skill created: `human-meaning-membrane/SKILL.md`
- [x] Schema written: `references/inference-schema.json`
- [x] Git committed + pushed (`945f36df`)

### T2: Hermes Agent Binding
- [ ] Verify skill loads in Hermes session (check skill index path)
- [ ] Add trigger condition note to SOUL.md or AGENTS.md
- [ ] Ensure inference protocol is referenced in human-interaction sections

### T3: OpenClaw Integration
- [ ] Create `openclaw-human-meaning` skill — teaches OpenClaw to run inference protocol on code review human-context
- [ ] Add inference schema to OpenClaw PR review templates
- [ ] Document OpenClaw role: "coding agent that understands human meaning behind the code"

### T4: MCP Inference Tool
- [ ] Create `human_inference` MCP tool that implements the inference protocol
- [ ] Input: observation + context → Output: structured JSON with 3+ interpretations, unknowns, projection risk, consent status
- [ ] Deploy as part of arifOS organ mesh

### T5: Cross-Repo Documentation
- [ ] Add AGI-substrate section to main README of each relevant repo
- [ ] Reference human-meaning-membrane as governance layer

## Execution Order

1. **T1** — DONE (committed)
2. **T2** — Hermes binding (can be done by main agent, no coding needed)
3. **T3** — OpenClaw integration (spawn coding agent)
4. **T4** — MCP inference tool (spawn coding agent — most complex)
5. **T5** — Documentation (main agent, after code agents finish)

## Risk Assessment

- **Destructive changes**: NONE planned. All changes additive.
- **Production impact**: Skills and docs only. No service restarts.
- **Rollback**: All changes git-versioned. `git revert` if needed.
- **F13 override**: All changes subject to F13 review on wake.

## Success Metrics

When Arif wakes, he should see:
1. human-meaning-membrane skill in AAA (DONE)
2. Hermes loads the skill on relevant triggers
3. OpenClaw has integration note
4. MCP inference tool exists (even as draft)
5. Morning summary with all git commits listed
