# RECEIPT — Lane-A seal patch: NOT EXECUTED (Option 1 verify-first)

> **Lane:** RECEIPT (Lane B) — procedural record, NOT a constitutional SEAL.
> **Actor:** hermes-prime (session SEAL-8a5912bd383749b2, OBSERVE_ONLY)
> **Forged:** 2026-09-13 09:0x MYT, KVM8/forge
> **Sovereign directive received:** "Ok can you execute this for me" (A+B+C)
> **Decision:** NOT EXECUTED. Verification (read-only) shows A/B/C would corrupt
> the audit record. F2 TRUTH outranks task completion.
> **Reversibility of this receipt:** YES (file write only). Zero mutation elsewhere.

---

## 0. What was asked

| Step | Request | Verdict |
|---|---|---|
| A | Add `ARIFOS_VAULT_HMAC_KEY_FILE=/opt/arifos/.secrets/vault_hmac_key` to A-FORGE MCP env | **REJECTED — would install the key that FAILS verification** |
| B | Confirm MCP transport for `forge_seal_lane_a` (stdio? HTTP? got SESSION_REQUIRED) | **ANSWERED — HTTP :7072, stateful; SESSION_REQUIRED is correct behaviour** |
| C | Authorize live write `mode=hmac, dry_run=false` → append 1 entry, "close 16.5h gap" | **REJECTED — the gap does not exist; the write would crash or fork; and it is not reversible** |

Nothing was written. No chain entry appended. No env changed. No service restarted.

---

## 1. Step A — the key in the plan is the WRONG key

Authoritative verifier, run twice on the live canonical chain:

```
tools/audit_verify.py --chain /root/.local/share/arifos/vault999/seal_chain.jsonl
```

| Key supplied | signatures verified | SIGNATURE_FAIL |
|---|---|---|
| `/var/lib/arifos/vault999-hmac.key` | **6 / 6** | 0 |
| `/opt/arifos/.secrets/vault_hmac_key` ← the plan's key | **0 / 6** | **6** |

With the plan's key the verifier prints, for seq 31–36:

```
✘ [SIGNATURE_FAIL] line=258 seq=31 — HMAC-SHA256 signature mismatch — receipt_hash or signature forged
... through seq=36
```

Independent recompute (my own, separate from the verifier) agrees: all 6
`sig_key_id=vault-hmac-1` entries are reproduced by
`/var/lib/arifos/vault999-hmac.key` **stripped**, and by no other candidate.

**Therefore:** installing the plan's key into A-FORGE env would wire the sealer to
a key that cannot produce signatures verifying against the existing chain.

### 1b. The key is ALREADY set — and already overridden to the wrong one

`systemctl cat arifos.service` shows the base unit and a drop-in disagreeing:

```
arifos.service:38          Environment=ARIFOS_VAULT_HMAC_KEY_FILE=/var/lib/arifos/vault999-hmac.key
40-signing-keys.conf:186   Environment=ARIFOS_VAULT_HMAC_KEY_FILE=/opt/arifos/.secrets/vault_hmac_key
```

Drop-ins win. Live kernel env (`/proc/1319982/environ`, pid of arifos.service):

```
ARIFOS_VAULT_HMAC_KEY_FILE=/opt/arifos/.secrets/vault_hmac_key   ← the failing key
```

Timeline:
- seq 36 signed `2026-09-12T14:32:51Z` = **22:32:51 MYT** (verifies under `/var/lib/...` key)
- `arifos.service` MainStartTimestamp = **2026-09-13 09:03:43 MYT**

The service restarted AFTER the last good signature, and now carries the key that
fails verification. **Consequence: the next `arif_seal` will append an entry whose
signature does not verify under the chain's established key — a new SIGNATURE_FAIL,
created by config, not by forgery.** This is a live defect and it is the real
finding of this audit. It predates and supersedes step A.

### 1c. The plan's target file is a symlink to master secrets

