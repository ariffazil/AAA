---
id: skill-artifact-redact
name: "Skill Artifact Redact — Secrets Never Land Raw"
description: "Use when output, logs, or receipts may carry secrets. Filters API keys, Bearer/JWT, presigned-URL credentials and tokens to <REDACTED> before any artifact, log, state.db row, receipt, or commit message is written, and forces loops to read credentials from env vars instead of inline text."
version: 1.0.0
owner: HERMES
risk_tier: high
floor_scope: [F1, F2, F11]
autonomy_tier: T1
forged: 2026-10-23
forged_by: HERMES (F13 order, contrast-hardening batch)
tags: [security, redaction, secrets, logging, state-db, receipts, capture-hygiene]
capability_tier: fed-agent-subagent
ecology_state: WARM
trigger_when:
  - about_to_emit_command_output
  - about_to_write_log_or_receipt
  - about_to_persist_to_state_db_or_memory
  - debugging_auth_headers_or_presigned_urls
  - composing_a_skill_example_with_credentials
related_skills: [secret-hygiene, secret-exposure-containment, agent-store-secret-scrub, forge-secret-hygiene, verify-before-report]
---

# Skill Artifact Redact — Secrets Never Land Raw

> **Doctrine:** A secret that entered an artifact is already leaked. Redaction happens
> **before** the write, not in a cleanup pass after someone notices.
> **Script:** `scripts/redact.py` (stdin/file → redacted stdout, `--check` gate, `--in-place`)
> **Canon kin:** `/root/AAA/instructions/data-authority-hierarchy.md` (F12) · F2 TRUTH (no silent edits)

## What this is

Every capture surface an agent touches — tool output pasted into chat, a debug log, a
receipt, a `state.db` message row, a commit body, a skill example — is a permanent
record. One credential in it survives restarts, backups, and every future session that
greps that store. This skill makes redaction a **precondition of the write**, and makes
the credential live in the environment instead of in the text.

## USE WHEN

1. You are about to show, paste, or save command output that could carry headers, URLs, or env dumps.
2. You are writing a receipt, log line, incident report, or `state.db` row from a live probe.
3. You are debugging auth: 401/403, expired signatures, token refresh, presigned URL failures.
4. You are composing a skill, reference doc, or example that shows a real config or `.env` shape.
5. You are capturing a network trace, HAR file, curl `-v` output, or browser devtools copy.

## DO NOT USE WHEN

1. The value is public by design — a public key, a DID, a URL slug, an ARN with no credential, a hash you are publishing as a receipt.
2. You are writing INTO the secret store (vault write, `.env` creation, secret-manager set). Redacting there destroys the credential; write the real value and keep the receipt value-free.
3. A human is entering their own credential into a masked prompt (vault/clarify). Do not intercept, do not echo, do not "helpfully" log the field.
4. The "secret" is a test fixture explicitly fabricated for a test (must be labelled `EXAMPLE_ONLY` in the same line).

## §1. The three laws

1. **Filter at the boundary, once.** One redaction function, applied where text leaves the machine's memory and enters a durable surface. Per-call-site ad-hoc scrubbing is how classes get missed.
2. **Env var, not inline.** Build loops and probes against environment variables (`set -a; source /root/.secrets/vault.env; set +a`), so the credential stays in the environment and never in the command line, shell history, or captured output.
3. **Never print the value, not even the redaction proof.** Report `X-Amz-Security-Token: <REDACTED> (len=1638)` — length and class, never the bytes, never a prefix of the bytes.

## §2. Pattern register (minimum set — extend, never shrink)

| Class | Shape it catches | Notes |
|---|---|---|
| OpenAI/Anthropic-style keys | `sk-[A-Za-z0-9_\-]{16,}` | prefix tells the provider |
| GitHub tokens | `gh[pousr]_[A-Za-z0-9]{20,}`, `github_pat_[A-Za-z0-9_]{20,}` | |
| AWS access key id | `AKIA[0-9A-Z]{16}`, `ASIA[0-9A-Z]{16}` | id alone is not the secret, session token is |
| AWS **session token** | `X-Amz-Security-Token=[^&\s"']+` (base64, no `KEY=VALUE` shape) | **the class that leaked before** — see §6 |
| Presigned URL credential | `X-Amz-Credential=`, `X-Amz-Signature=`, `X-Goog-Signature=`, `sig=` on SAS URLs | |
| Bearer / JWT | `Bearer\s+[A-Za-z0-9._\-]{16,}`, `eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.` | |
| Telegram bot token | `\b\d{8,10}:[A-Za-z0-9_\-]{35}\b` | bot tokens are full authority |
| Generic assigned secret | `(?i)(api[_-]?key|secret|token|password|passwd|pwd)\s*[:=]\s*\S{8,}` | env dumps, config echoes |
| Private keys | `-----BEGIN [A-Z ]*PRIVATE KEY-----` → matching END | redact the whole block |
| Cookies / session ids | `(?i)(set-cookie|cookie|sessionid|sid)\s*:\s*\S{12,}` | |

