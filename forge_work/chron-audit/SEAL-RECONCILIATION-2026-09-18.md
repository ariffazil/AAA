# SEAL RECONCILIATION — CHRON — 2026-09-18

**Type:** RECONCILIATION (append-only supersedes record, **not** a SEAL)
**Lane:** B · **F13-ratified:** NO · **Authority:** none beyond lane-B receipt grade
**Host:** forge (KVM8) · **Written:** 2026-09-18T11:43+08:00
**Machine record:** `SEAL-RECONCILIATION-2026-09-18.json` (same directory)

> A seal is a claim about a state of the world at a moment in time. When the world
> moves, the seal does not become a lie — it becomes **STALE**, and that transition
> must be RECORDED, never erased. Nothing in this directory was edited.

---

## 1. What this reconciles

Two seals were written over the CHRON work under one F13 chat instruction
("forge to seal this meaning fix all u see as witness just now"):

| Seal | Declared created | File birth (fs) | Hash claims |
|---|---|---|---|
| `SEAL-CHRON-FORGERY-2026-09-18.json` | 10:58:42 | 10:58:19.94 | 5 full sha256 pairs |
| `SEAL-CHRON-SPINE-2026-09-18.json` | 11:20 | **11:03:14.96** | 4 pairs, **12-char truncated** |

15 attested hash values were re-derived from raw disk, `backup-105522/` and git.
Nothing was taken on trust from any summary — including the summary that briefed this record,
which was **wrong on two points** (see §5).

## 2. The damage — one file, two stale values

**`/root/scripts/alpha_zen_engine.py`** — nothing else.

| | value | | |
|---|---|---|---|
| FORGERY seal, `changes[1].sha256_after` | `f0b31aa62d54…` | disk | `a822850a37c1…` | **MISMATCH** |
| SPINE seal, `changes_this_pass[2].sha256_after` | `dc1420b0eb19` | disk | `a822850a37c1…` | **MISMATCH** |

Both sealed values were **real**. They are preserved in git, byte-for-byte:

```
git show eb16372:alpha_zen_engine.py | sha256sum  ->  017a1da0eb88…   (pre-forge, = backup-105522)
git show b8c600c:alpha_zen_engine.py | sha256sum  ->  f0b31aa6…      (= FORGERY seal sha256_after)
git show 133f692:alpha_zen_engine.py | sha256sum  ->  dc1420b0eb19…   (= SPINE seal sha256_after, and HEAD)
```

The file on disk today is `a822850a37c1…` — **uncommitted**, in no commit and no backup.

**Lineage:** `017a1da0 → f0b31aa6 → dc1420b0 → a822850a`

## 3. The cause, and who did it

**Cause: ESTABLISHED.** A 26-line `STATUS: DORMANT — NOT IN THE PRODUCTION PATH` banner was
inserted at the head of the engine at **11:18:52 MYT** — after both seals — and never committed.
(`git diff HEAD` = 26 insertions, 0 deletions. File Birth = Modify = 11:18:52.290/.305 → atomic
replace, not an append.)

**Responsible lane: PROVABLE.** The lane that authored
`/root/briefing-system/RECEIPT-2026-09-18-chron-engine-witness-fix.json`. Three independent proofs:

1. the banner text carries `receipt: rcpt-2026-09-18-chron-engine-witness-fix`;
2. the receipt self-attributes it — `causal_path_finding.doctrine_applied`: *"A DORMANT banner was added to the engine header…"*;
3. that receipt's `two_writer_collision.hash_reality.after_this_lane_wrote` = `a822850a37c13fcf` — exactly today's disk hash.

**Culpability: none asserted.** The edit is documented and substantively correct (the engine has zero
scheduled callers). The defect is not the edit — it is that the edit was **uncommitted** and
**unwitnessed by the two seals it invalidated**.

**Timeline**

