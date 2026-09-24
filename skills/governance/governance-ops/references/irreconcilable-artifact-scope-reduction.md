<!-- governance-ops merge provenance — added 2026-09-24 -->
<!--
Workflow extension for artifacts that are TOO ENTANGLED with ratified-stance
conflict for the §9 four-outcome triage alone. Pairs with §9 and §8 (gate
direction); adds M12 "scope-reduce + stage sub-eurekas for sovereign review".
-->
---

# Irreconcilable artifact — scope-reduce and stage, do not seal wholesale

When the sovereign hands over an artifact that mixes real sub-eurekas with
sealed-stance conflicts (a self-ratifying "seal all" file whose capabilities
contradict ratified canon in the same session), the §9 four-outcome triage
is necessary but not sufficient. A fifth outcome is needed: **SCOPE-REDUCE
+ STAGE** — separate the evidence-grade sub-eurekas, drop or reframe the
rest, and stage the salvageable pieces under a workspace path the sovereign
can read and seal explicitly.

## The trigger — when scope-reduction applies

§9's four outcomes work when each item is independently auditable. They
break when:

1. The artifact **self-ratifies** — claims `SEALED`/`ALIVE`/`verified` in its
   own header despite contradicting F13-ratified canon in its claims.
2. The artifact **bundles** — wraps real sub-eurekas (evidence-grade, peer-
   reviewed sources, falsifiable claims) together with capabilities that
   contradict the Section 5 / Capability≠Authority / Identity ratification
   lineage. Wholesale acceptance seals the conflicts; wholesale rejection
   drops the salvageable sub-eurekas.
3. The artifact's **scope > available scope under the live canon** — a 9-
   item artifact where 5 items require constitutional-class ratification
   (which only F13 "SAH" can grant) and 4 are workspace-grade distillations.

In all three cases, the right move is **not** to seal the file as written,
and **not** to reject it whole.

## The workflow

```
1. PROBE — run §0 (symbol probe), §1 (citation check), §5 (duplicate owner),
   §8 (gate direction). Note what fails. (Existing §0–§9 work, unchanged.)

2. PARTITION — separate the artifact's items into three buckets:
   • SALVAGE  — evidence-grade, no sealed-stance conflict, fits in a
                 workspace-distillation note (≤ ~3k EPA each)
   • REFRAME  — mechanism or framing is real, but the surface artifact
                 contradicts canon (e.g., "Agentic Sexual Intelligence" as
                 capability when Section 5 v2 holds H1–H4 immutable).
                 Reframe = re-label to a non-colliding concept; cite
                 what was reframed and why.
   • DROP     — claim contradicts ratified canon, or source does not
                 verify, or item lies outside agent write scope (3rd-party
                 privacy, named-real-person content, consent artifacts).

3. STAGE the SALVAGE bucket as DISTILLATION_DRAFT files in:
       /root/.hermes/workspace/distillations-YYYY-MM-DD/
   NOT in:
       /root/AAA/canon/         — immutable (chattr +i); direct write
                                   returns EPERM by design
       /root/AAA/instructions/  — requires Status: line at create time
                                   and triggers doctrine-status gate
       /root/AAA/eurekas/       — LIVE FEED for ratified eurekas, not
                                   drafts
   Each staged file MUST carry in its frontmatter:
       status: DISTILLATION_DRAFT (not F13 ratified)
   so a future loader cannot mistake it for canonical artifact.

4. SHA-256 the staged files and report the partition in the response:
   "N salvaged → /path/to/file (sha256 prefix)
    M reframed → <concept>: <original> → <corrected>
    K dropped  → <reason class>"

5. HOLD constitutional-class items. The sovereign ratifies with "SAH" or
   re-directs; the agent does not promote workspace drafts to canon.

## Pitfalls

**Reporting "I distilled the 9 eurekas" without naming the dropped is a
false-receipt shape.** The partition must be visible: which items landed,
which reframed, which dropped, on what evidence. A report that names only
the adopted items reads as endorsement of the whole artifact.

**Workspace path ≠ canonical path.** A file under
`/root/.hermes/workspace/distillations-.../` is sovereign-readable staging,
not ratified canon. Agents must never auto-load or cite such a path as
authority; future loaders must not mistake DISTILLATION_DRAFT frontmatter
for F13_RATIFIED status.

**`/root/AAA/canon/` returns EPERM by design.** That failure is the lock
working, not a bug. Do not clear the immutable attribute to bypass — that
is an unauthorized bypass. The workflow's path (workspace staging) is the
lock's intended partner: drafts go to workspace; canon-mutate is the only
legal path for ratified writes.

**DISTILLATION_DRAFT is not a new status label in the ratified canon
status vocabulary.** It is a workspace-only marker so sovereigns reading
the file know it has not been constitutionally promoted. Do not use it on
fragments under `/root/AAA/instructions/` — those carry the formal
`Status: DRAFT_*` / `PENDING_*` / `F13_*` labels and pass through the
doctrine-status gate.

## When to use §9 alone vs §9 + scope-reduction

| Artifact shape | Workflow |
|---|---|
| Each item independently auditable, no constitutional conflicts | §9 four-outcome triage only |
| Items entangled with sealed-stance conflicts; some salvageable | §9 + this scope-reduction |
| Entire artifact contradicts ratified canon in its premise | §9; DROP all; report why |
| Artifact's claims are unverifiable (no sources, fabrication layer) | §9; HOLD; flag for sovereign |

## Why this is not in §9

§9 lists four outcomes for items, all keyed to a single artifact's
proposed items. Scope-reduction is a *meta-workflow* — it operates on the
artifact as a whole when the §9 outcomes, applied item-by-item, would
either seal the conflicts with the salvage or drop the salvage with the
conflicts. It is the workflow for the case where the artifact is too
entangled for per-item triage to be honest.

The partition into SALVAGE / REFRAME / DROP is also the durable record: a
future session that loads the workspace draft reads the reframe/drop log
and cannot re-import the conflicts as if they were sealed.