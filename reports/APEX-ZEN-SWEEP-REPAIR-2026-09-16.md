# APEX-ZEN Sweep — Repair Provenance (2026-09-16)

> **Authority:** F13 (Arif) — "ok do all", 2026-09-16
> **Backup:** `/root/.hermes-backups/agent-cards/pre-apex-zen-fix-20260916-063000.tar.gz`
> **Repaired by:** Hermes · **Pre-state commit:** `1f9b41756739b2f0566b06ce1901ca4558110157`
> **Introducing commit:** `a9df079d2` — *chore(apex-zen): federation alignment sweep committed + opencode SOUL.md forged* (2026-09-16T03:21:38+08:00, 34 files, +546/−68)

---

## What was wrong

### Defect 1 — capability/lane stamps were a bulk default, not derived

Commit `a9df079d2` appended an `apex_zen` block to agent cards. Every card whose
lane had never been assigned received `capability: "BUILD"` — a hardcoded value.

**Measured scope (realpath-deduped; `/root/AAA/agents/<x>` are symlinks into `_lanes/`):**

| | count |
|---|---|
| glob hits for `agent-card.json` | 43 |
| **unique files** (4 symlink duplicates removed) | **39** |
| cards carrying `apex_zen` | 30 |
| cards with an **assigned** lane and a **wrong** capability | **0** |
| cards with `lane: "unassigned"` + defaulted `BUILD` | **6** |

The canon map is direct (`333-AGI→BUILD · 555-ASI→VERIFY · 888-APEX→JUDGE ·
777-forge→ACT · VAULT999→WITNESS`), so the defect is narrow and objective: **six
cards**, all of them the ones whose lane was never set.

Notable instance — `agents/hermes/agent-card.json` declared
`role: EDGE_BRIDGE`, `authority: DISPLAY_ONLY`, `max_action_class: OBSERVE`,
`authority_ceiling: ROUTE_BRIDGE`, and its own `civ21_binding` reads *"I DO NOT
audit. I DO NOT judge. I DO NOT reflect."* — while carrying
`capability: "BUILD", lane: "unassigned"`. The card contradicted itself, and the
contradiction was a hardcoded default, not a decision.

### Defect 2 — signature blocks claimed a seal that could not verify

**All 39 signature blocks were unverifiable:**

| class | count | material |
|---|---|---|
| JWS-shaped, template `kid` | 21 | `protected` decodes to `{"alg":"EdDSA","typ":"JOSE","kid":"arifos-a2a-card-2026-%q"}`; `signature` is a genuine **64-byte Ed25519** value (correct length) — but the key id contains a **literal, unsubstituted** template specifier, so the signature cannot be attributed to any key. The body was also modified after signing. |
| hollow block | 14 | `{kid: null, signature: "", protected: ""}` — structurally present, cryptographically empty. Confirmed via `git show a9df079d2~1`: these were **already empty before** the sweep. |
| no block at all | 4 | `_external/{agy,copilot-cli,mesa-test-agent,opencode}` |

**No agent-card verifier exists anywhere in the federation.** The `[NEXT]` line
printed by `/root/AAA/scripts/sign-agent-card.sh` instructs the operator to run
`verify_card(...)` — **that function does not exist**. `sovereign_verify.py`
verifies *request* signatures (constitution hash + nonce challenge), not cards.
`sign-agent-card.sh` itself expects a different shape entirely
(`Ed25519Signature2020` with `proofValue` / `verificationMethod`), which none of
these blocks matched.

So nothing was ever verifying these, and nothing broke — the audit trail simply
asserted something untrue.

---

## What was changed

**30 files rewritten** (`git diff --stat`: 30 files, +660/−287).

### Capability / lane — 6 stamps repaired, each evidence-derived

Stamp follows the card's **own declared fields**, never the product's marketing.
Where two fields on one card contradict each other, the stamp follows the
stronger evidence **and the contradiction is recorded** — not silently resolved.

| card | was | now | basis |
|---|---|---|---|
| `hermes/` | BUILD / unassigned | **WITNESS / EDGE_BRIDGE** | role, authority, max_action_class, ceiling, civ21 self-description |
| `hermesarifos-bot/` | BUILD / unassigned | **WITNESS / VAULT999** | DISPLAY_ONLY ceiling + declared VAULT999 memory function (clean canon map) |
| `forge-bot/` | BUILD / unassigned | **ACT / 777-forge** | `authority=EXECUTE_AFTER_SEAL` + declared A-FORGE execution function |
| `antigravity/` | BUILD / unassigned | **ACT / 777-forge** | `role=forge_instrument`, `ceiling=EXECUTE_AFTER_SEAL` |
| `skill-auditor/` | BUILD / unassigned | **VERIFY / 555-ASI** | OBSERVE_ONLY ceiling + auditing function |
| `prospect-maturation/` | BUILD / unassigned | **BUILD / 333-AGI** | declared construction chain: basin → physics → prospect → volumetrics → risk → well proposal |

