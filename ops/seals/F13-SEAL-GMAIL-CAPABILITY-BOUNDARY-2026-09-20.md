# F13 SEAL CERTIFICATE — Gmail Capability Boundary

> **Status:** SEALED (2026-09-20) · F13 directive: *"Seal all"*
> **Scope:** the mail gateway; the MCP ASI upgrade; the enforcement-audit lesson
> **Repos:** A-FORGE `a55e65be` · AAA `a59a0853f` `51d066755` `530f0d658` · HERMES `950807d`
> **Motto:** DITEMPA BUKAN DIBERI ⚒️

---

## What was sealed

| Layer | Artifact | Repo · commit |
|---|---|---|
| Code | `bridges/mailgw_broker.py`, `mailgw_client.py`, `mailgw_grant.py`, `gws_shim`, `mail_gateway.py` | A-FORGE `a55e65be` |
| Container | `mailgw-broker.service`, `mailgw.tmpfiles.conf`, `arifos-gws-chokepoint` (AppArmor) | A-FORGE `a55e65be` |
| Proof | `gws_truth_test.py` (12 vectors + meta self-test), `test_attribution.py` | A-FORGE `a55e65be` |
| Post-mortem | `deprecated/README.md`, `evidence/repro-confine-denies-root.sh` | A-FORGE `a55e65be` |
| Doctrine | `canon/FEDERATION_GMAIL_GATEWAY_SPEC.md` | AAA `a59a0853f` |
| Agent surface | `canon/MAIL-GATEWAY-AGENT-QUICKREF.md` | AAA `a59a0853f` |
| Skill | `skills/google-workspace-gws/SKILL.md`, `skills/governance/chokepoint-enforcement-audit/` | AAA `a59a0853f` |
| Eureka | `eurekas/eureka-entries.jsonl` row 16 (LIVE FEED) | AAA `51d066755` |
| Registry | `AGENTS.md` fragment table, 2 rows | AAA `530f0d658` |
| MCP | hermes-rasa +4 tools; hermes-mcp +3 tools +3 prompts | HERMES `950807d` |

## Verified state

```
boundary suite   : ENFORCED_WITH_ROOT_RESIDUAL (11/12) · open defects: NONE
attribution      : 8/8 agents named (hermes-agent, opencode, qwen-code,
                   kimi-code, claude-code, codex, openclaw, cron)
eureka feed      : 16 rows, all valid JSON
multi-agent read : root, arifos, forge, aaa — all confirmed reading
boot persistence : broker + apparmor enabled; tmpfiles + profiles in place
```

## The three-state transition (not collapsed to a Boolean)

```
ATTEMPTED  → a shell guard, never on any resolution path, privilege = an env var
             reported 7/7 PASS while 0/8 vectors were blocked

BOUND-TOOL → AppArmor deny on the CLI, but the broker still ran as root and the
             store still sat under /root — the tool was bound, the credential was not

ENFORCED   → capability moved to uid mail-gateway; store 0700; socket-mediated;
             every call receipted; ENFORCED_WITH_ROOT_RESIDUAL (11/12)
```

## Corrections carried (do not re-import)

**Correction 1 — "no LSM mechanism denies root on the same kernel."**
FALSE. Falsified by a sibling audit and reproduced here. Same uid (0), same file,
same kernel: unconfined process → `READABLE`; confined by an AppArmor deny rule →
`DENIED`. Repro: `bridges/evidence/repro-confine-denies-root.sh`. AppArmor binds
root. The residual is that the **caller processes are unconfined**, not that root
is ungovernable. Remedy: confine the callers.

**Correction 2 — the first "chokepoint" was reported as GOVERNED & VERIFIED.**
It was a convention gate. An environment variable is a claim, not a capability.
Downgraded to `CANDIDATE → HOLD` before the rebuild.

**Correction 3 — "the guard denies Gmail."**
It denied *when invoked*. Nothing required invocation. A test that routes through
the gate cannot detect a missing gate.

## Not sealed / open debt

| Item | Class |
|---|---|
| Root can read the store while unconfined (V6) | Needs caller confinement (applies to every warga process) |
| Two entry points reach the same broker (`gws` shim + `mailread`) | Fragmentation; fold one into the other |
| `purpose` is a length check, not a scoped lease | Bind `actor × intent × scope × lease × expiry` |
| `mail_gateway.py` keeps its own policy layer beside the broker's | Consolidation |
| 53 unmerged commits on `proposals/orthogonality-v02-hermes-mapping` | Sibling's branch; not mine to push |

## Scope note

"Seal all" was applied to **the layers of the rules in play** — the mail boundary
and the two MCP surfaces built from the same session's lesson. It was **not** a
wholesale adoption of every dirty file in the repos: sibling agents' in-flight
work (`F13-SEAL-CERTIFICATE`, `GAP-AUDIT`, `MASTER-COMPRESSION`, the Rose-APEX
canon, unrelated skill edits) was left untouched and is reported here rather than
swept into these commits.

---

*Every claim above is backed by a runnable artifact. Where a claim could not be
verified, it is recorded as open debt instead of asserted.*

**DITEMPA BUKAN DIBERI** ⚒️
