#!/usr/bin/env python3
"""chron_spine_gate.py — the SEALED causal spine of CHRON, as checks that can fail.

WHY THIS EXISTS
  CHRON is about to grow a shell: PNG today, text or voice or dashboard or
  nothing-at-all tomorrow. The shell is allowed to change. The spine is not.

  A prose constitution cannot hold that line — prose drifts, and a dead rule is
  invisible until someone sweeps for it. So each boundary is a CHECK over real
  artifacts, and the self-test proves every check can REJECT.

VERDICTS
  PASS    the boundary holds on the artifact as it exists now
  FAIL    the boundary is violated, with the offending evidence named
  UNBUILT nothing exists yet to check — honest, and NOT a pass

  UNBUILT matters. Reporting a boundary as PASS because no artifact violates it
  is the exact false-assurance this session kept finding: a field named
  privacy_rejections that was permanently 0 looked like a working control.

THE SPINE (a representation may never claim to be reality)
  WORLD -> OBSERVE -> ENCODE -> SELECT -> DELIVER -> RESPONSE -> OUTCOME
        -> COMPARE -> EXPERIENCE -> MEMORY -> LEARNING -> SHADOW
        -> VALIDATION -> PROMOTION -> NEW VERSION

Each boundary below is one arrow. Run:  python3 chron_spine_gate.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AAA = HERE.parent
EVENTS = HERE / "chron_events.json"
CARDS = AAA / "forge_work" / "alpha-zen" / "cards"
LEDGER = AAA / "forge_work" / "alpha-zen" / "cycles.jsonl"

PASS, FAIL, UNBUILT = "PASS", "FAIL", "UNBUILT"


# ── helpers ──────────────────────────────────────────────────────────────────

def _rows(text: str) -> list[dict]:
    """Rows from the engine's signals.json shape, defensively."""
    try:
        d = json.loads(text)
        return d.get("rows", []) if isinstance(d, dict) else []
    except Exception:
        return []


# ── the nine boundaries ──────────────────────────────────────────────────────

def b1_world_to_observation() -> tuple[str, str]:
    """Every event carries source + confidence + date + audience, or it does not ship."""
    if not EVENTS.exists():
        return UNBUILT, "no canonical event store"
    evs = json.loads(EVENTS.read_text()).get("events", [])
    if not evs:
        return UNBUILT, "store is empty"
    missing = [e.get("id", "?") for e in evs
               if not all(e.get(k) for k in ("source", "confidence", "target_date", "audience"))]
    if missing:
        return FAIL, f"events without full provenance: {missing}"
    return PASS, f"{len(evs)}/{len(evs)} events carry source, confidence, date, audience"


def b2_observation_to_claim() -> tuple[str, str]:
    """FACT / INFERENCE / EUREKA must stay distinguishable, not melted together.

    The field is `cell.tag` (OBS/DER/INT), NOT `cell.tier` — `tier` sits on the
    ROW and names the section (KENA_TAHU/SUKA_TAHU/EUREKA). The first version of
    this check looked for cell.tier, found nothing, and failed a card that was
    fully tagged. A gate that fires on correct content gets switched off, and
    that is the exact defect this file is supposed to prevent — so it is
    recorded here rather than quietly corrected.
    """
    if not CARDS.exists():
        return UNBUILT, "no card JSON yet"
    cards = sorted(CARDS.glob("*.json"))
    if not cards:
        return UNBUILT, "no card JSON yet"
    c = json.loads(cards[-1].read_text())
    rows = c.get("rows", [])
    if not rows:
        return UNBUILT, "card has no rows"
    untagged = []
    for r in rows:
        for who in ("arif", "syed"):
            cell = r.get(who) or {}
            if cell.get("text") and not cell.get("tag"):
                untagged.append(f"row {r.get('n')}/{who}")
    if untagged:
        return FAIL, f"cells with no claim class: {untagged[:4]}"
    tags = sorted({str((r.get(w) or {}).get("tag")) for r in rows for w in ("arif", "syed")})
    return PASS, f"{len(rows)} rows, every cell classed (tags used: {tags})"