## §3. Where it must fire (surfaces, not vibes)

- **Chat / human output** — any pasted command output or log excerpt.
- **Receipts** — `/root/AAA/VAULT999`, `state/*.jsonl`, `eurekas/*.jsonl`, incident reports.
- **`state.db` / memory writes** — gateway stores, carry_forward, memory tools.
- **Git** — commit bodies, `.md` artifacts, skill examples, issue/PR text.
- **Artifacts** — PDFs, decks, screenshots taken of terminals (crop or re-run redacted).

## §4. Verification gate

```bash
# gate a candidate artifact before it leaves the machine
python3 scripts/redact.py --check path/to/artifact.txt   # exit 1 = secret found, prints class only

# produce a safe copy for chat / receipt
python3 scripts/redact.py path/to/capture.txt > /tmp/safe.txt
```

A capture is **PRODUCED_SAFE** only when `--check` exits 0 on the final text. "I looked at
it" is not a check: the eye normalises base64 exactly like the old scrubber did.

## §5. Env-var loop pattern

```bash
set -a; source /root/.secrets/vault.env; set +a
curl -sS -H "Authorization: Bearer $TOKEN" "$API/health" | python3 scripts/redact.py
```

Never: `curl -H "Authorization: Bearer sk-live-..."`. Never `echo "$TOKEN"` to verify it
exists — test with `[ -n "${TOKEN:-}" ] && echo "TOKEN present (len=${#TOKEN})"`.

## §6. Known defeat — the X-Amz-Security-Token bypass (2026-10)

A scrubber keyed on `KEY=VALUE` shapes caught `X-Amz-Credential=` and **missed**
`X-Amz-Security-Token=`: the value is a long base64 blob with no `=`-delimited key
pattern the regex expected. A presigned S3 URL pasted into chat therefore carried an AWS
session token into `state.db` in full. Repair was regex + `wal_checkpoint(TRUNCATE)` +
`VACUUM`, and the value was never printed during the repair. Two lessons: a scrubber
must be tested against a **sample of the real leaked string class**, and pattern tables
that only cover `KEY=VALUE` are incomplete by construction.

## §7. Anti-patterns

- ❌ Scrubbing after the write ("I'll clean the log later") — the copy already exists in WAL, backups, and indexes.
- ❌ Replacing with a plausible fake value (`sk-xxxx`) — it reads as real and gets re-used.
- ❌ Redacting the key name too — the class must stay legible for audit.
- ❌ Printing the first 6 chars "for identification" — that is a partial leak.
- ❌ Trusting a single regex; run the whole table, then `--check`.

## §8. Floors

| Floor | Obligation |
|---|---|
| F1 AMANAH | Irreversible leak prevention before the write; no undo story is offered because there is none. |
| F2 TRUTH | The artifact states `<REDACTED>` — an honest marker, not a fabricated value. |
| F11 AUDIT | Class and length stay visible so the receipt remains checkable without the secret. |

## §9. Cross-references

| # | Skill | Role | When |
|---|---|---|---|
| 1 | `skill-artifact-redact` (v1.0.0) | this skill | — |
| 2 | `forge-feedback-loop-ladder` (v1.0.0) | consumer — every captured rung artifact is gated here | during diagnosis |
| 3 | `secret-exposure-containment` · `agent-store-secret-scrub` | remediation when a leak already landed | after a miss |
| 4 | `probe-before-panic` (doctrine) | no "down"/"broken" claim before inventory | before diagnosing |

## §10. Changelog

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-10-23 | Initial forge. Pattern table, env-var law, verification gate, X-Amz-Security-Token defeat record. |