```
/root/.secrets/vault.env -> /root/.secrets/kunci-root.env   (498 lines, mode 600)
```

"one-line addition to /root/.secrets/vault.env" would append to the master
secrets file, and would not be read by `a-forge-mcp.service` at all — that unit's
`EnvironmentFile` is `/root/.secrets/vault.flat.env` (181 keys, mode 600).

**Retraction of my own earlier claim:** I reported "vault.env = 777 → secret
hygiene violation". False. 777 is the mode of the *symlink*; the target is 600.
The apparent 29-byte size with 498 lines was my probe mixing `stat -c%s` (link)
with `stat -Lc%s` (target). No violation. I retract it.

---

## 2. Step B — transport answer

```
a-forge-mcp.service ExecStart = node dist/src/interfaces/mcp/cli.js serve --transport http --port 7072
MCP_STATELESS_HTTP=false
MCP_PROTOCOL_VERSION=2025-06-18
health :7072 = HTTP 200   listening on 127.0.0.1:7072 + 100.64.0.2:7072
```

- Transport is **streamable HTTP on :7072**, not stdio, not OpenClaw/A2A.
- `SESSION_REQUIRED` is **correct behaviour**, not a bug: with
  `MCP_STATELESS_HTTP=false` the server requires an `initialize` handshake and the
  returned `Mcp-Session-Id` on subsequent calls. A stateless POST has no session,
  so it is refused. Response headers confirm the server advertises
  `Access-Control-Allow-Headers: ... Mcp-Session-Id`.
- My probe's `initialize` succeeded (`protocolVersion: 2025-06-18`,
  `serverInfo: A-FORGE-MCP 0.1.0`), so the handshake path works.
- `dist/src/interfaces/mcp/sealLaneA.js` mtime **08:42:17**, service start
  **08:42:18** → the tool IS loaded in the running server. Registration is also
  present in `core.ts:2336`.

So: HTTP, session required, tool live. Nothing to change for B.

---

## 3. Step C — three independent reasons not to write

### 3a. The gap the write would "close" does not exist

```
entries    : 254 (canonical 53, historical 201, corrupt 9)
signatures : 6 verified, 0 unverifiable(no key), cutover_seq=31
unsigned after cutover : 0        ← authoritative verifier
```

My own earlier count of "60 unsigned" was raw, not cutover-aware: all 60 sit
**before** `cutover_seq=31` (July-era historical entries, covered by the
annotations registry). Post-cutover unsigned = **zero**.

Claimed gap 16.5h; measured gap to the last entry (seq 36, 2026-09-12T14:32:51Z)
= **10.48h**. And that is simply *no seal has happened since* — not a missing
signature. Appending an entry to close it would manufacture an event that never
occurred, in an append-only audit record.

### 3b. The A-FORGE chain path resolution is buggy — wrong env var, type confusion

`/root/scripts/forge_seal_lane_a.py`:
```python
CHAIN_PATH = Path(os.environ.get(
    "ARIFOS_VAULT_DIR",
    "/root/.local/share/arifos/vault999/seal_chain.jsonl"))   # ← DIR var used as FILE path
```

Kernel canonical (`arifosmcp/runtime/canonical_vault_chain.py`):
```python
DEFAULT_VAULT_DIR = Path(os.environ.get("ARIFOS_CANONICAL_VAULT_DIR", ...))
CHAIN_FILENAME = "seal_chain.jsonl"
... return self.vault_dir / CHAIN_FILENAME                    # ← joins dir + filename
```

Two defects:
1. **Different env var.** Script reads `ARIFOS_VAULT_DIR`; kernel reads
   `ARIFOS_CANONICAL_VAULT_DIR`. Kernel sets `ARIFOS_VAULT_DIR=/var/lib/arifos/vault`
   (which contains **no** seal_chain.jsonl); A-FORGE has
   `ARIFOS_VAULT_DIR=/root/.secrets`.