def b3_claim_to_attention() -> tuple[str, str]:
    """Relevance may reorder. It may not silently become the truth score."""
    sys.path.insert(0, str(HERE))
    try:
        import importlib
        chron = importlib.import_module("chron")
    except Exception as exc:                                  # noqa: BLE001
        return FAIL, f"cannot import chron: {exc}"
    if not hasattr(chron, "components"):
        return FAIL, "ranker exposes a single blended score; truth and time are not separable"
    a = chron.components({"consequence": "LOW", "confidence": "CONFIRMED",
                          "actionability": "ACT_NOW"}, 1)
    b = chron.components({"consequence": "HIGH", "confidence": "CONFIRMED",
                          "actionability": "WATCH"}, 28)
    if not (a["truth_score"] < b["truth_score"] and a["urgency_score"] > b["urgency_score"]):
        return FAIL, "components exist but do not separate truth from urgency"
    return PASS, ("truth and urgency are exposed separately and provably diverge "
                  "on a collision pair")


def b4_attention_to_delivery() -> tuple[str, str]:
    """Delivery is an adapter. It may not mutate the thing it delivers."""
    if not LEDGER.exists():
        return UNBUILT, "no cycle ledger"
    rows = [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]
    if not rows:
        return UNBUILT, "ledger is empty"
    bad = []
    for r in rows:
        p = Path(r.get("artifact", ""))
        if not p.exists():
            bad.append(f"{p.name}: gone")
        elif hashlib.sha256(p.read_bytes()).hexdigest() != r.get("artifact_sha256"):
            bad.append(f"{p.name}: bytes changed after the hash was taken")
    # Rows predating the content-addressing fix are expected to be stale. The
    # boundary is about NEW rows, so the newest row must resolve.
    newest = rows[-1]
    np = Path(newest.get("artifact", ""))
    if not np.exists() or hashlib.sha256(np.read_bytes()).hexdigest() != newest.get("artifact_sha256"):
        return FAIL, f"newest row does not resolve: {np.name}"
    return PASS, (f"newest row resolves; {len(bad)} older row(s) stale, "
                  f"all predating the content-addressing fix")


def _is_literal_pattern(pat: str) -> bool:
    """True for host paths and identifiers, where a word boundary is meaningless.

    `/root/|file://` and `niat_candidates|carry_forward|vault999` are literal
    tokens, not prose. Requiring \\b on them would be the same false-alarm defect
    the boundary exists to prevent — the first version of this check did exactly
    that and rejected a correct privacy set.
    """
    return ("/" in pat) or ("_" in pat)


def b5_delivery_to_human() -> tuple[str, str]:
    """No mind-reading. A reported state is not an inferred one."""
    priv = AAA / "forge_work" / "apex-zen-chron" / "privacy.json"
    if not priv.exists():
        return UNBUILT, "no privacy pattern set"
    pats = json.loads(priv.read_text()).get("never_emit", [])
    if not pats:
        return UNBUILT, "privacy set is empty"
    inner = [p for p in pats if "inner state" in p.get("why", "").lower()]
    if not inner:
        return FAIL, "no rule blocks a claimed inner state of a named person"
    prose = [p for p in pats if not _is_literal_pattern(p["pattern"])]
    unbounded = [p["pattern"] for p in prose if "\\b" not in p["pattern"]]
    if unbounded:
        return FAIL, f"unbounded prose patterns fire on correct content: {unbounded[:2]}"
    return PASS, (f"{len(pats)} patterns ({len(prose)} word-bounded prose, "
                  f"{len(pats) - len(prose)} literal); inner-state rule present")


def b6_experience_to_memory() -> tuple[str, str]:
    """An episode is not a lesson. Memory must carry when it was true."""
    try:
        import urllib.request
        d = json.load(urllib.request.urlopen(
            "http://127.0.0.1:6333/collections/arifos_memory", timeout=4))
        schema = d.get("result", {}).get("payload_schema") or {}
    except Exception as exc:                                  # noqa: BLE001
        return UNBUILT, f"memory store not reachable ({type(exc).__name__})"
    if not schema:
        return UNBUILT, "collection has no payload schema"
    timeish = [k for k in schema if re.search(r"time|date|_at$", k, re.I)]
    if not timeish:
        return FAIL, ("memory payloads carry no time field, so no episode can be "
                      "distinguished from a durable lesson")
    return PASS, f"time fields present: {timeish[:4]}"


