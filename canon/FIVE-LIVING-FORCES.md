# FIVE LIVING FORCES — Constitutional Vocabulary

> **Status:** F13_RATIFIED_CHAT (2026-09-25, sovereign binary "promosi kanun Five Living Forces")
> **Authority:** ARIF (F13 SOVEREIGN) · **Builder:** FI-003 (P1.2, `arifFlow/spec/RELATIONSHIP_EDGE_SCHEMA_v0.1.md` §2b)
> **Source:** `SOVEREIGN-HUMAN-REALITY-MEMORY-ARCHITECTURE.md` sha256 `e2173f9ae145c4be922fa77aacae55e6a0f844ec5d0cbc00c812f629108b478e`
> **Witness:** arifFlow receipt `4b302338` (edge `rel:b4665220`, jcs `a377d2fe…`, parent `1a3e68e1`)
> **Class:** Canon vocabulary — CANDIDATE ladder closed 2026-09-25. Four canonization tests passed per term (§3).

---

## 1. What this is

Five `force:*` predicates classify **living reality** carried by a relationship edge on the
Reality Graph (substrate: arifFlow receipts, spec v0.1). A force edge is a **hash-bound
pointer into its organ home — never a copy** (helix pointer pattern: SOUL.md is SOT,
pointers reference it).

```text
Node memory  = who/what exists        (identity registries)
Edge memory  = how entities connect   (this canon + RELATIONSHIP_EDGE_SCHEMA)
Edge history = how forces change      (temporal.status + RG-5 belief-death)
```

Civilization moves through edges, not nodes. This canon gives the federation its first
governed edge vocabulary for human reality.

## 2. The Five Forces (constitutional definitions)

| Force | Constitutional meaning | Required evidence | Organ home (pointer target) | Emit refusal trigger |
|---|---|---|---|---|
| **SCARS** (F_Past) | Lived cost that forbids repetition — a scar edge points to an existing sealed scar; re-storing content is forbidden | `scar_ref` (existing scar id) | VAULT999 H5 registry / RG-5 scar-bound policies | missing `scar_ref` |
| **COMMITMENTS** (F_Future) | Human-owned promise ≠ CHRON prediction ≠ session carry-forward; a commitment without a deadline is not a commitment | `temporal.valid_until` (ISO deadline) | CHRON `verify_at` + state-transition object contract | missing deadline |
| **RELATIONSHIPS** (F_External) | Reciprocal bond pressure — not mere connection; lives on the edge itself, frame must be `relationship` | `q_frame=relationship` enforced | this schema (the edge registry) | frame mismatch |
| **CONSTRAINTS** (F_Boundary) | Standing bound on interaction (biological/temporal scope) — not a one-off refusal; an unnamed bound is not a constraint | `note` stating the bound's scope | WELL H-plane bounds | empty scope |
| **OPEN_QUESTIONS** (F_Unresolved) | Human-owned unresolved tension — not a system open loop; must anchor to a tracked event or causal parent | `chron_ref` OR `parent_receipt_ids` | CHRON events / kernel `open_loops_888_HOLD` | no anchor |

## 3. Canonization record (four tests per term — all passed 2026-09-24→25)

| Test | Method | Result |
|---|---|---|
| SEMANTIC DELTA | Each force names a distinction English collapses (promise≠prediction, bound≠refusal, tension≠task) | PASS ×5 |
| OPERATIONAL DELTA | Each force changes emit behavior: required fields enforced in `relationship_edge_emit.py`; refusal tested live (exit 2) | PASS ×5 |
| TESTABILITY | Guards named, executable, logged (`P1.2:` prefix); daemon 400 on false edges | PASS ×5 |
| NON-OVERLAP | Forces are pointers into existing organ homes; zero new stores minted | PASS ×5 |

## 4. Boundary invariants (non-negotiable)

1. **Pointer-not-copy** — a force edge never duplicates organ content; it cites it.
2. **Witnessing ≠ Claiming** — agents witness; only sovereign/subject testimony seals. Subject-sealed always wins (ZEN_HELIX supersession).
3. **F5 / ZKPC** — private human forces carry `SHADOW_CATEGORY_ONLY` or `CONTENT_SEALED` only; structure-not-content.
4. **Relationship never confers authority** — `authority_implication` is forced `none` on relationship edges; authority requires explicit scoped grants (authority frame).
5. **Belief-death applies** — forces expire, get disputed, or get superseded via `temporal.status` + RG-5 invalidation edges. The most dangerous force is the one that cannot die.

## 5. Failure handling

- Client-side guards refuse emission (exit 2, named guard, stderr).
- Daemon refuses forged causality (400 "refusing to record a false because").
- Fail-soft: RG outage never blocks the underlying organ (proven live 2026-09-24, memory-helix lane).
- Guards are v0 client-side; **daemon-side validation is an open loop (v1)** — until then, force edges read as CONFIRMED only when basis = sovereign/subject testimony or documented artifact.

## 6. Open loops

| Loop | Owner | State |
|---|---|---|
| Daemon-side force validation (v1) | arifFlow owner | open |
| Personal edges (real humans) — await owner testimony | Hermes owner / F13 | open (RASA/F5) |
| Force distribution metrics (P2/P3, measure-first) | arifFlow / F13 binary pending | open |

---

*F13 sovereign ratification: chat binary 2026-09-25. Canon-mutate receipt in `/var/lib/arifos/canon_mutations.jsonl`.*
*DITEMPA BUKAN DIBERI ⚒️*