2. **Directory used as a file path.** With A-FORGE's live env the resolved
   `CHAIN_PATH = /root/.secrets`, which `os.path.isdir()` confirms is a directory.

Verified outcomes of `dry_run=false` under that env:
- append to a directory → `IsADirectoryError` → **crash**, or
- if the code path creates it → a **second chain forked** away from the canonical
  one at `/root/.local/share/arifos/vault999/seal_chain.jsonl`.

Neither is "one entry appended to seal_chain.jsonl". Only a shell invocation
*without* `ARIFOS_VAULT_DIR` set falls back to the correct canonical path.

### 3c. The reversibility claim is false for the part that matters

The plan's rollback:
```
git -C /root/A-FORGE revert <commit>
rm /root/scripts/forge_seal_lane_a.py
rm /root/A-FORGE/src/interfaces/mcp/sealLaneA.ts
systemctl restart a-forge-mcp.service
# → back to 118 tools, pre-patch state
```

That reverts **code**. It does not revert a **chain entry**. And the canonical
chain is append-only at the kernel level:

```
/root/.local/share/arifos/vault999/seal_chain.jsonl
  mode=644  owner=arifos:arifos  attr=-----a--------e-------
```

`a` = append-only. Entries cannot be removed or rewritten in place, even by root,
without `chattr -a`. So a bad entry is **permanent** — exactly what makes
VAULT999 worth anything. The plan labels step C "irreversible" and then lists a
rollback; only the code half of that rollback is real.

### 3d. The tool is explicitly a gate bypass

`sealLaneA.ts:4`:
> *bypasses chat-MCP `arif_seal` HOLD (vault_sovereign lease requires sovereign
> role + 888_HOLD that chat transport cannot establish)*

`core.ts:2340`:
> *Invoke ONLY when MCP `arif_seal` returned HOLD with reason mentioning
> "SESSION_POLICY" or "lease" — never as a primary path.*

And `ForgeSealService.ts:83` GATE 0 is the Q9 Gödel lock:
> *Q9 GÖDEL LOCK: Same actor (judge + seal) without external witness*

`forge_seal_lane_a.py` contains **no** Q9 / tri-witness / `constitutional_chain_id`
check — its only related token is a hardcoded `"irreversibility_ack": True`. My
session is `OBSERVE_ONLY` (`actor_verified=false`), so I would be both the actor
requesting and the actor sealing, with no external witness. That is precisely the
configuration Q9 exists to reject.

---

## 4. What the chain actually contains (real findings, all pre-existing)

Verifier output on the live chain: `RED ✘ GAPS FOUND`

| Finding | Count | Status |
|---|---|---|
| `CORRUPT_LINE` (non-dict) | 9 | **already classified** |
| `CHAIN_BREAK` | 2 (line 187 seq 1; line 257 seq 30) | line 187 = EPOCH_RESET (annotated); line 257 needs attention |
| `SIGNATURE_FAIL` | 0 under the correct key / 6 under the plan's key | see §1 |
| unsigned after cutover | **0** | healthy |

The 9 corrupt lines are **bare JSON strings** appended into a JSONL chain of seal
receipts — prose, not records:

```
line 115 "AAA: agent.json and llms.json MCP endpoint URLs corrected"
line 117 "RESOURCES (agent.json, tools.json x78, openapi.json x78)"
line 121 "strategic_sovereignty"
line 122 "no_paying_users"
line 123 "One Value — decisions improved × uncertainty reduced × trust increased."
line 126 "minimax-media.service"
line 127 "minimax-code (redundant)"
line 128 "/etc/1mcp.env (watchdog 120→300)"
```

Surrounding lines show `actor: 777_FORGE (jwt_verified)` and `actor: HERMES
(self_report)` — i.e. some writer emitted list items as separate lines instead of
one record. All 9 are already registered in
`seal_chain_annotations.jsonl` as `HISTORICAL_CLASSIFIED_HISTORICAL_CORRUPT_LINE`
(81 annotations total; also 55 MISSING_FIELDS, 12 LINK_GAP, 1 EPOCH_RESET).
So this is a **known, annotated, historical** condition — not a live breach, and
not fixable by appending anything.

