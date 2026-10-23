# IDENTITY COLLISION GATE

**Status:** F13_RATIFIED_CHAT (2026-10-23) · **Owner:** ARIF (F13) · **Enforced by:** this file + `state/hermes-actor-family-registry.yaml`
**Origin:** three portraits were conflated in one report — Hermes KVM8, Hermes KVM4 and irfanclaw were quoted as one actor with one inventory. The correction is not "be careful"; it is a gate.

---

## The law

> **The string "Hermes" is not a sufficient identity key.**

Canonical runtime identity is a tuple:

```
(actor_name, host, service, channel, process_or_instance_id)
```

Display name is presentation. **Runtime tuple is identity evidence.**

If two live instances share `actor_name` but differ in host, service or channel:

1. **preserve both** — do not delete one,
2. **do not elect one by recency** — the newest process is not the true one,
3. **do not borrow memory across them**,
4. **do not merge their skill counts**,
5. **do not merge their schedules**,
6. **do not merge their authority**,
7. classify any stale `DORMANT` or `ACTIVE` label as **CONTRADICTED** until the identity owner repairs it.

## Every state claim must carry seven fields

| field | why |
|---|---|
| `actor` | the tuple, not the display name |
| `host` | a number from one machine is not a federation number |
| `endpoint` or `process` | an address or a pid — something that can be probed again |
| `observed_at` | absolute UTC; "recently" is not a timestamp |
| `observer` | who looked. Self-measurement is not attestation |
| `evidence_source` | the command or file, so the claim can be re-derived |
| `classification` | OBSERVED · DERIVED · REPORTED · UNKNOWN |

A federation total may be reported **only after explicit cross-node deduplication**.

## The three failure shapes this gate exists to stop

1. **Name-as-identity.** Two live processes, one label; the report quotes whichever it saw last, and the count silently becomes wrong.
2. **Machine-as-federation.** A number measured on KVM8 is written as "the federation has N" — as if KVM4 and irfanclaw did not exist.
3. **Stored-status-as-current-reality.** A registry field written weeks ago (`DORMANT`) is read as a live observation, while the process it describes is up and serving.

## Self-measurement is not attestation

An agent that probes its own process produces a **self-report with receipts**. That is useful and it is not independent. Raise it only when:

- a **different host** probes it, or
- a **different process tree** (not a child of the same engine) probes it, or
- a **cryptographic witness** signs the observed tuple.

Until then the envelope's `identity_status` is `PARTIAL`, and saying otherwise is the defect this gate names.

## Where the registry lives

`/root/AAA/state/hermes-actor-family-registry.yaml` — `actor_family: Hermes`, one block per instance, `authority_shared: false`, `memory_shared: false`, `family_state: MULTI_INSTANCE`.

## Falsifier

A report that names an actor by display name alone, or quotes an inventory total with no host and no `cross_node_dedup` line, is in breach. So is an agent that marks its own runtime envelope `VERIFIED`.

## Provenance

Written 2026-10-23 by HERMES under F13 correction. The incident is recorded in `state/aureadiness-2026-10-23/` and in the eureka entry *EXPOSE-VS-ENFORCE*.
