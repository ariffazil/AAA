# AAA P2P Inner-Loop Protocol (v1.0)

> **Authority:** 888-APEX · **Status:** LIVE · **Ratified:** 2026-07-15
> **Layer:** Phase 3a — between A2A (external/federation) and MCP (organ tools)

DITEMPA BUKAN DIBERI. Forged, not given.

---

## 1. Purpose

The AAA inner loop — 333-AGI ⇄ 555-ASI ⇄ 888-APEX — requires a low-latency
transport for co-located agents on the same VPS. A2A (HTTP) is too heavy for
per-turn reasoning; MCP (organ tools) is for execution, not deliberation.
**P2P is the third rail**: a Unix domain socket mesh that lets the three
primary agents talk to each other in microseconds, with F11 audit baked in.

| Transport | Layer | Latency target | Use |
|-----------|-------|----------------|-----|
| **P2P** (Unix socket) | Inner loop | ≤10ms (888), ≤50ms (555) | propose / translate / judge cycle |
| A2A (HTTP) | Federation | ≤500ms | cross-warga discovery + delegation |
| MCP (stdio/HTTP) | Organs | ≤200ms | tool execution in arifOS / GEOX / WEALTH / WELL |

## 2. Topology

```
              ┌──────────┐
   propose    │ 333-AGI  │  judge / HOLD / VOID / SEAL
   ─────────▶ │ (THINK)  │ ◀─────────────────────────┐
              └────┬─────┘                           │
                   │ translate                       │
                   ▼                                 │
              ┌──────────┐                           │
              │ 555-ASI  │──── ethical flags ────────┤
              │ (HEART)  │                           │
              └──────────┘                           │
                                                   │
              ┌──────────┐                           │
              │ 888-APEX │───────────────────────────┘
              │ (JUDGE)  │
              └──────────┘
```

Three listening sockets (one per agent) plus a broadcast socket for fan-out.
The `audit.jsonl` ledger is shared and hash-chained.

| Socket path | Owner | Listens for |
|-------------|-------|-------------|
| `/tmp/aaa-p2p/333-to-888.sock` | 333-AGI | outbound to 888 |
| `/tmp/aaa-p2p/555-to-333.sock` | 555-ASI | outbound to 333 |
| `/tmp/aaa-p2p/888-to-all.sock` | 888-APEX | outbound to 333 + 555 |
| `/tmp/aaa-p2p/audit.sock` | (broadcast) | every message, all agents |

## 3. Message Schema

Every message is a single JSON object terminated by `\n`.

```json
{
  "from": "333-AGI",
  "to": "888-APEX",
  "verb": "propose",
  "payload": { "...": "verb-specific" },
  "timestamp": "2026-07-15T04:30:00.123456+00:00",
  "requires_judgment": false,
  "session_id": "SEAL-...",
  "blast_radius": "LOW",
  "signature": null
}
```

### 3.1 Field constraints

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `from` | string | yes | one of `333-AGI`, `555-ASI`, `888-APEX` |
| `to` | string | yes | one of the same, or literal `"all"` for broadcast |
| `verb` | string | yes | `propose` \| `translate` \| `judge` \| `ack` \| `reject` |
| `payload` | object | yes | verb-specific body; no required keys for `ack`/`reject` |
| `timestamp` | string | yes | ISO-8601 with microseconds + timezone |
| `requires_judgment` | bool | yes | 333→888 must set `true` for IRREVERSIBLE proposals |
| `session_id` | string | no | kernel-born session id, opaque |
| `blast_radius` | string | yes | `LOW` \| `MEDIUM` \| `HIGH` \| `IRREVERSIBLE` |
| `signature` | string | no | hex-Ed25519 over canonical JSON; **required for `IRREVERSIBLE`** |

F12 INJECTION: every field is validated against this schema before the
message is forwarded. Rejected messages get a `reject` ack and never reach
the recipient.

### 3.2 Verbs