Each carries an `apex_zen.derivation` object recording `basis`, `evidence`,
`method`, `stamped_by`, `stamped_at` — so the stamp is auditable, not asserted.

`WITNESS / EDGE_BRIDGE` is a **declared non-lane locus**, not a fifth chain lane:
Hermes is neither a lane node nor an actuator. Forcing it into `888-APEX` would
be false (it explicitly never judges); `555-ASI` likewise (it never audits).

### Signatures — honest state, evidence preserved

For all 35 cards that had a block:

```json
"signature_legacy": [ ...verbatim prior material, nothing destroyed... ],
"signature_status": {
  "state": "ABSENT",
  "detail": "...template kid / hollow block...",
  "conforms_to": "Ed25519Signature2020 — see /root/AAA/scripts/sign-agent-card.sh",
  "verifier": "none — no agent-card verifier exists; verify_card() is a dead pointer",
  "detected_by": "/root/scripts/agent-card-drift-detector.py",
  "material_preserved_under": "signature_legacy",
  "requires": "888-APEX + air-gapped key /mnt/usb/sovereign.pem"
}
```

The live `signatures` key is dropped (it implied a seal that does not exist);
the material itself is **preserved verbatim** under `signature_legacy`. Nothing
was deleted.

---

## Deliberately NOT changed

- **`registry_receipt_hash`** — 12 cards carry a receipt hash alongside
  `registry_tool_count: {source:0, registry:0, card:0}`. Removing a hash that
  cannot be *disproved* would destroy possible evidence. **Reported, not deleted.**
- **`_external/*` capability stamps** — all `_external` cards have an assigned
  lane (333-AGI) and a canon-correct capability. Left alone.
- **Canonical doctrine fields** (`canonical_ref`, `governance_chain`,
  `invariant`, `doctrine`, `motto`) — correct on every card. Kept.
- **Nothing re-signed.** No key was present, and inventing a signature would be
  the exact failure this repair exists to remove.

---

## Open items for 888 / F13

1. **Two cards contradict themselves** and the contradiction is now *recorded*,
   not resolved:
   - `forge-bot` — `authority=EXECUTE_AFTER_SEAL` vs `authority_ceiling=DISPLAY_ONLY`
   - `prospect-maturation` — `authority_ceiling=OBSERVE_ONLY` vs an autonomous construction function
   - `skill-auditor` — `authority: "888"`: an APEX **lane** label used where an
     authority **class** belongs
2. **Duplicate card for one tool** — `antigravity/` (ACT / 777-forge) and
   `_external/agy/` (BUILD / 333-AGI) describe the same Google Antigravity CLI
   with two different stamps.
3. **Four card trees, no ratified SOT** — see
   `/root/AAA/agent-cards/CARD_TREE_DRIFT_2026-08-27.md`: `agent-cards/identity/`
   (read by `arifosmcp/runtime/authority.py`), `a2a-server/agent-cards/`,
   `agents/`, and `/opt/arifos/identity/agent_identities.json`. The kernel reads
   the **legacy** tree — which never received `apex_zen` — so **runtime
   authorisation was never affected** by this repair. Verified: no running
   process holds `/root/AAA/agents/` open.
4. **Real seals are owed.** `sign-agent-card.sh` exists and works; it needs
   `/mnt/usb/sovereign.pem`, which was not mounted.

---

## Verification

```bash
# drift detector — should report WARN only on the 12 D6 receipt hashes
python3 /root/scripts/agent-card-drift-detector.py

# the invariant that matters: the edge bridge no longer claims BUILD
python3 -c "import json;d=json.load(open('/root/AAA/agents/hermes/agent-card.json'));print(d['apex_zen']['capability'], d['apex_zen']['lane'])"
# -> WITNESS EDGE_BRIDGE
```

Rollback: `tar xzf /root/.hermes-backups/agent-cards/pre-apex-zen-fix-20260916-063000.tar.gz`
or `git revert <repair-commit>`.

---

## Lesson

The sweep was built and committed at 03:21 with **no checker**, so a hardcoded
default (`capability: "BUILD"`) and 35 hollow signature blocks reached a signed
governance tree undetected. The repair is smaller than the detector matters:
`/root/scripts/agent-card-drift-detector.py` now runs as the missing check, and
it is wired to cron. **A seal that nothing verifies is decoration.**

*DITEMPA BUKAN DIBERI ⚒️*