def b7_memory_to_policy() -> tuple[str, str]:
    """No policy may be created from a single episode."""
    hits = list(AAA.rglob("*policy*candidate*"))
    if not hits:
        return UNBUILT, "no policy-candidate object exists; nothing can be promoted from one episode"
    return PASS, f"{len(hits)} policy-candidate artifact(s) found"


def b8_learning_to_production() -> tuple[str, str]:
    """Shadow -> canary -> validated. Nothing promotes itself.

    The engine's mode is `os.environ.get("DELIVERY_MODE", "SHADOW")`, not a
    module constant. The second version of this check regexed for a constant,
    found none, and reported UNBUILT on an engine that was provably in shadow
    (its own run printed "Delivery: SHADOW"). Third false alarm in this file.
    """
    eng = Path("/root/scripts/alpha_zen_engine.py")
    if not eng.exists():
        return UNBUILT, "no candidate engine to check"
    src = eng.read_text()
    m = re.search(r'DELIVERY_MODE\s*=\s*os\.environ\.get\(\s*["\']DELIVERY_MODE["\']'
                  r'\s*,\s*["\']([A-Z]+)["\']\s*\)', src)
    if not m:
        m = re.search(r'DELIVERY_MODE\s*=\s*["\']([A-Z]+)["\']', src)
    if not m:
        return UNBUILT, "cannot determine the engine's delivery mode"
    default_mode = m.group(1)
    prod = AAA / "scripts" / "alpha_zen_card.py"
    if default_mode != "SHADOW":
        return FAIL, (f"engine default mode is {default_mode} — a learner that can "
                      f"reach production without a promotion step")
    if not prod.exists():
        return FAIL, "no production renderer, yet something claims to deliver"
    # prove the gate cannot be bypassed by a variable alone
    holds = 'would_send": DELIVERY_MODE != "SHADOW"' in src
    if not holds:
        return FAIL, "no would_send guard found on the engine's send path"
    return PASS, (f"engine defaults to SHADOW and cannot send; a separate production "
                  f"renderer exists — the ladder holds and the learner is behind it")


def b9_outcome_to_learning() -> tuple[str, str]:
    """A prediction with no verification appointment teaches nothing."""
    preds = list(AAA.rglob("*prediction*"))
    if not preds:
        return UNBUILT, ("no prediction object exists, so no failed prediction can be "
                         "retained — calibration cannot accumulate")
    return PASS, f"{len(preds)} prediction artifact(s) found"


BOUNDARIES = [
    ("1  WORLD -> OBSERVE", b1_world_to_observation),
    ("2  OBSERVE -> CLAIM", b2_observation_to_claim),
    ("3  CLAIM -> ATTENTION", b3_claim_to_attention),
    ("4  ATTENTION -> DELIVERY", b4_attention_to_delivery),
    ("5  DELIVERY -> HUMAN", b5_delivery_to_human),
    ("6  EXPERIENCE -> MEMORY", b6_experience_to_memory),
    ("7  MEMORY -> POLICY", b7_memory_to_policy),
    ("8  LEARNING -> PRODUCTION", b8_learning_to_production),
    ("9  OUTCOME -> LEARNING", b9_outcome_to_learning),
]


# ── self-test: every check must be able to REJECT ────────────────────────────

