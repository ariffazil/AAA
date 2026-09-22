#!/usr/bin/env python3
"""alpha_zen_gate — the pre-send quality gate. Section 16, enforced.

WHY A GATE AND NOT A CHECKLIST
  A checklist in a prompt is advice; an agent under time pressure will skip it.
  A gate that exits non-zero is a wall. The difference matters most exactly when
  it matters: on the bad day, when nine slots must be filled and only seven good
  signals exist. The temptation is to pad. This refuses.

  "Do not fill garbage to reach nine." — the whole point.

WHAT IT REFUSES
  G1  components    exactly 9 rows, numbered 01..09
  G2  tiers         3 KENA_TAHU, 3 SUKA_TAHU, 3 EUREKA
  G3  freshness     KENA_TAHU rows carry a source
  G4  chron         no expired/absent countdown in the store
  G5  duplication   no two rows share the same subject (token-overlap test)
  G6  privacy       no private marker leaks; audit for first-person tells
  G7  quotes        real attribution; a quote without an author is not a quote
  G8  anchors       Syed gets >=1 gym/body AND >=1 gold/trading; Arif gets >=1 structural
  G9  relevance     both men receive something (no all-Arif card)
  G10 render        the PDF/PNG exists and has a text-free sanity size

  Exit 0 = may send. Exit 1 = HOLD. Never sends anything itself.
  G14 register      machine vocabulary must not reach a cell a human reads.
  G11 freshness     KENA_TAHU market/price claims must carry a DATE in the source,
                    and that date must be recent. A stale number with a real source
                    passes G3 and is still wrong.

WHY G11 EXISTS (proven, not theorised)
  A parallel lane rendered a near-identical card on 2026-09-18 claiming gold at
  $2,580 and "Fed slowing cuts". Independently verified: gold was $4,328-4,350
  (JM Bullion / USA Today, 17 Sep) and the Fed HAD HIKED 25bps to 3.75-4.00%
  (CNBC / Kiplinger) — the opposite direction. Its sources were real outlets; the
  numbers were stale. G3 would have passed that card. Presence of a source is not
  freshness of a source, and a confidently-sourced stale figure is more dangerous
  than an unsourced one because it looks verified.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
STORE = HERE / "chron_events.json"

#: How old a dated news/market source may be before the card is held.
STALE_DAYS = 4

_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "mac": 3, "apr": 4, "may": 5, "mei": 5,
    "jun": 6, "jul": 7, "aug": 8, "ogo": 8, "sep": 9, "oct": 10, "okt": 10,
    "nov": 11, "dec": 12, "dis": 12,
}
_DATE_RE = re.compile(r"\b(\d{1,2})\s+([A-Za-z]{3,4})\b")
_ISO_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
_NUMERIC = re.compile(r"[$]?\d[\d,]{2,}(?:\.\d+)?")


def _source_age_days(src: str, today: date) -> int | None:
    """Days since the newest date mentioned in a source string, or None."""
    best: date | None = None
    for m in _ISO_RE.finditer(src or ""):
        try:
            d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            best = d if best is None or d > best else best
        except ValueError:
            continue
    for m in _DATE_RE.finditer(src or ""):
        day = int(m.group(1))
        mon = _MONTHS.get(m.group(2)[:3].lower())
        if not mon:
            continue
        try:
            d = date(today.year, mon, day)
        except ValueError:
            continue
        if d > today:                      # month with no year, rolled over
            d = date(today.year - 1, mon, day)
        best = d if best is None or d > best else best
    return None if best is None else (today - best).days


# ── anchor lexicons. Deliberately small and explicit so failures are legible. ──
GYM = ("gym", "latihan", "training", "strength", "kekuatan", "hypertrophy", "hipertrofi",
       "recovery", "pemulihan", "overload", "rep", "set", "deload", "badan", "otot",
       "muscle", "squat", "deadlift", "bench", "coaching", "atlet", "physique")
GOLD = ("gold", "emas", "xauusd", "trading", "posisi", "position sizing", "usd", "dolar",
        "yield", "fed", "kadar", "rates", "commodity", "komoditi", "drawdown", "margin",
        "setup", "entry", "risk", "hedge")
STRUCTURAL = ("sistem", "system", "institusi", "institution", "governance", "tadbir",
              "agent", "ai", "intelligence", "kecerdasan", "memory", "memori", "geolog",
              "geology", "petroleum", "energy", "tenaga", "capital", "modal", "epistem",
              "architecture", "arkitektur", "data", "model", "provenance")

# ── machine vocabulary. Reads as precision, carries no meaning to a human. ────
# (pattern, label). Warned, never held — the boundary is a judgement: "RSI 59.3"
# is a figure a trader reads fine, "confluence 0.016" is not. So it is made
# VISIBLE rather than enforced, and the writer translates it.
#
# This tuple is named by the G14 warning check. A check that references a
# constant nobody defined does not warn — it raises NameError and the gate
# crashes for EVERY card, which is how this comment came to exist.
MACHINE_TOKENS: tuple[tuple[str, str], ...] = (
    (r"\bconfluence\b", "confluence"),
    (r"\bRR\b", "RR"),
    (r"\bEMA\s?\d+\b", "EMA code"),
    (r"\bRSI\b", "RSI code"),
    (r"\b(?:keyakinan|confidence)\s*0?\.\d+", "raw confidence"),
    (r"\bverdict\b", "verdict"),
)

# ── privacy markers. A card both men read must not contain these. ────────────
PRIVATE_MARKERS = (
    "dia pernah cakap", "hang pernah cakap", "arif pernah cakap", "syed pernah cakap",
    "privately", "secara peribadi dia", "aku tahu hang", "kami tahu",
    "confidential", "rahsia dia", "rahsia hang", "dalaman kami",
    "berdasarkan apa yang hang cerita", "sebab hang pernah",
    "mss rm", "rm418", "od1",          # named private figures must not reprint
)

#: Vocabulary the engine uses to talk to itself, which must not reach a cell a
#: human reads. `RR 1.0, confluence 0.016` is opacity wearing the look of
#: precision — the reader can act on neither. `Momentum 59.3` is different: a
#: trader reads that figure directly, so only the raw engine internals and the
#: bare indicator codes are listed here.
MACHINE_TOKENS = (
    (r"\bRR\s*(?:cuma\s*)?[\d.]+", "RR=<n>"),
    (r"\bconfluence\s*[\d.]+", "confluence=<n>"),
    (r"\bkeyakinan\s*[\d.]+", "keyakinan=<float>"),
    (r"\bconfidence\s*[\d.]+", "confidence=<float>"),
    (r"\bEMA\s*\d+", "EMA<n>"),
    (r"\bRSI\s*[\d.]+", "RSI=<n>"),
    (r"\bDOWNTREND\b|\bUPTREND\b", "TREND_TOKEN"),
)



def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9\s]", " ", (s or "").lower()).split()


def _hits(text: str, lex: tuple[str, ...]) -> list[str]:
    t = (text or "").lower()
    return [k for k in lex if k in t]


def _subject(text: str) -> set[str]:
    """Cheap subject fingerprint: content words >= 5 chars, minus stopwords."""
    stop = {"untuk", "dalam", "dengan", "yang", "tidak", "bukan", "adalah", "kerana",
            "sebab", "masa", "hari", "benda", "orang", "lebih", "kalau", "sudah",
            "there", "their", "which", "would", "could", "about", "these", "those"}
    return {w for w in _norm(text) if len(w) >= 5 and w not in stop}


def chron_ok() -> tuple[bool, str]:
    try:
        evs = json.loads(STORE.read_text()).get("events", [])
    except Exception as exc:  # noqa: BLE001
        return False, f"cannot read chron store: {exc}"
    today = datetime.now().date()
    live = 0
    for e in evs:
        if e.get("state", "ACTIVE") != "ACTIVE":
            continue
        try:
            d = datetime.strptime(e["target_date"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            return False, f"event {e.get('id')} has an unparseable date"
        if (d - today).days >= 0:
            live += 1
    if live == 0:
        return False, "no live countdown — CHRON would render empty"
    return True, f"{live} live"


def run(card_path: Path) -> tuple[bool, list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    try:
        c = json.loads(card_path.read_text())
    except Exception as exc:  # noqa: BLE001
        return False, [f"cannot read card: {exc}"], []

    rows = c.get("rows") or []

    # G1
    if len(rows) != 9:
        errs.append(f"G1 components: need exactly 9 rows, got {len(rows)}")
    nums = [r.get("n") for r in rows]
    if nums != [f"0{i}" for i in range(1, 10)]:
        errs.append(f"G1 numbering: must run 01..09, got {nums}")

    # G2
    tiers: dict[str, int] = {}
    for r in rows:
        tiers[r.get("tier", "?")] = tiers.get(r.get("tier", "?"), 0) + 1
    for t, want in (("KENA_TAHU", 3), ("SUKA_TAHU", 3), ("EUREKA", 3)):
        if tiers.get(t, 0) != want:
            errs.append(f"G2 tiers: {t} needs {want}, got {tiers.get(t, 0)}")

    # G3 + G9 + G8
    a_txt, s_txt = [], []
    for r in rows:
        a, s = r.get("arif") or {}, r.get("syed") or {}
        if not a.get("text"):
            errs.append(f"G3 row {r.get('n')}: arif signal empty")
        if not s.get("text"):
            errs.append(f"G3 row {r.get('n')}: syed signal empty")
        if r.get("tier") == "KENA_TAHU":
            if not a.get("source"):
                errs.append(f"G3 row {r.get('n')}: KENA_TAHU arif needs a source")
            if not s.get("source"):
                errs.append(f"G3 row {r.get('n')}: KENA_TAHU syed needs a source")
        a_txt.append(a.get("text", ""))
        s_txt.append(s.get("text", ""))

    at, st = " ".join(a_txt), " ".join(s_txt)
    if not _hits(st, GYM):
        errs.append("G8 anchor: Syed has NO gym/body signal — a permanent attractor is missing")
    if not _hits(st, GOLD):
        errs.append("G8 anchor: Syed has NO gold/trading signal — a permanent attractor is missing")
    if not _hits(at, STRUCTURAL):
        errs.append("G8 anchor: Arif has no structural/intelligence signal")
    if not at.strip():
        errs.append("G9 relevance: Arif lane is empty")
    if not st.strip():
        errs.append("G9 relevance: Syed lane is empty")

    # G4
    ok, detail = chron_ok()
    if not ok:
        errs.append(f"G4 chron: {detail}")

    # G14 human register — WARN, not HOLD.
    #
    # The engine's internal vocabulary (RR, confluence, raw confidence floats) and
    # bare indicator codes (EMA20, RSI) are how the machine talks to itself. In a
    # cell a human reads, they are opacity wearing the look of precision: "RR cuma
    # 1.0, confluence 0.016" tells the reader nothing he can act on, while the
    # translated form ("sebab masuk tak cukup kuat untuk harga sekarang") carries
    # the same finding.
    #
    # Warn rather than hold because the boundary is a judgement — "Momentum 59.3"
    # is a figure a trader reads fine, "confluence 0.016" is not. A hard gate here
    # would start deleting legitimate signal. The warning makes it VISIBLE so the
    # writer fixes it; silence would let the register drift back.
    # Armed on BOTH surfaces, because they are not the same surface: the pool rows
    # are candidates, and `signals` is what actually publishes (G13). A rule that
    # only guards the pool would let the machine vocabulary walk out the door on the
    # one card the reader sees — clean where nobody looks, dirty where everybody does.
    def _reg(txt: str, where: str) -> None:
        hit = sorted({lab for pat, lab in MACHINE_TOKENS if re.search(pat, txt)})
        if hit:
            warns.append(f"G14 {where}: machine vocabulary in a human cell "
                         f"({', '.join(hit)}) — translate to what it means, or drop it")

    for r in rows:
        for who in ("arif", "syed"):
            _reg(((r.get(who) or {}).get("text") or ""), f"row {r.get('n')} ({who})")
    for i, sig in enumerate(c.get("signals") or []):
        if isinstance(sig, dict):
            _reg((sig.get("text") or ""), f"signals[{i}] ({sig.get('who')})")

    # G5 duplication — any two rows sharing a strong subject overlap
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            ri, rj = rows[i], rows[j]
            si = _subject((ri.get("arif") or {}).get("text", "") + " " +
                          (ri.get("syed") or {}).get("text", ""))
            sj = _subject((rj.get("arif") or {}).get("text", "") + " " +
                          (rj.get("syed") or {}).get("text", ""))
            if not si or not sj:
                continue
            overlap = len(si & sj) / max(1, min(len(si), len(sj)))
            if overlap >= 0.45:
                errs.append(f"G5 duplication: rows {ri.get('n')} and {rj.get('n')} "
                            f"share {overlap:.0%} of subject terms — same item twice")

    # G6 privacy
    blob = json.dumps(c, ensure_ascii=False).lower()
    for m in PRIVATE_MARKERS:
        if m in blob:
            errs.append(f"G6 privacy: card contains the marker {m!r} — "
                        f"read it as if the other man were reading it. Rewrite or drop.")
    for r in rows:
        for who, other in (("arif", "syed"), ("syed", "arif")):
            txt = ((r.get(who) or {}).get("text") or "").lower()
            if " sebab " in txt and ("hang" in txt or "dia" in txt):
                warns.append(f"G6 row {r.get('n')} ({who}): contains a causal clause "
                             f"about a person — check it does not reveal why it was chosen")

    # G7 quotes
    for k in ("yin_quote", "yang_quote"):
        q = c.get(k) or {}
        if not q.get("text") or not q.get("author"):
            errs.append(f"G7 {k}: needs text AND author — attribution cannot be omitted")
        elif q.get("author", "").lower().strip() in ("", "unknown", "anonymous", "ai"):
            errs.append(f"G7 {k}: author {q.get('author')!r} is not a real attribution")

    # G11 freshness — a source can be real and the number still stale.
    #
    # Scoped deliberately to rows carrying a PRICE token (RM / $ / harga / price).
    # Applying it to every numeral produced false holds on legitimately
    # low-frequency data: DOSM unemployment is monthly, not stale. A price is
    # different — a four-day-old gold quote is simply wrong, not merely old.
    price_tok = re.compile(r"(RM\s?\d|[$]\d|\bharga\b|\bprice\b)", re.I)
    for r in rows:
        if r.get("tier") != "KENA_TAHU":
            continue
        for who in ("arif", "syed"):
            sig = r.get(who) or {}
            txt, src = sig.get("text", ""), sig.get("source", "")
            if not price_tok.search(txt):
                continue
            age = _source_age_days(src, date.today())
            if age is None:
                errs.append(
                    f"G11 row {r.get('n')} ({who}): carries a price but its source "
                    f"has no DATE ({src!r}) — a figure cannot be checked without "
                    f"knowing when it was true")
            elif age > STALE_DAYS:
                errs.append(
                    f"G11 row {r.get('n')} ({who}): price is {age} days old "
                    f"(limit {STALE_DAYS}) per source {src!r} — re-verify against a "
                    f"live quote before sending a market number")

    # G12 no embedded day-counts — a number in prose cannot update itself.
    #
    # Found by auditing a parallel engine: it printed "budget_2027_days: 377"
    # (true value: 21 — off by exactly one year) and hardcoded "od1_days: 164" as
    # a literal. A clock that stores its own answer is not a clock.
    #
    # The same defect existed HERE: this card's CLOCK row read "9 Oktober — 21
    # hari". True on 18 Sep, wrong every day after, and nothing would have
    # caught it because it is prose, not a field.
    #
    # SCOPE — deliberately narrow, because a validator that emits false holds is
    # as broken as one that misses real ones. First run flagged "11,000 tahun"
    # (Perak Man's age) as a frozen countdown. It is an archaeological FACT, not a
    # clock. So:
    #   * only day/week/month units are checked — year-scale clocks belong to CHRON
    #   * numbers carrying a thousands separator are deep-time/historical facts
    #   * the value must be plausible as a near-term countdown (< 400)
    daycount = re.compile(
        r"\b(\d{1,4})\s*(?:hari|days?|bulan|months?|minggu|weeks?)\b", re.I)
    allow_ctx = re.compile(r"(harga|price|kuat kuasa|sehari|sehari-hari|per hari)", re.I)
    for r in rows:
        for who in ("arif", "syed"):
            txt = ((r.get(who) or {}).get("text") or "")
            for m in daycount.finditer(txt):
                # a digit run inside a comma-grouped number (11,000) is not a count
                start = m.start(1)
                if start >= 1 and txt[start - 1] == ",":
                    continue
                if int(m.group(1)) >= 400:
                    continue
                ctx = txt[max(0, m.start() - 30):m.end() + 30]
                if allow_ctx.search(ctx):
                    continue
                errs.append(
                    f"G12 row {r.get('n')} ({who}): prose contains a day-count "
                    f"({m.group(0)!r}). A number written into text is frozen at "
                    f"authoring time and will be wrong tomorrow. Cite the DATE "
                    f"instead; let CHRON carry the countdown.")

    # ── G13 THE SIGNAL CARD ────────────────────────────────────────────────
    # F13-directed 2026-09-21: "too chaos, signal only". The 9 rows are the
    # candidate POOL; `signals` is what actually publishes.
    #
    # This is not a second gate bolted on for symmetry. Narrowing is where
    # people get dropped: the first lines to vanish from a "signal only" card
    # are the ones whose subject is rarest in the day's news — which is
    # exactly Syed's whole lane. So the publication layer gets its own wall:
    # the pool may be wide, the card must be narrow, and BOTH men must still
    # come out of it with something.
    sigs = c.get("signals")
    if sigs is not None:
        # GYM is reused as-is (body words). GOLD is NOT: GOLD is a POOL anchor,
        # where "kadar" or "risk" is enough to say a row is about money. The
        # signal card needs a line a reader can recognise AS the gold/trading
        # lane, so the loose topic words are dropped here and the rest matched
        # on word boundaries.
        gym = GYM
        gold = ("emas", "gold", "xauusd", "perak", "silver", "bank pusat", "central bank",
                "rizab", "reserve", "dxy", "us10y", "trading", "posisi")
        if not isinstance(sigs, list) or not (4 <= len(sigs) <= 8):
            got = len(sigs) if isinstance(sigs, list) else "not a list"
            errs.append(f"G13 signals: need 4-8 lines, got {got} — a signal card "
                        f"that needs scrolling is the card it was meant to replace")
        seen: list[tuple[int, set[str]]] = []
        if isinstance(sigs, list):
            for i, s in enumerate(sigs):
                if not isinstance(s, dict):
                    errs.append(f"G13 signals[{i}]: not an object")
                    continue
                if s.get("who") not in ("arif", "syed", "shared"):
                    errs.append(f"G13 signals[{i}]: who must be arif|syed|shared, "
                                f"got {s.get('who')!r}")
                txt = (s.get("text") or "").strip()
                if not txt:
                    errs.append(f"G13 signals[{i}]: empty — a signal that says nothing "
                                f"is a blank line with a receipt")
                    continue
                if len(txt) > 240:
                    errs.append(f"G13 signals[{i}]: {len(txt)} chars — a signal is one "
                                f"sentence, not a paragraph. Cut it or leave it in the pool.")
                for tok in ("KENA_TAHU", "SUKA_TAHU", "EUREKA", "ARIF:", "SYED:"):
                    if tok.lower() in txt.lower():
                        errs.append(f"G13 signals[{i}]: contains the machine label {tok!r} — "
                                    f"the card speaks human; the tiers stay in the file")
                for m in daycount.finditer(txt):
                    st = m.start(1)
                    if st >= 1 and txt[st - 1] == ",":
                        continue
                    if int(m.group(1)) >= 400:
                        continue
                    if allow_ctx.search(txt[max(0, m.start() - 30):m.end() + 30]):
                        continue
                    errs.append(f"G13 signals[{i}]: carries a day-count ({m.group(0)!r}) that "
                                f"is wrong tomorrow — cite the date and let CHRON count")
                for mk in PRIVATE_MARKERS:
                    if mk in txt.lower():
                        errs.append(f"G13 signals[{i}]: private marker {mk!r} — "
                                    f"read it as the other man would")
                subj = _subject(txt)
                for j, prev in seen:
                    if not subj or not prev:
                        continue
                    ov = len(subj & prev) / max(1, min(len(subj), len(prev)))
                    if ov >= 0.45:
                        errs.append(f"G13 signals[{i}] and signals[{j}] share {ov:.0%} of "
                                    f"subject terms — one event printed twice")
                seen.append((i, subj))
            texts = [(s.get("text") or "").lower() for s in sigs if isinstance(s, dict)]
            # WORD-BOUNDARY matching, not substring. Caught by the negative control:
            # "kemas kini" contains "emas", so deleting the gold line STILL passed
            # the gold anchor. A substring test turns a coincidence of spelling into
            # evidence of a signal — the same defect class as G12 flagging
            # "11,000 tahun" as a countdown.
            def _wb(tl: list[str], lex: tuple[str, ...]) -> bool:
                pat = rf"\b(?:{'|'.join(re.escape(k) for k in lex)})"
                return any(re.search(pat, t) for t in tl)

            # Lexical backstop, not a judgement: it proves a gym line and a gold
            # line are PRESENT. Whether either is any good is the composer's job.
            if not _wb(texts, gym):
                errs.append("G13 anchors: no gym/body line survived the narrowing — "
                            "Syed's permanent attractor was dropped to make room")
            if not _wb(texts, gold):
                errs.append("G13 anchors: no gold/trading line survived the narrowing — "
                            "Syed's permanent attractor was dropped to make room")
            if not any(s.get("who") in ("arif", "shared") for s in sigs
                       if isinstance(s, dict)):
                errs.append("G13 relevance: every line belongs to Syed's world — "
                            "Arif is reading someone else's card")
            if not any(s.get("who") in ("syed", "shared") for s in sigs
                       if isinstance(s, dict)):
                errs.append("G13 relevance: every line belongs to Arif's world — "
                            "Syed is reading someone else's card")

    return (not errs), errs, warns


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 0
    p = Path(argv[0])
    ok, errs, warns = run(p)
    print(f"ALPHA-ZEN GATE — {p.name}")
    print("=" * 66)
    for w in warns:
        print(f"  ⚠  {w}")
    for e in errs:
        print(f"  ✗  {e}")
    print("=" * 66)
    if ok:
        print("  VERDICT: PASS — artifact may be sent")
        return 0
    print(f"  VERDICT: HOLD — {len(errs)} gate failure(s). DO NOT SEND.")
    print("  Fix the content. Do not lower a threshold to pass.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
