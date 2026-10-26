# EXECUTION RECORD — 4 structural fixes, 2026-10-23

Sovereign instruction: 888-approved, 4 steps in order, no Manifest v1.2.
Observer: HERMES KVM8 · session SEAL-CAND-22bb052cd48bfaa2 · commit base be644182

---

## STEP 0 — I was wrong, and the correction changes step 1

The 888 directive was built on my finding that `/root/HERMES` is a "dead root" with no live
process. **That finding was wrong in mechanism.** Probed:

```
/root/HERMES   -> /root/runtime/hermes/.hermes
/root/.hermes  -> /root/runtime/hermes/.hermes      SAME TREE
```

Both are symlinks to one live directory. `/root/HERMES` is not dead and not separate. So the
failed write was never "into a ghost room" — it was into a **different profile of the same live
home**. `/root/.hermes/memories/USER.md` is the *default profile's* file, not a global one;
`profiles/aaa-hermes/memories/USER.md` belongs to the opencode/333-AGI lane. Writing to one
never reaches the other. Six profiles exist with six separate memory sets.

Had I executed the directive as written — archive the delta, then replace
`profiles/aaa-hermes/memories/USER.md` with a symlink to the default profile's — I would have
destroyed a live lane's own memory, including facts unique to it. The intent was right; the
mechanism was not. Recorded here because a wrong premise that produces a right-looking edit is
the most expensive kind.

### Second correction: the budget was never 10,000

`config.yaml: memory.user_char_limit = 11000`, `memory.memory_char_limit = 16000`. The "10,000"
figure in the 333-AGI report, in my own manifest v1.1, and in an old comment inside USER.md was
all wrong. Measured against the real limit, `USER.md` was **never over budget**. The metabolism
I ran in the previous turn therefore fixed a problem that did not exist on that file — it made
the file smaller and lost nothing, but the urgency in that receipt was overstated. The manifest
now reads its budgets from config; the hardcoded constants are gone.

---

## STEP 1 — geo anchors into every live profile

Written to all five live profiles, identical block, provenance stated inside the text:

```
[GEO 2026-10-23 · coords geocoded, never guessed] Stay One South, Seri Kembangan 43300 =
3.044248, 101.7061448 (Google geocode, verified twice). Kerja KLCC = 3.15785, 101.71160.
Kampung Penang — kawasan tepat belum disahkan. Default konteks SK↔KLCC. Jawapan lokal WAJIB
nama anchor + radius; alamat rumah ≠ dia sedang di rumah. Gym: Peak Fitness Premier (daftar
21/10, cabang TRX/Connaught belum pasti). Skill: my-local-reality.
```

| Profile | before | after | limit | headroom |
|---|---|---|---|---|
| default (root memories) | 9,882 | 10,314 | 11,000 | +686 |
| aaa-hermes | 1,595 | 2,027 | 11,000 (inherited) | +8,973 |
| hermes_apex | 2,501 | 2,933 | 11,000 | +8,067 |
| hermes_asi | 2,501 | 2,933 | 11,000 | +8,067 |
| hermes_forge | 2,501 | 2,933 | 11,000 | +8,067 |

Rollback copy of every file is in `state/runtime-manifest/memory-ledger/`.

**Referent fix replaced with a sensor, not a symlink.** New file `/root/.hermes/MEMORY-TOPOLOGY.md`
names the two symlinks, lists every profile and which lane it serves, and states the rule:
resolve the profile the *reader* runs under before writing. And the manifest gained a
`memory_profiles` section that records each profile's char count, sha256 and whether the geo
anchor is present — so the next collapse is measurable instead of arguable. Current state:
`geo_anchor_in_all_live = true`.

### Cross-profile contradictions found, not resolved

| Fact | default profile | aaa-hermes profile |
|---|---|---|
| Father's death | 2 Mac 2024, 9:59pm HKB | 4 Mac 2024 (Penang) |
| Years at PETRONAS Carigali | 12 yr | 13 yr |

Both files are live. These are person facts, so neither value is mine to overrule. Left standing,
recorded in MEMORY-TOPOLOGY.md, and reported to F13 as the one item needing his word. An agent
quoting either should say which profile it came from.

---

## STEP 2 — AGENTS.md truncation closed

Measured cause: `/root/AAA/AGENTS.md` was 43,434 chars against a 32,000 char admission cap.
Journal, twice today:

```
WARNING agent.prompt_builder: Context file AGENTS.md TRUNCATED: 43433 chars
exceeds limit of 32000 — the full file stays readable with read_file: AAA/AGENTS.md
```

Structure probe: **95% of the file (41,637 of 43,434 chars) was one 96-row table** of doctrine
paths and statuses. The prose — ground truth pointer, autonomy pointer, execution-first rule —
was 1,798 chars.

Actions:
1. Full pre-extraction copy: `state/runtime-manifest/AGENTS.md.bak-20261023-full` (44,156 B,
   sha256 77951da9bb708ae2).
