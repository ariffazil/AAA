# JURISDICTION DOCTRINE — Domain vs Constitutional Separation

> **Status:** F13_RATIFIED_CHAT (sovereign directive 2026-09-17, 333-AGI canon synthesis).
> **Origin:** GEOX `prospect.py` JURISDICTION-001 patch + sovereign ledger directive.
> **Source labels (F2):** OBS — GEOX `prospect.py:391-450` shows the implemented contract.
> DER — pattern generalises from GEOX to WEALTH/WELL as same-class domain organs.
> SPEC — the full `DomainEvidenceEnvelope` field set below extends beyond what is currently encoded in GEOX; the implemented subset is marked `[IMPLEMENTED]`.
> **No ChatGPT round-2 source material was located on disk** despite a wide grep across `/root/docs`, `/root/memory`, `/root/AAA`, `/root/A-FORGE`, `/root/WEALTH`, `/root/arifOS`, `/root/GEOX`, `/root/.local/share/arifos`. This fragment is the sovereign ledger directive compressed with the GEOX patch as primary evidence. If the ChatGPT analysis is later surfaced, append as §9 with full provenance.

## 1. The violation (HARAM)

**Expertise(D) ⇏ Authority(D).** A domain organ may possess *competence* (Earth evidence for GEOX, capital math for WEALTH, vitality signals for WELL) without possessing *sovereign authority* to mint a verdict that authorises irreversible action. The previous GEOX `prospect.evaluate` path locally minted `GovernanceStatus.SEAL` if `ac_risk_score < 0.5` — **domain competence impersonating sovereign authority**. Closed 2026-09-17 (commit on the GEOX working tree; deploy verified this turn).

## 2. The verdict vocabulary — physically separated

| Class | Verdict values | Producer | Authority to ACT? |
|---|---|---|---|
| **DOMAIN** `[IMPLEMENTED in GEOX]` | `PHYSICALLY_SUPPORTED` \| `HYPOTHESIS` \| `INSUFFICIENT_EVIDENCE` | GEOX, WEALTH, WELL | **NO** |
| **CONSTITUTIONAL** `[IMPLEMENTED]` | `SEAL` \| `HOLD` \| `SABAR` \| `VOID` | arifOS 888 only | **YES** (after F13 ack for irreversible) |

**`PHYSICALLY_SUPPORTED` ≠ `AUTHORIZED`.** A domain verdict of `PHYSICALLY_SUPPORTED` is the *necessary precondition* for an action; it is not *sufficient*. The sufficient verdict (`SEAL`) is arifOS-only and is gated by F13 sovereign ack for irreversible work.

## 3. DomainEvidenceEnvelope contract

When a domain verdict touches constitutional scope, the envelope MUST carry:

```yaml
domain_verdict:        enum {PHYSICALLY_SUPPORTED, HYPOTHESIS, INSUFFICIENT_EVIDENCE}  # [IMPLEMENTED]
verdict_class:         "DOMAIN"                                                          # [IMPLEMENTED]
recommended_handoff:   "arifOS (888 judge)"                                              # [IMPLEMENTED]
awaiting_verification: true        # ALWAYS true until arifOS responds                   # [IMPLEMENTED]
sealed:                false       # ALWAYS false at domain boundary                    # [IMPLEMENTED]
constitutional:                                                                            # [IMPLEMENTED]
  adjudicated_by:      "arifOS"
  verdict:             <one of SEAL|HOLD|SABAR|VOID>
  judge_state_hash:    <sha256 from arifOS judge>
  delegation:          "JURISDICTION-001: domain organs never self-adjudicate"
evidence_refs:         [<source citations>]   # [SPEC — GEOX has evidence_ids at claim layer; not yet folded into envelope]
authority_ceiling:     <scope string from organ contract>   # [SPEC — A-FORGE forge_actuator_authority; not yet stamped on domain envelope]
delegation_error:      <string, if judge unreachable>      # [IMPLEMENTED, optional]
```

## 4. Delegation contract

1. Domain organ builds payload via `build_governed_payload()` (GEOX: `geox_core.integrations.arifos_governance`; WEALTH: equivalent; WELL: equivalent).
2. Domain organ calls `call_judge(arifOS)` via the integration bridge.
3. **If judge unreachable → HOLD. Never mint SEAL locally.** Graceful degradation, not a fallback path that violates the rule. `[IMPLEMENTED in GEOX]`
4. `ack_irreversible: true` remains required at the user boundary (defence in depth).

## 5. Cross-references (live)

| Item | Surface | Status |
|---|---|---|
| **arifOS mode-aware risk** | `arifosmcp/runtime/tools.py:851` + `:1737` | root-cause located; source patch ready; **888-HOLD pending** (deployed wheel `bd4880e` is one commit behind source `cf9ceab`) |
| **GEOX implemented** | `/root/GEOX/src/geox_mcp/tools/prospect.py:391-450` | source + **deployed this turn** (T2 announce); health self-classification `degraded` is stale build metadata, jurisdiction fix live (md5 match) |
| **A-FORGE actionClassifier F10** | commit `b7e06135` | `forge_visual_seal` removed from OBSERVE set (was dual-classified ghost) |
| **Musyawawah GATE systemic** | `arifflow_fq_g` + dry-run reports | 2,775 Seal receipts missing `musyawawah_reference` (cron-actor systemic); F11 audit finding |

## 6. Anti-patterns (HARAM, post-2026-09-17)

- ❌ Domain organ mints `GovernanceStatus.SEAL` / `AUTHORIZED` / `sealed: true` locally.
- ❌ Constitutional verdict embedded in a domain tool response without explicit `verdict_class: "CONSTITUTIONAL"` + `adjudicated_by: "arifOS"` stamp.
- ❌ `sealed: true` on a payload that has not passed through arifOS 888.
- ❌ Default-to-SEAL on judge-unreachable (graceful degradation = HOLD, not SEAL).
- ❌ Tool metadata declaring `EXECUTE`/`blast_radius:high` for what is actually a mode-aware query-only call (e.g., `arif_forge` with `mode=dry_run`/`query`) — pending arifOS patch.

## 7. Authority

- **Expertise lives in the domain.** GEOX reads Earth evidence. WEALTH computes capital. WELL mirrors vitality.
- **Authority lives in arifOS 888 + F13.** Constitutional verdicts are minted here, gated by sovereign ack.
- **Action is the human/F13 layer.** Neither domain nor kernel may execute irreversible work without F13.

## 8. Metrics (jurisdiction leakage, separate task)

Pending wiring (item 6 in the ledger):
- `JurisdictionLeakRate` — domain envelopes with `sealed: true` or constitutional verdict class (must be 0).
- `SurfaceAgreementRate` — domain verdict vs constitutional verdict agreement rate.
- `DecisionSemanticContradictions` — count of `verdict_class: "DOMAIN"` paired with `verdict: "SEAL"` without proper delegation stamp.

DITEMPA BUKAN DIBERI ⚒️

*Composed by 333-AGI, 2026-09-17. F2 source labels: see §0. No fabrications. Where the ledger referenced a "ChatGPT round-2 analysis" as source material, that artifact was not located on disk; the fragment above stands on GEOX patch + sovereign directive + the canon-fingerprint of the doctrine already encoded in arifOS/A-FORGE working trees. If the ChatGPT analysis surfaces later, append as §9 with full provenance.*
