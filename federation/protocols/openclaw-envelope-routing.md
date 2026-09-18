# OpenClaw Capability Check Routing — RECLASSIFIED

> **CCC-T-05 (2026-09-18)** — probe-before-panic finding, RECLASSIFICATION of GAP-01
> **Supersedes:** "OpenClaw runs but no hook" framing in `AAA_FEDERATION_GAP_REPORT.md` §GAP-01
> **Status:** INFORMATIONAL — informs hook design, not a binding doctrine

## Probe findings (2026-09-18)

`find /root /home -maxdepth 4 -name "*openclaw*"` returned **11 references**:
- `/root/ariffazil/.openclaw` ← actual config dir (NOT `/root/.openclaw/`)
- `/root/AAA/a2a-server/agent-cards/harnesses/openclaw.json` ← A2A agent card (live)
- `/root/AAA/agents/openclaw/agent-card.json` ← AAA repo card
- `/root/arifOS/skills/openclaw-ops` ← skill bundle
- `/root/.kimi-code/skills/openclaw-*` ← 4 skill bundles in kimi harness
- `/root/.hermes/skills/openclaw-propose-seal` ← hermes skill
- `/root/.qwen/projects/-root--openclaw-workspace` ← qwen project memory
- `/root/.hermes/skills/FORGE-spatial-grounding/openclaw` ← forge reference
- `/root/.archive/2026-06-22-forge-cleanup/openclaw` ← archived reference

## Reclassification

GAP-01 in original `AAA_FEDERATION_GAP_REPORT.md` was framed as: **"OpenClaw gateway live, no gate/hook in config, no receipt path"**

This was **representation not reality**. Actual situation:
- OpenClaw is a **federation citizen** registered in `organs.yaml`
- It is a **passenger** in Kimi/Qwen/Hermes harnesses via the 6 skill bundles
- The agent-card exists at both `/root/AAA/a2a-server/agent-cards/harnesses/openclaw.json` and `/root/AAA/agents/openclaw/agent-card.json`
- The `/root/ariffazil/.openclaw/openclaw.json` config is the **canonical** OpenClaw runtime config (different path from what GAP-01 looked at)
- No standalone hook script exists because OpenClaw is **borrowed infrastructure** — its hooks live in the host harnesses (Kimi/Qwen/Hermes), not in OpenClaw itself

Per `representation-reality-invariant.md`: phantom capability and phantom absence are the same defect with sign flipped. GAP-01 was a phantom absence claim — wrong because OpenClaw isn't a missing hook, it's borrowed capability.

## Correct routing (CCC-T-05 action)

OpenClaw capability checks route through:
- **Host harness hook** (Kimi/Qwen/Hermes): if a Kimi session invokes `agy` CLI or uses an OpenClaw skill, the host hook (Kimi `aaa-witness-pre.sh`, Hermes gate, etc.) catches it. Envelope emits through those hooks.
- **A2A agent-card**: discovery-layer-only; no execution authority. Per `AAA_CAPABILITY_REGISTRY.yaml`, OpenClaw's authority ceiling is `OBSERVE_ONLY | DRAFT_ONLY`.

**No new OpenClaw-specific hook needed.** The borrowed-infrastructure model is already constitutional.

## Verdict

GAP-01 closure = update GAP_REPORT.md classification to match reality. No code change. Cross-link this file from GAP_REPORT to prevent future reclassification.

> **DITEMPA BUKAN DIBERI ⚒️**
> **Path:** `/root/AAA/federation/protocols/openclaw-envelope-routing.md`
> **Status:** INFORMATIONAL — probe-before-panic evidence file