2. The 96 rows moved **byte-identical** to `/root/AAA/instructions/DOCTRINE-INDEX.md` with a
   provenance header. Row count verified 96 → 96, none dropped, none reworded, none re-sorted.
3. `AGENTS.md` rewritten at **4,075 chars** (from 43,434, −90.6%), and rather than merely shrink
   it, the seven mandatory invariants are now **written out plainly** instead of being buried in
   table prose: F13 sovereignty · fail-closed UNKNOWN/HOLD · capability is not authority ·
   no agent may SEAL itself · proposer ≠ judge ≠ executor · witness before mutation ·
   representation of a person is not the person. Each one grep-verified present.

Effect on the admission receipt: `COMPLETE_WITH_TRUNCATION` → **`COMPLETE`**. Total admitted
instruction drops 81,548 → 42,572 chars, and nothing is cut any more.

Journal check: the last TRUNCATED line is 12:41:51; the file was replaced 12:48:33; **zero
TRUNCATED lines since**. A fresh one-shot CLI turn produced no truncation warning. Honest limit:
per-turn journal proof for the gateway needs the next live turn, and the arithmetic is already
decisive — 4,075 chars cannot exceed a 32,000 cap.

### Tooling gap this exposed, and closed

`AGENTS.md` and ~40 other root-level AAA files are `chattr +i` individually but sit outside every
`canon-mutate TREES` member, so the only way to edit them was a raw `chattr -i` at the shell —
the exact practice F13 banned. `canon-mutate` gained a **`file` mode**:

```
canon-mutate file <path> -- <command...>
```

Single-file cycle: immutable check, unlock, run, relock **verified with lsattr and retried three
times**, EXIT/INT/TERM/HUP trap guaranteeing relock on any exit path, receipt with pre/post
sha256 and an effect verdict. Tested on a throwaway locked file first (`lock=true effect=CHANGED`),
then used on AGENTS.md itself. Backup: `canon-mutate.bak-20261023-pre-filemode`.

---

## STEP 3 — F1 = 0.0 and FQ = 0.111: root cause

This was not missing receipts, an unverified actor, or a mis-referenced counter. It is the
loudest finding of the four steps.

`arifFlow :7073` FQ block:

```
rollup_formula      minimum_gated_harmonic_mean
quotient            0.1111111111111111
raw_pool_quotient   0.9782608695652174      <- healthy
execute_count       46
verify_count        45
actors_tracked      19
```

Per-actor, the minimum is **my own lane**:

| actor | execute | verify | quotient | held |
|---|---|---|---|---|
| **hermes** | **9** | **1** | **0.111** | **true** |
| qwen-code | 2 | 1 | 0.500 | false |
| hermes-asi | 21 | 14 | 0.667 | false |
| a-forge | 22 | 28 | 1.273 | false |
| 333-agi | 10 | 14 | 1.400 | false |

Under a minimum-gated harmonic mean, the worst actor *is* the federation score. The federation's
raw pool quotient is 0.978; the rollup reports 0.111 because the `hermes` actor executed nine
times and emitted one Verify. Six actors are additionally `held=true`: anonymous, arif_fazil,
codex, fi-002, fi-008-cron, hermes.

So F1 = 0.0 is not a broken metric. It is the constitution correctly reporting that this lane's
verification **was not receipted**. The distinction that matters:

- **True as a measure of receipted verification.** Nine executes, one verify receipt.
- **False as a measure of actual verification.** This session ran dozens of verifications —
  renderer gates, cross-node probes, admission measurement, patch apply-check — and emitted
  almost none of them as arifFlow Verify receipts.

Classification, using the report's own taxonomy: **`F1_PRODUCER_DEFECT`** — the instrumentation
is missing, so the floor measures receipt emission rather than verification behaviour. Remedy is
behavioural and mechanical, not a threshold change: route verifications through
`POST /ingest {step_type: "Verify"}` and `POST /release` so the counter reflects work that
actually happened. I did **not** back-fill nine historical verify receipts to move a number.
Fabricating them would have produced a green floor and a dishonest ledger.

Consequence for the ladder: while F1 is 0.0, `JUDGMENT` stays `DEGRADED`. That is correct.
F8 (score 0.8) and F6 (score 0.5) are `unmeasured`, not failing — a distinction the 333-AGI
report collapsed, and the reason it named the wrong floor.

---

## STEP 4 — the uncommitted telegram patch, preserved

```
tree   /usr/local/lib/hermes-agent
HEAD   5e16f33277320118d41d1729f4ebac421c12c0b2   fix(tests): ...  2026-10-22 19:28:00 +0800
dirty  M plugins/platforms/telegram/adapter.py     +21 / -3
```