| Verb | Sender → Receiver | Meaning | Typical payload |
|------|-------------------|---------|------------------|
| `propose` | 333 → 888 | Candidate action for judgment | `{ "candidate": str, "rationale": str, "evidence_refs": [..] }` |
| `translate` | 555 → 333 | Clarification / rephrase | `{ "original": str, "rephrased": str, "concerns": [str] }` |
| `judge` | 888 → all | HOLD / VOID / SEAL verdict | `{ "verdict": "SEAL"|"HOLD"|"VOID", "reason": str, "f1_f13_pass": [bool] }` |
| `ack` | any → sender | Receipt confirmation | `{ "ref_timestamp": str, "received_at": str }` |
| `reject` | any → sender | Rejection with reason | `{ "ref_timestamp": str, "reason": str, "code": str }` |

`propose` messages **must** set `blast_radius` honestly. Misclassifying an
IRREVERSIBLE action as LOW is an F2 (TRUTH) and F1 (AMANAH) violation.

## 4. Latency Targets

Measured end-to-end on the same VPS, no other P2P traffic:

| Path | Target | Hard ceiling |
|------|--------|--------------|
| 333 → 888 roundtrip | ≤10ms | 50ms |
| 333 → 555 → 888 chain | ≤50ms | 200ms |
| 888 broadcast → all ack | ≤20ms | 100ms |

Unix domain sockets avoid the TCP loopback path; `SOCK_STREAM` framing gives
us one message per connection, which makes back-pressure and ack semantics
trivial.

## 5. F11 Audit (append-only hash chain)

Every message — accepted, rejected, or routed — is appended to
`/root/AAA/p2p/audit.jsonl` **before** it is delivered. Each line is:

```json
{
  "seq": 17,
  "ts": "2026-07-15T04:30:00.123456+00:00",
  "from": "333-AGI",
  "to": "888-APEX",
  "verb": "propose",
  "blast_radius": "LOW",
  "session_id": "SEAL-...",
  "prev_hash": "sha256:...",
  "hash": "sha256:...",
  "message": { ...the original message... }
}
```

`hash = sha256(prev_hash + canonical_json(message))`. Tampering with any
line breaks the chain from that point forward — `verify_chain()` will
return `False`.

The audit file is **append-only**: there is no public write API that
overwrites prior lines. The auditor (888-APEX.apex_audit_embed) periodically
seals a Merkle root to VAULT999.

## 6. Lifecycle

1. **Boot**: `python -m AAA.p2p.run_p2p start 333` (or 555 / 888) spawns an
   asyncio server bound to `/tmp/aaa-p2p/<agent>.sock`.
2. **Steady**: agents read inbound messages from their socket, validate the
   schema, append to `audit.jsonl`, then forward to the recipient's socket.
3. **Shutdown**: SIGINT triggers a graceful drain — finish pending writes,
   close the socket file, exit 0.

## 7. Failure modes

| Failure | Behaviour |
|---------|-----------|
| Recipient socket missing | sender retries once with backoff, then `reject` ack to caller |
| Schema invalid | sender receives `reject` with `code: "F12_SCHEMA"`, message NOT forwarded, audit row written |
| Audit write fails (disk full, perms) | message is NOT delivered; sender receives `reject` with `code: "F11_AUDIT_BLOCKED"` |
| Signature missing on `IRREVERSIBLE` | sender receives `reject` with `code: "F1_ED25519_REQUIRED"` |

## 8. Compatibility

- **Python:** 3.12+ (uses `asyncio.StreamReader.readexactly`, PEP 695 generics not required)
- **OS:** Linux (Unix domain sockets); macOS works for dev; Windows not supported (would need named pipes)
- **Dependencies:** stdlib only (`asyncio`, `socket`, `json`, `hashlib`, `pathlib`, `dataclasses`)

## 9. Pointer

Implementation:
- `socket_server.py` — asyncio Unix-socket server
- `socket_client.py` — asyncio client for outbound messages
- `audit.py` — append-only hash-chained audit log
- `run_p2p.py` — CLI entry point
- `tests/test_p2p_loop.py` — 333 ⇄ 555 ⇄ 888 integration test
- `tests/test_audit.py` — hash-chain verification + tamper detection