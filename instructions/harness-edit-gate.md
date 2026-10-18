# Harness Edit Gate — Evidence Before Doctrine (S3)

> **Status:** F13_RATIFIED_CHAT (2026-10-18) — sovereign relay of the S1/S3 authorization verdict (`SEAL S3`). Applies to every agent that can edit prompts, skills, guardrails, memory policy, or tool guidance.
> **Failure class killed:** a permanent harness edit adopted on narrative alone, with no matched before/after evidence — the drift that makes two agents disagree about the same rule six weeks later.

## Law

Any edit to a **prompt, skill, guardrail, memory-policy, or tool-guidance** surface MUST declare, before merge:

```yaml
failure_class:    the observed defect this edit removes
observed_evidence: where it was seen (file/probe/receipt id)
proposed_invariant: the rule in one sentence
expected_change:  the behavior that should differ
evaluation_task:  the task used to compare before/after
rollback:         the exact revert path
```

If **matched before/after behavioral evidence is unavailable**, the edit stays `CANDIDATE` and MUST NOT enter the canonical harness. It may live in a scratch file, a branch, or a proposal — not in the loaded surface.

## Mechanical exemption

Typos, broken paths, schema migrations, and config-shape fixes that cannot change behavior are exempt from semantic A/B — but still require a regression check and a rollback line. The exemption is for **mechanical**, not for **behavioral** claims.

## Where this binds

| Surface | Example |
|---|---|
| System prompt / agent def | `/root/.config/opencode/agents/*.md`, `AAA/instructions/*.md` |
| Skills | `/root/.agents/skills/**/SKILL.md` |
| Guardrails | permissions, hooks, policies |
| Memory policy | tier promotion rules, injection rules |
| Tool guidance | `tools_sot.yaml`, MCP descriptions |

## Anti-pattern (what this forbids)

> "I improved the prompt, it feels better." — no task, no comparison, no rollback.
> Two agents then inherit a rule whose author cannot say which failure it prevents.

DITEMPA BUKAN DIBERI ⚒️