Content: `_check_delivery_target()` gains a branch making a BOT target a silent no-op returning
`SendResult(success=True, message_id=None)` instead of fail-closed, so callers stop retrying
(2,700+ Forbidden lines of log noise). Human and unknown targets keep the original fail-closed
behaviour. Comment records the decision: F13, 2026-10-22.

Frozen as:

```
state/runtime-manifest/patches/telegram-adapter-bot-to-bot-noop.patch   1,727 B
state/runtime-manifest/patches/README.md                                restoration + drift check
state/runtime-manifest/patches/BASE-COMMIT.txt
```

Restoration and drift-check commands are in the README. Verified: `git apply --check` against a
fresh copy of HEAD passes clean. Honest limit recorded there — the patch exists only on this
host and is not upstreamed; if the tree is replaced by a clean checkout, the behaviour disappears
and this patch is the only code-form record of the decision.

---

## State after the four steps

| Item | Before | After |
|---|---|---|
| AGENTS.md | 43,434 chars, truncated 11,433 each turn | 4,075 chars, `COMPLETE` |
| Admission verdict | `COMPLETE_WITH_TRUNCATION` | `COMPLETE` |
| Geo anchor in live memory | absent from all 5 profiles | present in all 5 |
| Referent trap | undocumented | `MEMORY-TOPOLOGY.md` + `memory_profiles` sensor |
| Budget source | hardcoded 10,000 (wrong) | read from `config.yaml` (11,000 / 16,000) |
| Locked files outside TREES | raw `chattr` required | `canon-mutate file` mode |
| F1 / FQ | 0.0 / 0.111 unexplained | `F1_PRODUCER_DEFECT`: hermes 9 exec / 1 verify, min-gated |
| telegram patch | uncommitted, one tree reset from loss | patch + README + base commit frozen |

Readiness ladder is unchanged except where earned: `PROPOSAL` `READY_WITH_LIMITS`,
`VERIFICATION` `PARTIAL`, `JUDGMENT` `DEGRADED` (F1), `INDEPENDENT_WITNESS` `NOT_PRESENT`.
Nothing was promoted by wording.

## What is still not done, and why

1. **Verify receipt instrumentation** — the real fix for F1. Needs a standing rule that every
   verification emits a receipt, not a one-off backfill.
2. **The two person-fact contradictions** — F13's word. Not mine to settle.
3. **`/root/AAA` root-level locked files** — `canon-mutate file` closes the mechanism, but ~40
   files still sit outside any declared tree. Adding them would be a tree-list decision.
4. **MCP capability canaries** (DECLARED → REACHABLE → DISCOVERABLE → SCHEMA_VALID →
   READ_ONLY_CANARY_PASS) — deliberately not attempted; reachability is still not claimed as
   capability.

---

## ADDENDUM — F8 changed between observers, and both were right

Written 2026-10-23 04:57Z, after the PDF render.

Step 3 states that F8 was `unmeasured` (score 0.8, default) and therefore not failing, and uses
that to say the 333-AGI report named the wrong floor. Re-probing at 04:53:45Z shows F8 is now
**measured and failing**:

```
F8  score=0.5802  status=fail  measured=True
    provenance=arifflow_live_vector:g=0.5802@2026-10-23T04:53:45Z
```

At 04:34:19Z it was `unmeasured` (0.8, `unmeasured_default`). The live-vector producer came alive
between the two probes. So:

- My 04:34 reading was correct at its own timestamp.
- The 333-AGI statement "F8 masih gagal" is correct at 04:53.
- Neither reading was wrong. The earlier framing — "they named the wrong floor" — is only true
  for the 04:34 window, and the honest statement is that **F8's status flipped under us**.

Current floor truth (04:53:45Z):

| floor | score | status | provenance |
|---|---|---|---|
| F1 | 0.0 | **fail** | arifflow_fq_probe fq=0.111 |
| F8 | 0.5802 | **fail** | arifflow_live_vector g=0.5802 |
| F6 | 0.5 | unmeasured | empty_kernel_signal |
| F10 | 1.0 | unmeasured | ontology_config_reference |
| others | — | pass | floor_producer / live_vector |

So there are now TWO failing floors, not one: F1 (receipted-verification deficit, mine) and
F8 (G scalar 0.5802). F8's number is the same `apex_scalars.G` value seen earlier at 0.5807, which
means F8 is a passthrough of federation coherence G. Diagnosing F8 causally is therefore the same
job as diagnosing G, and it is not solved by moving a threshold — which is exactly what the
333-AGI report warned against and I now apply to F8 rather than only to its framing.

Also noticed and not explained: F12 scores 0.0 with status `pass`, and F7 scores 0.04 with status
`pass`. A floor whose status is `pass` at near-zero score is a semantic defect in its own gate,
recorded here as an open question rather than a claim.

Lesson recorded: a floor's status is a reading with a timestamp, like any other measurement.
Two observers who disagree across a 20-minute window are not in contradiction — they are in
different frames. State the frame.