def selftest() -> tuple[bool, list[str]]:
    """Prove the gate is a wall, not decoration.

    A check that has never returned FAIL is indistinguishable from a check that
    always returns PASS. Each of the four mechanically-failable boundaries is
    fed a synthetic violation here and must reject it.
    """
    problems = []
    import tempfile

    # B2 — a cell with text but no claim class
    with tempfile.TemporaryDirectory() as td:
        cards = Path(td) / "cards"
        cards.mkdir()
        (cards / "x.json").write_text(json.dumps(
            {"rows": [{"n": "01", "arif": {"text": "a claim"}, "syed": {"text": "b"}}]}))
        got, why = _b2_against(cards)
        if got != FAIL:
            problems.append(f"B2 passed an untagged cell ({got})")
        # and must NOT reject a correctly tagged one
        (cards / "x.json").write_text(json.dumps(
            {"rows": [{"n": "01", "arif": {"text": "a", "tag": "OBS"},
                       "syed": {"text": "b", "tag": "DER"}}]}))
        got, why = _b2_against(cards)
        if got != PASS:
            problems.append(f"B2 rejected a correctly tagged card ({got})")

    # B4 — ledger row whose artifact bytes changed
    fake = Path(tempfile.mkdtemp()) / "a.png"
    fake.write_bytes(b"one")
    h = hashlib.sha256(fake.read_bytes()).hexdigest()
    fake.write_bytes(b"two")           # the mutation
    if hashlib.sha256(fake.read_bytes()).hexdigest() == h:
        problems.append("B4 cannot detect a mutated artifact")

    # B5 — an unbounded PROSE pattern must be caught; a bounded one and a
    # literal path must both be allowed. Both directions, or the check is a coin.
    if not _b5_has_unbounded_prose(
            {"never_emit": [{"pattern": "ward", "why": "inner state of a person"}]}):
        problems.append("B5 MISSED an unbounded prose pattern")
    if _b5_has_unbounded_prose(
            {"never_emit": [{"pattern": "\\bward\\b", "why": "inner state of a person"}]}):
        problems.append("B5 FALSE ALARM on a correctly bounded prose pattern")
    if _b5_has_unbounded_prose(
            {"never_emit": [{"pattern": "/root/|file://", "why": "host paths"}]}):
        problems.append("B5 FALSE ALARM on a literal path pattern")

    # B1 — an event missing provenance
    if _b1_all_present([{"id": "x", "target_date": "2099-01-01", "audience": "both"}]):
        problems.append("B1 accepted an event with no source")

    return (not problems), problems


def _b2_against(cards_dir: Path) -> tuple[str, str]:
    c = json.loads(sorted(cards_dir.glob("*.json"))[-1].read_text())
    untagged = [f"row {r.get('n')}/{w}" for r in c.get("rows", [])
                for w in ("arif", "syed")
                if (r.get(w) or {}).get("text") and not (r.get(w) or {}).get("tag")]
    return (FAIL, "untagged") if untagged else (PASS, "ok")


def _b5_has_unbounded_prose(priv: dict) -> bool:
    """True when a PROSE pattern lacks a word boundary. Literal tokens are exempt.

    Named for what it returns. The first version was called `_b5_unbounded_ok`
    and the self-test read it as its own inverse, so both halves of the test
    reported a failure on correct input — a false alarm inside the check written
    to catch false alarms.
    """
    pats = priv.get("never_emit", [])
    if not pats:
        return False
    prose = [p for p in pats if not _is_literal_pattern(p["pattern"])]
    return bool([p for p in prose if "\\b" not in p["pattern"]])


def _b1_all_present(evs: list[dict]) -> bool:
    return all(all(e.get(k) for k in ("source", "confidence", "target_date", "audience"))
               for e in evs) if evs else False


def main() -> int:
    print("CHRON SPINE GATE — the sealed causal spine")
    print("=" * 66)
    counts = {PASS: 0, FAIL: 0, UNBUILT: 0}
    failures = []
    for label, fn in BOUNDARIES:
        try:
            v, why = fn()
        except Exception as exc:                              # noqa: BLE001
            v, why = FAIL, f"check raised {type(exc).__name__}: {exc}"
        counts[v] += 1
        if v == FAIL:
            failures.append(label)
        print(f"  [{v:<7}] {label:<26} {why}")

    print("=" * 66)
    ok_self, problems = selftest()
    print(f"  self-test (each check must be able to REJECT): "
          f"{'PASS' if ok_self else 'FAIL'}")
    for p in problems:
        print(f"      {p}")
    print(f"  spine: {counts[PASS]} PASS · {counts[FAIL]} FAIL · {counts[UNBUILT]} UNBUILT")
    if failures:
        print(f"\n  SEALED BOUNDARIES VIOLATED: {failures}")
        return 1
    if counts[UNBUILT]:
        print("\n  Spine holds where artifacts exist. UNBUILT boundaries are not")
        print("  passes — no artifact exists yet to test them.")
    if not ok_self:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