```
10:38:37  engine on disk = 017a1da0 (mtime of backup-105522/alpha_zen_engine.py)
10:39:11  commit eb16372 lands 017a1da0
10:55:22  pre-forge backup taken into backup-105522/
10:56:37  sibling lane mutates the file (rejection-funnel fix in progress)
10:58:19  FORGERY seal file created
10:58:42  FORGERY seal declares sha256_after = f0b31aa6  -> TRUE of the tree at that moment
10:59:04  commit b8c600c lands f0b31aa6  -> the sealed state becomes durable
11:02:24  FIRST MOVEMENT — commit 133f692 lands dc1420b0  -> FORGERY seal STALE (3m42s later)
11:03:14  SPINE seal file created  (declared as 11:20 — see OPEN-1)
11:18:52  SECOND MOVEMENT — DORMANT banner inserted -> a822850a (uncommitted)
11:20:00  SPINE seal declared created_local  <- conflicts with fs birth 11:03:14
11:26:00  sibling lane re-hashes, finds a822850a
11:29:32  art-a822850a37c13fcf registered in claim_ledger
11:29:40  clm-47aab3359c209d17 records the same transition
11:30:30  BOTH seals amended with an identical append_only_corrections block
11:43:17  this reconciliation: still a822850a, still uncommitted
```

## 4. What is NOT damaged — 7 claims still valid

Do not let §2 cast doubt on the rest. **Seven** attested values still match disk exactly:

| File | Seal | Verdict |
|---|---|---|
| `/root/AAA/scripts/alpha_zen_card.py` | FORGERY `changes[0].sha256_after` | **MATCH** |
| `/root/AAA/scripts/cron_failure_autopause.py` | FORGERY `changes[2].sha256_after` | **MATCH** |
| `/root/AAA/registries/federated-recurrence.yaml` | FORGERY `changes[3].sha256_after` | **MATCH** |
| `/root/AAA/scripts/apex-zen-compact.py` | FORGERY `changes[4].sha256_after` | **MATCH** |
| `/root/AAA/scripts/chron.py` | SPINE `changes_this_pass[0]` | **MATCH** (= git HEAD) |
| `/root/AAA/scripts/chron_spine_gate.py` | SPINE `changes_this_pass[1]` | **MATCH** (= git HEAD) |
| `/root/AAA/scripts/alpha_zen_card.py` | SPINE `changes_this_pass[3]` | **MATCH** (declared no-op) |

**And all 8 historical `sha256_before` claims** resolve — 5 against `backup-105522/` and/or git,
3 against git alone. 8 of 8. Zero unverified.

**The production path is clean.** `/root/AAA/scripts/chron.py` and `/root/AAA/scripts/alpha_zen_card.py`
match both seals and are byte-exact at git HEAD `d1f97be` ("preserve(live-chron)"). The first natural
scheduled fire at 14:00 MYT is unaffected by anything in this record.

## 5. Two premises in the briefing were false — corrected

1. *"The SPINE seal attests no hashes at all."* — **FALSE.** It attests six **12-hex-char** values
   (`sha256_before`/`sha256_after` fields). Truncated, not absent. Different defect.
2. *"11:00:41 a second writer patched the same file."* — **UNVERIFIED.** No such event exists in git,
   mtimes or the receipt. 11:00:48 is the mtime of a *different* file (`/root/AAA/scripts/chron.py`).

## 6. A third-party claim refuted — in the forgery lane's favour

`RECEIPT-2026-09-18-chron-engine-witness-fix.json`, `two_writer_collision.finding`, asserts:
*"Neither hash on disk has ever matched the sibling's sealed hash. The sibling seal attests a state
that does not exist."*

**That is false, and git alone settles it.** The forgery seal's `f0b31aa6…` is the byte-exact content of
commit `b8c600c` (10:59:04). The state exists.

The error is a **stale-read inference** (`FINDING-B-1`): the receipt's own block records
`before_this_lane_wrote = dc1420b0` — by the time that lane looked, the file already held the *spine*
state. Both earlier values are invisible from a vantage point after 11:02:24. That is an artefact of
**when** the read happened, not evidence the earlier state never existed — the same class the receipt
correctly retracts elsewhere as SELF-1 (*asserting absence from a probe that could not have returned a hit*).

**Rule:** a hash mismatch licenses the inference *"not now"*, never *"never was"*.

## 7. THE SPINE SEAL — plain finding, not softened

**It is a seal of a DOCUMENT, not a seal of a state.**

