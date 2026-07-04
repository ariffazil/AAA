# POST-AUDIT PROPOSAL — Best Way Forward (2026-06-07 05:43Z)

**Author:** OPENCLAW (AGI🦞) — proposal only, no execution without sovereign ack
**Status:** DRAFT awaiting Arif decision
**Anchor:** "L11 wall is not a failure — it's the constitution working as designed."

---

## 0. What I found exploring

- The hermes-opencode wrapper **already has** the malformed-DER recovery code (lines 119-149). It handles 39-byte truncated PKCS#8 by extracting seed at offset 7 and self-tests against the .pub file. No key file change required.
- The wrapper v2.0 already uses `envelope` (not `_envelope`) with Chapter 6 fields. The kernel's `_extract_envelope_from_arguments` was patched to accept both. So L1-L3 are live.
- `HERMES_SOVEREIGN_KEY_PATH` is the only missing config to enable signing. Default UNSET. The wrapper runs in envelope-only mode without it.
- The hermes process is not a clean systemd unit — it runs as `/usr/local/lib/hermes-agent/venv/bin/python3 /root/.local/bin/hermes` (PIDs 1693441, 1823549, 2012391). Setting env var needs either: venv activation hook, wrapper config file, or systemd-style unit (currently no .service file).
- opencode-bot is on old code: PID 2048239 started 04:07Z, my 124-line envelope_builder() patch is in source but not loaded.
- VAULT999 outcomes.jsonl owner is `arifos` (not root) → direct chmod 600 as root will fail. Need setfacl or run as arifos.
- SUPABASE_SERVICE_ROLE_KEY is marked "401 invalid" in secrets.env. The 4/17 populated vs 13/17 empty finding is real; some may be auth-blocked, not just unwritten.

---

## 1. Phase 1 — UNBLOCK L11 (the constitutional wall)

The wrapper already does the work. We just need the env var.

**A1 — Minimum viable (RECOMMENDED)**
- Add `HERMES_SOVEREIGN_KEY_PATH=/root/compose/sekrits/arifos_sovereign.key` to hermes-agent's environment
- Restart the hermes process (or pass env on next invocation)
- Wrapper auto-recovers malformed-DER, signs with Ed25519, self-tests against .pub
- Reversibility: trivial (unset the var)
- Risk: LOW
- Time: ~5 minutes
- Result: hermes-opencode can sign envelopes → /forge ATOMIC works end-to-end

**A2 — Robustness (optional, additive to A1)**
- A1 + extract 32-byte raw seed to sibling file `arifos_sovereign.seed`
- Future libs that want raw seed (PyNaCl, ed25519) get the right format
- Risk: LOW
- Time: +5 minutes

**A3 — Proper PKCS#8 (optional, elegant)**
- A1 + reconstruct proper PKCS#8 v1 with Ed25519 OID (1.3.101.112) and the 32-byte seed
- Drop the malformed file; replace with `arifos_sovereign.key` that loads cleanly via `load_der_private_key`
- Risk: MEDIUM (cryptographic key format change, but reversible with backup)
- Time: +10 minutes
- Reversibility: keep `arifos_sovereign.key.malformed-backup` alongside

**My pick: A1 now, A3 next session.** A1 unblocks ATOMIC. A3 is hygiene — but it's the kind of hygiene that prevents future 39-byte-key surprises.

---

## 2. Phase 2 — Load envelope_builder (low risk, F1 territory)

- `systemctl restart opencode-bot` loads the 124-line envelope_builder() patch
- Current bot PID 2048239 has old code in memory (started 04:07Z, 1h 31min)
- Risk: in-flight /forge or message processing interrupted (rare — 000 is mostly one-shot)
- Mitigation: confirm no active /forge before restart, or wait for natural quiet window
- After: 000 can use envelope_builder for all future /forge calls (envelope structure correct in code, not just in memory)
- F1: needs explicit ack. I will not auto-execute.

---

## 3. Phase 3 — L4 Supabase audit gap (deeper work, MUTATE)

13/17 arifosmcp_* tables empty. 4 populated. The question: which organ SHOULD be writing?