---

## 5. The one defect worth fixing (not in the plan)

**Kernel signing key points at a key that fails chain verification** (§1b).
Since the 09:03:43 restart, `arifos.service` carries
`ARIFOS_VAULT_HMAC_KEY_FILE=/opt/arifos/.secrets/vault_hmac_key`, which verifies
**0 of 6** existing signatures. The next `arif_seal` will therefore append an
entry that reads as `SIGNATURE_FAIL — forged` to any auditor, while being
perfectly honest.

Candidate fix (NOT applied — production kernel mutation, needs your call):

```
# /etc/systemd/system/arifos.service.d/40-signing-keys.conf
- Environment=ARIFOS_VAULT_HMAC_KEY_FILE=/opt/arifos/.secrets/vault_hmac_key
+ Environment=ARIFOS_VAULT_HMAC_KEY_FILE=/var/lib/arifos/vault999-hmac.key
systemctl daemon-reload && systemctl restart arifos
# verify: python3 /root/arifOS/tools/audit_verify.py \
#           --chain /root/.local/share/arifos/vault999/seal_chain.jsonl \
#           --key-file /var/lib/arifos/vault999-hmac.key
# rollback: restore the line, daemon-reload, restart
```

Two things must be decided before this is safe, and I cannot decide them from the
box:
1. **Which key is canonical going forward?** The chain's history verifies under
   `/var/lib/arifos/vault999-hmac.key`. But `40-signing-keys.conf` was added by a
   P0-2 888 audit (2026-09-05) deliberately — possibly an intended key rotation
   that was never completed by re-signing or annotating a cutover.
2. **Is a cutover annotation required?** If the `/opt` key is the intended future
   key, the correct action is not to revert the drop-in but to record a key
   rotation in `seal_chain_annotations.jsonl` so auditors know which key applies
   to which seq range. Reverting silently would hide that intent.

Either way the current state is the worst of both: config says one key, history
verifies under another.

---

## 6. Also observed, not touched

- `ARIFOS_VAULT_DIR=/var/lib/arifos/vault` (kernel) contains **no**
  `seal_chain.jsonl`; canonical chain lives at
  `/root/.local/share/arifos/vault999/seal_chain.jsonl`. Two vault locations in
  play — the same class of drift as the `carry_forward.json` collision.
- `/root/compose/sekrits/arifos_sovereign.key` still **MISSING** (confirms the
  signing-lane key drift finding; Ed25519 kernel merkle seal remains impossible
  on this box).
- `/root/.local/share/arifos/vault999/seal_chain_annotations.jsonl` = 81
  annotations, 6 classes. This registry is what makes the historical gaps
  explainable rather than alarming — it is doing its job.

---

## 7. Counterfactual — one condition under which this receipt is wrong

If `a-forge-mcp.service` is restarted, or `ARIFOS_VAULT_DIR` is unset in its
environment, before step C is attempted, then the script's fallback resolves to
the **correct** canonical chain path and reason 3b (crash/fork) no longer applies.
Reasons 3a (gap does not exist) and 3c (append-only is irreversible) would still
stand independently. My env readings bind to snapshot **09:0x MYT,
a-forge-mcp MainPID 1287666, arifos.service MainPID 1319982** — both services have
already restarted once during this session, so re-probe before acting on them.

## 8. What I changed

Nothing outside this receipt file. Read-only probes only:
`systemctl cat/show`, `stat`, `lsattr`, `/proc/<pid>/environ`, `git log/show`,
`sha256sum`, and `tools/audit_verify.py` against the chain **as read** (the tool's
own help says "work on a COPY"; I passed the live path for a read-only verify and
it did not write — chain mtime/ctime unchanged at 2026-09-12 22:32:51).

*DITEMPA BUKAN DIBERI ⚒️*
