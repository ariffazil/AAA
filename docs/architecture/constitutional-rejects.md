# Constitutional Rejects — arifOS Federation

> **Public-facing summary** of the HARAM canon.
> **Source of truth:** `/root/arifOS/docs/HARAM_DOCTRINE.md` (read-only canon, F13).
> **Last sync:** 2026-06-13
> **Authority:** F13 SOVEREIGN (canon is sovereign-ratified)

This is the public-readable version of the constitutional rejects. The internal
canon (`HARAM_DOCTRINE.md`) carries the full citation chains, the F-floor
violation analysis, and the procedure for adding/removing entries. This page
is the executive summary — for **why each pattern is rejected** and **what
arifOS does instead**.

---

## The 5 rejects (as of 2026-06-13)

| # | Rejected pattern | Why | arifOS position |
|---|---|---|---|
| **H1** | `--experimental` global flag for new backends/tools | Smuggles new surfaces past the 13-tool canonical contract | New MCP tool is in the canonical 13, or it does not exist |
| **H2** | "Skills are written by the harness" (agent self-authors canon) | F11 + F12 failure mode; memory poisoning; agent self-authorisation | Helpers are agent-editable; canon is sovereign-ratified |
| **H3** | YOLO mode (auto-approve all tools, lift workspace boundary) | Constitutional exit wound; F13 veto bypassed; F1 floor bypassed | There is no auto-approve mode. Period. |
| **H4** | Backward-compat via deprecation aliases | Accumulates debt; parser aliases are irreversible commitments | F11 seal **is** the deprecation signal. No parser aliases. |
| **H5** | Community-PR skill model / "Don't write secrets" as a courtesy | F11 AUTH is cryptographic, not courteous; public corpus ≠ sovereign truth | SOPS+AGE+ED25519+per-IPC token; skills cross via sovereign-ratified merge |

---

## Why negative canon exists

Most codebases document what they **do**. Few document what they **explicitly
refuse to do**. The HARAM list exists so that:

1. **Future agents** do not re-litigate the decision. If a new pattern lands
   on the HARAM list, the default is *rejection*, not *debate*.
2. **Operators** (Arif, federation peers, downstream integrators) can
   audit the constitution by reading the negative surface. A federation
   that says "we don't do X" is more governable than one that says "we do
   Y" and leaves the no's implicit.
3. **The constitution is versioned, not aliased.** When a HARAM is
   removed, the F13 record shows when, why, and what replaced it. The
   history is part of the canon.

---

## The constitutional floor map (quick reference)

For each reject, the floor(s) it would violate:

| Reject | F1 | F2 | F4 | F5 | F11 | F12 | F13 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| H1 experimental flag | ✓ |   | ✓ |   |   |   |   |
| H2 agent-writes-canon |   |   |   |   | ✓ | ✓ |   |
| H3 YOLO mode | ✓ |   |   | ✓ |   |   | ✓ |
| H4 deprecation aliases | ✓ |   | ✓ |   |   |   |   |
| H5 community-PR secrets |   | ✓ |   |   | ✓ |   |   |

If you are proposing a new pattern, the first question is: **does it
violate any of these floors?** If yes, you are in HARAM territory. The
proposal needs an F13 override, not a re-debate.

---

## How the list grows and shrinks

**Both directions are F13 territory.**

- **Adding** a new reject: surface the pattern in an ADR with `Status:
  PROPOSED`, cite the source eureka, state the arifOS alternative, submit
  to `arif_judge_deliberate` for SEAL.
- **Removing** an existing reject: same procedure, but the entry is
  **superseded**, not edited. The history of why the pattern was rejected
  is part of the canon.

The list of 5 here is the load-bearing set as of 2026-06-13. It is not
permanent. It is the **federation's immune system** as currently configured.

---

## Where to read more

- **Full canon with citations:** `/root/arifOS/docs/HARAM_DOCTRINE.md`
- **Source brief:** `/root/AAA/docs/architect-briefs/distill-mxc-ds-bh-2026-06-13/brief.md` §2.3
- **ADRs:** `decisions.md` in the same brief, ADRs 002, 003, 004, 005, 009
- **F-floor definitions:** `/root/arifOS/arifosmcp/constitutional_map.py::CANONICAL_TOOLS`
- **Task graph:** `task_graph.yaml` in the same brief, phase P11

---

*DITEMPA BUKAN DIBERI — The rejects are forged, not given. To remove one, F13.*