- It seals the spine gate's own verdict set — nine boundaries, `6 PASS / 0 FAIL / 3 UNBUILT`, self-test PASS.
- Its four file entries are change-log entries, not verifiable bindings: one carries no defect at all,
  one is a declared no-op (`before == after`), one says `NEW`.
- `changes_this_pass[0/1].sha256_after` do match disk and git HEAD. So the file references are honest.

**Can it be verified? PARTIALLY — and not as a seal of state.**

- **Full sha256 values: 0. Truncated 12-char prefixes: 6.** All six were resolved this session and all
  six point at real content.
- But a 48-bit prefix is a **matchable** value, not a **verifying** one. Second-preimage resistance at
  48 bits is ≈2²⁴ (~1.7×10⁷) — constructible for anyone writing a mutable production file. The field is
  *named* `sha256_after` while storing something weaker. **That is a representation claiming to be more
  than it is — precisely the law this seal itself declares: "A representation may never claim to be
  reality itself."**
- Its engine value (`dc1420b0eb19`) describes no state the file holds today, and the file was never
  committed in the state it held when that seal was declared.

**What *is* sound and worth reading:** `self_reported_defects`. The seal records that its own self-test
caught three false alarms the author had written into the gate, and that they were recorded *inside the
file* rather than quietly deleted. Falsifiable, self-incriminating, genuinely useful. It is not a hash,
and it does not verify file state — but it is the best thing in either seal.

**Bottom line:** cite the spine seal for *which boundaries were checked, with which verdicts and what
evidence*. Do **not** cite it as proof that any file is what it was. A hash field that cannot verify plus
a count field that is scope-imprecise give a reviewer the *sensation* of verification without its substance.

## 8. Errata in existing records (recorded, not rewritten)

| ID | Where | Defect | Severity |
|---|---|---|---|
| ERR-1 | FORGERY `append_only_corrections.corrections[0].subject` | says `changes[2] alpha_zen_engine.py` — the engine is `changes[1]` in that seal. Correct for SPINE, where it *is* index 2. Both seals carry a byte-identical correction block, so it was copied without re-indexing. | LOW — pointer label |
| ERR-2 | FORGERY `…corrections[0].original` | `"dc1420b0eb19 (forgery seal: f0b31aa62d54)"` inverts the attribution: `f0b31aa6` is the forgery value, `dc1420b0` the spine value. | LOW — verifiable both ways |

## 9. What remains open

- **OPEN-1 — SPINE creation time conflict.** Declared `11:20` vs filesystem birth `11:03:14.955`.
  A 16m45s gap. It decides whether the spine engine hash was *true-then-stale* (as the forgery one was)
  or *stale-at-write*. **UNRESOLVED** — both observations recorded, neither privileged. Does not change
  the stale fact either way; it changes attribution of care.
- **OPEN-2** — `/root/scripts/alpha_zen_engine.py` is still uncommitted at `a822850a…`. One commit in
  `/root/scripts` would close it; that is a mutation outside this record's lane.
- **OPEN-3** — No seal or receipt names a single **enforced** owner for that file across 10:56–11:19.
  Three lanes, one file, one F13 instruction, no lock, no declared owner.
- **OPEN-4** — Ownership A/B/C remains unanswered by F13; `carry_forward e-3a377340`'s self-authored
  ratification does not self-bind. Carried forward, not adjudicated here.
- **OPEN-5** — `verified_not_broken` is behavioural and was **not re-executed** (the engine is dormant;
  running it could write artifacts). UNVERIFIED-BY-THIS-RECORD, not false.

One behavioural claim was spot-checked read-only: the seal's *"OD1=0 occurrences, 377=0 occurrences"*
does not hold as a literal substring count (7 and 2 today, in prose/comment/banner text) and did not
hold at 10:58 either — it is **scope-imprecise, not a failed fix**. Substantively, the
`privacy_filter: "OD1 arif-only"` literal and the hardcoded `{chrono["od1_days"]}` CHRON strip present
pre-fix are both gone from the committed state. Recorded so it is neither inherited blindly nor
counted as extra damage.

---

**This is a RECONCILIATION record, not a SEAL. Lane B. NOT F13-ratified.**
No existing seal, audit or receipt was edited, moved or deleted.
DITEMPA BUKAN DIBERI ⚒️