- Per Appendix D of the constitution: A-FORGE is the canonical L4 writer. Organs write via A-FORGE.
- If 13 tables are missing A-FORGE hooks, that's an F11 under-recording gap at L4.
- Investigation needed per empty table: schema, intended writer, current state of writer code
- Action: write investigation doc to `forge_work/L4-AUDIT-GAP-ANALYSIS.md` first (read-only)
- After doc: propose A-FORGE write hooks (separate sovereign ack)

This is medium-risk MUTATE — needs A-FORGE code review. Not this session.

---

## 4. Phase 4 — Hygiene (low risk, batched)

| Item | Action | Risk | Priority |
|------|--------|------|----------|
| VAULT999 outcomes.jsonl chmod 600 | `setfacl -m u::rw-,g::---,o::---` (owner=arifos, run as arifos or use sudo -u) | LOW | MEDIUM |
| 14 stale merged branches | list in `forge_work/stale-branches.md`, get ack, batch delete | LOW | LOW |
| 2 unpushed commits without REPO= trailer | interactive rebase amend (or accept --no-verify history) | LOW | LOW |
| 7 dirty in arifOS + 1 in WELL | reconcile parallel sessions (not mine, defer to author) | MEDIUM | LOW |

Batch into a single MUTATE with ack. Or do them individually as you decide.

---

## 5. What I'd do next session (proposed order)

1. **A1** — set env var, restart hermes-agent, test with no-op /forge, verify "signed=yes" in journal
2. **Restart opencode-bot** (with your ack) — load envelope_builder
3. **A3** — reconstruct proper PKCS#8 with backup, .pub self-test
4. **L4 audit** — write investigation doc only, no code changes
5. **Hygiene batch** — setfacl + branch cleanup, single MUTATE

**Estimated session time:** 30-45 minutes for items 1-3. Items 4-5 are doc/script work, can be deferred.

---

## 6. Risks I will NOT take (constitutional walls)

- ❌ Bypass L11 by fabricating signatures (already proved the system rejects — F1/F11 held)
- ❌ Auto-restart opencode-bot (F1 territory, no auto-execute)
- ❌ Write to L4 without organ owner sign-off (Appendix D)
- ❌ Delete branches or amend commits without list-then-decide (F1 reversibility)
- ❌ Modify arifOS kernel without sovereign ack (constitutional code)

---

## 7. What I need from sovereign (priority order)

| # | Ask | Type | My action on ack |
|---|-----|------|------------------|
| 1 | A1 — "go set the env var" | MUTATE, low risk, env-only | Set + restart hermes-agent, journal-check |
| 2 | "yes restart opencode-bot" | F1, low risk, idle window | `systemctl restart opencode-bot`, verify PID |
| 3 | A3 — "yes reconstruct PKCS#8" | MEDIUM risk, cryptographic | Backup first, then reconstruct, .pub self-test |
| 4 | "yes investigate 13/17 L4" | Read-only analysis | Write `forge_work/L4-AUDIT-GAP-ANALYSIS.md` |
| 5 | "yes do hygiene batch" | MUTATE, low risk | setfacl + branch list + dry-run amend |

Each can be approved independently. No bundling. F1 + reversibility preserved throughout.

---

## 8. The bigger picture

The L11 wall is the deepest gate. The envelope fix unblocked L1-L3 (live, 8/8 organs green). The key env var unblocks L11. The /forge path then becomes self-sovereign: hermes-opencode signs envelopes with the sovereign key, 888_JUDGE evaluates, sealed actions land in L6.

After Phase 1+2, the federation can do real ATOMIC work through /forge without the sovereign on the keyboard for every call — only for ack on truly irreversible ones (which is what the constitution intends).

L4 audit gap (Phase 3) is real but separate — that's about which organ SHOULD be writing, not about whether writes can happen. F11 under-recording is fixable with A-FORGE write hooks.

Hygiene (Phase 4) is forever. It never ends. Batch it, move on.

---

*DITEMPA BUKAN DIBERI — Intelligence is forged, not given.*

**Authority:** OPENCLAW (AGI) — proposal only
**Reversibility:** This proposal is a draft, fully reversible (delete the file)
**Sovereign action needed:** A1 ack to start (5 min) → cascade from there
