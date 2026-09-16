---
name: provider-endpoint-migration
category: forge
description: "Use when moving a provider endpoint to another host."
version: 1.0.0
owner: AAA
tags: [ollama, provider, migration, systemd, env, embeddings, federation]
floor_scope: [F1, F2, F4]
autonomy_tier: T1
---

# Provider Endpoint Migration

Moving a provider to another host is easy. **Finding every consumer so nothing fails
silently** is the actual work. This skill exists because that failure happened for real:
demoting a local Ollama silently broke the federation's vector-memory embedder, and only
an independent observer (FRAME probe) caught it.

## Rule 1 — grep the VARIABLE, then grep the DEFAULT

After moving a provider, these are different sets of consumers:

```bash
grep -rn "<old-host>:<port>" /root --include="*.py" --include="*.conf" --include="*.env" \
  | grep -v node_modules
```

Then, critically, find code that **defaults** to the old endpoint — it will not appear in
that grep at all:

```bash
grep -rn "getenv(" /opt/<app>/<pkg> --include="*.py" | grep -i "11434\|localhost"
```

An `os.getenv("X", "http://localhost:11434")` is a **hidden consumer** with no config
footprint. It works until you move the provider, then fails silently.

## Rule 2 — one subsystem, many variables (the four-variable trap)

arifOS resolved the SAME endpoint from three unrelated places, so fixing one looked like a
fix while others stayed broken:

| code path | variable it actually reads |
|---|---|
| health probe | `OLLAMA_HOST` + `OLLAMA_PORT` |
| memory store | `OLLAMA_URL` |
| hib embedder | `ARIFOS_HIB_OLLAMA_URL` → `HIB_*` → `ARIFOS_PRL_*` → **hardcoded localhost** |

The embedder **never read `OLLAMA_URL`**. Setting it changed nothing, while `/health`
flipped to green and hid the problem.

**Never conclude a migration is done because `/health` is green.** Health checks test the
probe path, not the work path.

## Rule 3 — systemd precedence: `EnvironmentFile` beats `Environment=`

Drop-ins setting `Environment=OLLAMA_URL=...` are **silently overridden** when the unit
also declares an `EnvironmentFile` — files are read *after* directives. Symptom: config
looks correct, `systemctl cat` shows your value, and the running process still has the old
one.

**Verify against the live process, never the file:**
```bash
pid=$(systemctl show <svc> -p MainPID --value)
tr '\0' '\n' < /proc/$pid/environ | grep -i <VAR>
```

Fix it at the **source of truth** (the env file), not with a drop-in. Also check whether a
timer regenerates that file (`systemctl list-timers`) — a generated file reverts your edit.

## Rule 4 — retune timeouts; remote is not local

Timeouts tuned for a loopback provider are wrong the moment the provider is remote. A
typical embedder shipped `CONNECT=1s READ=4s` with a circuit breaker (3 fails → 15s open).
A remote node's **cold** model load takes 20s+, so:

```
cold load 20s > read timeout 4s  ->  3 failures  ->  breaker opens  ->  memory lane fails
```

Raise read/connect timeouts for a remote provider, and set a long `KEEP_ALIVE` on the
provider so cold loads are rare. Measure **warm** latency separately from cold — a 4s
reading that is really cold-load is not steady state.

## Rule 5 — prove it with the DEEPEST consumer, not the health endpoint

Order of proof, weakest to strongest:

1. `/health` returns 200 — proves almost nothing about the move
2. provider reachable from the consumer host — proves the network
3. `provider_status` inside the consumer's own health payload — proves the consumer's view
4. **exercising the real work path** (write a record that must be embedded, then recall it) — the only real proof

```bash
# import the consumer's own module in its venv with its env, then call it
cd /opt/<app> && /opt/<app>/venv/bin/python -c "
import os
[os.environ.setdefault(*l.strip().split('=',1)) for l in open('/root/.secrets/<env>.flat.env') if '=' in l and not l.startswith('#')]
from <pkg>.hib import ollama_embedder as oe
print(len(oe.embed_text('probe')))"
```

## Rule 6 — sequence, and keep rollback

```
1. inventory consumers       (Rules 1-2)
2. provider up + parity      (models, digests, reachability)
3. repoint SOURCE env files  (Rule 3)
4. retune timeouts           (Rule 4)
5. restart consumers low-risk first, governance organs last
6. prove with the deepest consumer (Rule 5)
```

- **Never restart a provider while a consumer has in-flight work.** Quiesce → change → verify → resume.
- **Demote, do not delete.** Keep models + unit; rollback is one command.
- If a config is deliberately inert (`.inert-<date>` suffix), **surface it, do not silently
  re-enable** — that was someone's decision, not an accident.

## Pitfalls

- Don't trust a report claiming a change is "staged, not installed" — re-probe it.
- Don't trust "0 drift" from your own audit until you have tested the audit: a 307 counted
  as DOWN, case-sensitive name matching, and "no config" vs "empty config" all produced
  false results in a single session.
- When the machine and your expectation disagree, **the burden of proof is on your
  expectation.**

## Rollback
```bash
cp /root/.secrets/vault.flat.env.bak-<stamp> /root/.secrets/vault.flat.env
systemctl daemon-reload && systemctl restart <consumers>
```
