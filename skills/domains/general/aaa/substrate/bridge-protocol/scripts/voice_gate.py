#!/usr/bin/env python3
"""
voice_gate.py - mechanical pre-flight for the VOICE-GOVERNOR output law.

Part of the `bridge-protocol` skill (STAGE 3: RESPOND).

WHY THIS EXISTS: the law says "do not rely on awareness against prompt-level format pressure -
strip mechanically". A model reading its own draft cannot reliably detect its own AI-speak.
This script can.

HONEST SCOPE: this is a WITNESS, not a judge. It checks what is countable.
Tension, Peace-squared, delta-S and RASA are JUDGMENT_ONLY - the script says so in its output
rather than faking a score for them. A green result here means only:
"no mechanical AI-speak survived". It does NOT mean the reply passed the law.

USAGE
    echo "...reply text..." | python3 voice_gate.py
    python3 voice_gate.py --file reply.txt
    python3 voice_gate.py "reply text in argv"
    python3 voice_gate.py --file reply.txt --audience internal --json

    --audience human (default) full gate, including the Arif register bans
    --audience internal       skips register bans and label checks (reasoning, receipts, code)
    --thermal                 only report the SABAR heat/cooldown state

EXIT CODES
    0 = mechanical pass     1 = re-draft     2 = SABAR cooldown first
    3 = usage / input error
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import dataclass, field
from typing import Iterable

# ---------------------------------------------------------------------------
# Banks. Each entry: (regex, label, suggestion-or-None)
# Regexes are case-insensitive; use \b where a bare substring would over-match.
# ---------------------------------------------------------------------------

AI_SPEAK: list[tuple[str, str, str | None]] = [
    # --- Malay formal/bureaucratic AI-speak ---
    (r"adalah penting untuk", "bm_formal_filler", "terus kata apa yang penting"),
    (r"perlu diambil perhatian", "bm_formal_filler", None),
    (r"mari kita lihat", "filler_opener", "buang, mula terus dengan benda sebenar"),
    (r"mari kita(?!\s+bincang|\s+tengok)\b", "filler_opener", None),
    (r"sehubungan dengan itu", "connective_filler", None),
    (r"dengan ini(\s+(?:di)?nyatakan)?\b", "legalese", None),
    (r"\bselanjutnya\b", "connective_filler", None),
    (r"\bolehkah\b", "bm_formal", "boleh x"),
    (r"\bmengapa\b", "bm_formal", "apsal"),
    (r"\bencik\b", "bm_formal", "hang"),
    (r"\banda\b", "bm_formal", "hang"),
    (r"\bawak\b", "bm_formal", "hang"),
    (r"\bsaya\b", "pronoun_ban", "aku"),
    (r"\btidak\b", "bm_formal", "tak / x"),
    (r"\bmesyuarat\b", "bm_baku", "meeting"),
    (r"\bberkaitan dengan\b", "bm_baku", "pasal"),
    # --- English AI-speak ---
    (r"it(?:'s| is) (?:important|worth) (?:to note|noting)", "en_formal_filler", None),
    (r"i(?:'d| would) be happy to", "service_desk", None),
    (r"would you like me to", "service_desk", "buat keputusan, tanya hanya di sempadan F13"),
    (r"as an ai\b", "ai_disclosure_tell", None),
    (r"as a language model", "ai_disclosure_tell", None),
    (r"\bdelv\w* into\b", "en_slop", None),
    (r"\bleverag\w*\b", "en_slop", "guna"),
    (r"\butiliz\w*\b", "en_slop", "guna"),
    (r"\bseamless\w*\b", "en_slop", None),
    (r"\brobust\w* solution\b", "en_slop", None),
    (r"\bin conclusion\b", "en_formal_filler", None),
    (r"\bfurthermore\b", "en_formal_filler", None),
    (r"\bmoreover\b", "en_formal_filler", None),
    (r"comprehensive overview", "en_formal_filler", None),
    (r"let me know if you (?:need|have)", "service_desk", None),
    (r"feel free to reach out", "service_desk", None),
    (r"i hope this helps", "service_desk", None),
]

WEAK_CLOSER: list[tuple[str, str]] = [
    (r"terima kasih kerana membaca", "gratitude_padding"),
    (r"semoga (?:bermanfaat|membantu)", "wish_padding"),
    (r"harap (?:dapat )?membantu", "wish_padding"),
    (r"selamat maju jaya", "wish_padding"),
    (r"jangan ragu(?:-ragu)? untuk", "service_desk"),
    (r"have a (?:great|nice) day", "wish_padding"),
    (r"(?:let me know|tell me) if you need anything", "service_desk"),
    (r"i(?:'m| am) here (?:for you|if you need)", "verbal_affection"),
    (r"(?:ditempa|ditemba) bukan diberi", "motto_as_punctuation"),
    (r"ditemba bukan diberi", "motto_as_punctuation"),
    (r"—\s*$|^-\s*$|\b(?:wallahualam|sekian,? terima kasih)\b", "trailing_self_ref",),
]

# Structural-skill frame patterns that belong in offline deliverables (wisdom-letter,
# briefing, multi-document-drafting), NOT in CONVERSE replies. When a chat reply carries
# more than 2 hits it is the wrong artefact shape - the wisdom-letter template is bleeding
# into the chat surface. The companion to this list is the forensic-topic cooldown in
# bridge-protocol SKILL.md §STAGE 3.
STRUCTURAL_FRAME: list[tuple[str, str]] = [
    (r"(?m)^Layer\s+\d+\s*[—\-]", "structural_layer_frame"),
    (r"(?m)^Bab\s+\d+\s*[—\-]", "structural_layer_frame_bm"),
    (r"(?m)^Section\s+\d+\s*[—\-]", "structural_layer_frame_en"),
    (r"(?m)^##\s+(?:Opening|Nasihat|Practical Steps|Closing)\s*$", "letter_header_template"),
]

HUMAN_LABEL_LEAK: list[tuple[str, str]] = [
    (r"\[\s*(?:OBS|DER|INT|SPEC|ACT|SILENT|HOLD|SEAL|WITNESS)\s*\]", "receipt_label"),
    (r"\[\s*\U0001F9BE\s*ACT\s*\]", "receipt_label"),
    (r"\b(?:ΔS|dS|delta_?S)\b", "entropy_label"),
    (r"\b(?:OBS|DER|INT|SPEC)\s*:", "receipt_label"),
    (r"\btrace_?id\b", "receipt_label"),
    (r"\b(?:APEX|ZEN|F13|F2)\b\s*(?:=|:)", "doctrine_label"),
    (r"\b(?:ROUTED|VERDICT|STATE)\s*:", "verdict_label"),
    (r"\b(?:init|seal|judge)\s*(?:→|->)", "verb_chain_leak"),
]

# Words that add disorder for a human reader rather than reducing it.
ENTROPY_ADDERS: list[tuple[str, str]] = [
    (r"\b(?:epistemik|ontolog(?:i|ikal)|isomorfik|heuristik|aksiologi)\b", "jargon"),
    (r"\b(?:paradigma|sinergi|operasionalisasi|kontekstualisasi)\b", "jargon"),
    (r"\b(?:ortogonal|ortogonality|invariant|substrat)\b", "jargon"),
    (r"\b(?:isomorphism|epistemic|ontology|heuristic|substrate|orthogonal|invariant)\b", "jargon_en"),
    (r"\b(?:L1|L2|L3|L4|L5)\b\s*(?:memory|layer)", "internal_arch"),
    (r"\b(?:MCP|SSOT|SOT|CI/CD)\b", "internal_arch_en"),
]

HEAT_WORDS: list[str] = [
    "bangang", "bodoh", "sial", "celaka", "pukimak", "babi", "punda", "sundal",
    "stupid", "idiot", "idiotic", "bullshit", "wtf", "garbage", "useless",
]

# BM markers are distinctive enough for substring; English pronouns need word boundaries
# (a bare "i " substring false-positives inside "kali ", "sini ", "multi ").
INTIMACY_PRESENT: list[str] = [
    "hang", "kau", "aku", "kita", "kami", "depa", "korang", "kitorang",
]
INTIMACY_PRESENT_RE = re.compile(r"\b(?:you|we|our|us|i|me|my)\b", re.IGNORECASE)

INTIMACY_ABSENT_MARKERS: list[str] = [
    "para pembaca", "pembaca yang dihormati", "pengguna", "pengguna yang dihormati",
    "the reader", "users", "stakeholders", "audience", "readers",
]

# Concrete / witnessed specificity: numbers, years, currency, named tokens.
SPEC_NUMERIC = re.compile(r"(?:\b\d{4}\b|\bRM\s?[\d,]+|\b\d+(?:\.\d+)?\s?%|\b\d+(?:\.\d+)?\b)")
SPEC_CAPS = re.compile(r"\b(?!I\b)[A-Z][a-zA-Z]{2,}(?:\s+[A-Z][a-zA-Z]+)?\b")

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")

WEAK_OPENERS = re.compile(
    r"^(?:ok(?:ay)?|alright|sure|well|so|hello|hi|hei|hai|greetings|good (?:morning|afternoon|evening))\b[,.! ]*",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------


@dataclass
class Finding:
    gate: str
    severity: str  # FLAG | WARN | INFO
    label: str
    match: str
    suggestion: str | None = None
    count: int = 1


@dataclass
class Report:
    audience: str
    words: int = 0
    sentences: int = 0
    findings: list[Finding] = field(default_factory=list)
    mechanical: dict[str, str] = field(default_factory=dict)
    judgment_only: list[str] = field(default_factory=list)
    sabar_triggered: bool = False
    sabar_reasons: list[str] = field(default_factory=list)


def sentences(text: str) -> list[str]:
    return [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]


def find_bank(text: str, bank: Iterable[tuple], gate: str, severity: str,
              quoted: list[tuple[int, int]] | None = None) -> list[Finding]:
    out: list[Finding] = []
    quoted = quoted or []
    for entry in bank:
        pattern, label = entry[0], entry[1]
        suggestion = entry[2] if len(entry) > 2 else None
        matches = list(re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE))
        if not matches:
            continue
        # Mention vs use: a hit inside quotes is cited text, not the author's voice.
        live = [m for m in matches if not _in_spans(m.start(), quoted)]
        cited = [m for m in matches if _in_spans(m.start(), quoted)]
        if live:
            out.append(Finding(gate=gate, severity=severity, label=label,
                               match=live[0].group(0).strip()[:60], suggestion=suggestion,
                               count=len(live)))
        if cited:
            out.append(Finding(gate=gate, severity="INFO", label=label + " (quoted_mention)",
                               match=cited[0].group(0).strip()[:60],
                               suggestion="quoted example - mention, not use", count=len(cited)))
    return out


def _quoted_spans(text: str) -> list[tuple[int, int]]:
    """Spans of quoted material - mention, not use.

    A linter that cannot tell mention from use fires on every quoted example. Standard
    approach: quoted substrings are cited text, so a hit inside them is downgraded to INFO
    rather than dropped - the reader still sees it, it just cannot force a RE-DRAFT.
    """
    spans: list[tuple[int, int]] = []
    for m in re.finditer(r'"[^"\n]{1,200}"|\u00ab[^\u00bb\n]{1,200}\u00bb|\u201c[^\u201d\n]{1,200}\u201d', text):
        spans.append((m.start(), m.end()))
    return spans


def _in_spans(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(a <= pos < b for a, b in spans)


def _is_identifier_token(text: str, start: int, end: int) -> bool:
    """True when an ALL-CAPS token is a filename / path / identifier, not shouting.

    'VOICE-GOVERNOR', 'STAGE 3', 'SKILL.md', 'SOUL.md' are names. Shouting is different.
    """
    after = text[end:end + 4]
    before = text[max(0, start - 1):start]
    if before in ("/", "."):
        return True
    if after.startswith(("-", "_", ".py", ".md", ".json", ".sh", ".yaml")):
        return True
    # hyphenated all-caps pair, e.g. VOICE-GOVERNOR, RASA-Authenticity
    if re.match(r"-[A-Za-z]", after) or before == "-":
        return True
    return False


KNOWN_NAMES = {
    "VOICE", "GOVERNOR", "STAGE", "SABAR", "DITING", "READ", "REASON", "RESPOND",
    "SKILL", "SOUL", "SOUL.md", "APEX", "ZEN", "F13", "F2", "F7", "RASA", "PEACE",
    "JSON", "HTTP", "HTTPS", "YAML", "TRUE", "FALSE", "NONE", "PASS", "FAIL",
}


def check_heat(text: str, r: Report) -> None:
    bangs = text.count("!")
    if bangs >= 2:
        r.sabar_triggered = True
        r.sabar_reasons.append(f"{bangs} exclamation marks (>=2)")
    letters = [c for c in text if c.isalpha()]
    caps = [c for c in letters if c.isupper()]
    ratio = (len(caps) / len(letters)) if letters else 0.0
    if ratio > 0.35 and len(letters) > 40:
        r.sabar_triggered = True
        r.sabar_reasons.append(f"caps ratio {ratio:.0%} > 35%")
    # ALL-CAPS as a heat signal must be SHOUTING, not naming files / doctrines.
    loud: list[str] = []
    for m in re.finditer(r"\b[A-Z]{3,}\b", text):
        w = m.group(0)
        if _is_identifier_token(text, m.start(), m.end()):
            continue
        if w in KNOWN_NAMES:
            continue
        loud.append(w)
    # A couple of emphasised caps words inside an otherwise calm message is ordinary
    # register in BM chat ("aku suruh JANGAN"), not heat. Require corroboration before
    # treating caps as a SABAR trigger: the ratio rule above already catches genuine
    # ALL-CAPS shouting, and exclamations/heat-words catch the rest.
    corroborated = bool(bangs) or ratio > 0.15 or any(
        re.search(rf"\b{re.escape(w)}\w*\b", text, re.IGNORECASE) for w in HEAT_WORDS
    )
    if len(loud) >= 2 and corroborated:
        r.sabar_triggered = True
        r.sabar_reasons.append(f"all-caps words: {', '.join(loud[:4])}")
    elif len(loud) >= 2:
        r.findings.append(Finding(
            gate="SABAR", severity="INFO", label="caps_emphasis_uncorroborated",
            match=", ".join(loud[:4]),
            suggestion="emphasis caps only, no other heat signal - not treated as SABAR",
            count=len(loud),
        ))
    for w in HEAT_WORDS:
        if re.search(rf"\b{re.escape(w)}\w*\b", text, re.IGNORECASE):
            r.sabar_triggered = True
            r.sabar_reasons.append(f"heat word: {w}")


def check_intimacy(text: str, r: Report) -> None:
    low = text.lower()
    present = sorted({m for m in INTIMACY_PRESENT if m in low})
    present += sorted({m.group(0).lower() for m in INTIMACY_PRESENT_RE.finditer(text)})
    present = sorted(set(present))
    absent = sorted({m for m in INTIMACY_ABSENT_MARKERS if m in low})
    if absent:
        r.findings.append(Finding(
            gate="Intimacy", severity="FLAG", label="audience_address",
            match=", ".join(absent), suggestion="sebut 'hang' / 'kita' — cakap dengan satu orang",
        ))
    r.mechanical["intimacy"] = (
        f"PASS (markers: {', '.join(present)})" if present and not absent
        else "WARN (no second-person marker)" if not present else "FLAG"
    )


def check_gates(text: str, r: Report) -> None:
    sents = sentences(text)
    r.sentences = len(sents)
    r.words = len(text.split())

    # --- Density ---
    lens = [len(s.split()) for s in sents] or [0]
    avg = statistics.mean(lens) if lens else 0
    long_sents = [s for s in sents if len(s.split()) > 32]
    if avg > 26:
        r.findings.append(Finding("Density", "WARN", "dense_sentences",
                                  f"avg {avg:.0f} words/sentence", "pecahkan jadi ayat pendek"))
    for s in long_sents[:3]:
        r.findings.append(Finding("Density", "WARN", "long_sentence",
                                  s[:60] + ("..." if len(s) > 60 else ""),
                                  "potong separuh"))
    if WEAK_OPENERS.match(text.strip()):
        r.findings.append(Finding("Density", "WARN", "greeting_opener",
                                  text.strip()[:40],
                                  "buang sapaan — ayat pertama kena lekat pada realiti dia"))
    r.mechanical["density"] = (
        f"PASS (avg {avg:.0f} w/s, {r.sentences} ayat)" if not long_sents and avg <= 26
        else f"WARN (avg {avg:.0f} w/s, {len(long_sents)} ayat panjang)"
    )

    # --- Image (proxy) ---
    # concrete = digits/currency/caps-nouns roughly per 100 words
    spec_hits = len(SPEC_NUMERIC.findall(text))
    cap_hits = len(SPEC_CAPS.findall(text))
    concrete = (spec_hits + cap_hits) / max(r.words, 1) * 100
    r.mechanical["image"] = (
        f"PROXY (concrete tokens {concrete:.1f}/100w: {spec_hits} numeric, {cap_hits} named) "
        f"- anchor fit is judgment"
    )
    if concrete < 1.5 and r.words > 60:
        r.findings.append(Finding("Image", "WARN", "low_concrete_density",
                                  f"{concrete:.1f} concrete tokens/100w",
                                  "tambah benda yang boleh disentuh / tempat / tarikh"))

    # --- Named (proxy) ---
    r.mechanical["named"] = f"PROXY ({spec_hits} numeric, {cap_hits} named tokens) - adequacy is judgment"

    # --- Gravity ---
    last = sents[-1] if sents else ""
    low = last.lower()
    if re.search(r"[.!?]$", last) and len(last.split()) > 45:
        r.findings.append(Finding("Gravity", "WARN", "weak_closer_long",
                                  last[:60], "hujung kena hentak, bukan mengalir"))
    if len(last.split()) < 3 and last:
        r.findings.append(Finding("Gravity", "WARN", "weak_closer_short", last,
                                  "ayat terakhir terlalu ringan"))
    r.mechanical["gravity"] = f"WARN (closer: {last[:50]!r})" if len(last.split()) < 3 else "PASS (closer present)"

    # --- Entropy proxy ---
    ent = sum(f.count for f in find_bank(text, ENTROPY_ADDERS, "dS", "WARN"))
    hedge = len(re.findall(r"\b(?:mungkin|kadang-kadang|agak|perhaps|maybe|possibly|it depends)\b", text, re.IGNORECASE))
    q = text.count("?")
    r.mechanical["delta_s"] = (
        f"PROXY (jargon {ent}, hedge {hedge}, questions {q}) - disorder is judgment"
    )
    if ent:
        r.findings.append(Finding("dS", "WARN", "jargon_proxy", f"{ent} jargon token(s)",
                                  "tukar jadi bahasa yang orang boleh rasa"))

def check_register(text: str, r: Report) -> None:
    quoted = _quoted_spans(text)
    r.findings += find_bank(text, AI_SPEAK, "Density", "FLAG", quoted)
    r.findings += find_bank(text, HUMAN_LABEL_LEAK, "Intimacy", "FLAG", quoted)
    # weak closers only if in last third of the text
    third_start = int(len(text) * 0.6)
    third = text[third_start:]
    shifted = [(a - third_start, b - third_start) for a, b in quoted if b > third_start]
    r.findings += find_bank(third, WEAK_CLOSER, "Gravity", "FLAG", shifted)


def check_structural_frame(text: str, r: Report) -> None:
    """Count `^Layer N —` / `^Bab N —` / `^Section N —` / letter-header patterns.

    These belong in offline deliverables (wisdom-letter, multi-document-drafting), not in
    CONVERSE chat replies. More than 2 hits = the structural-skill template is bleeding
    into the chat surface; mechanical RE-DRAFT and let the human re-state or accept a
    prose paragraph. One or two is fine (a single "Layer 1 / Layer 2" prose summary).
    Quoted substrings (mention vs use) are still downgraded to INFO via find_bank's
    quoted-spans handling. See bridge-protocol SKILL.md §STAGE 3 forensic cooldown.
    """
    quoted = _quoted_spans(text)
    hits = find_bank(text, STRUCTURAL_FRAME, "Register", "WARN", quoted)
    # Count live (non-quoted) hits; if > 2 it's a RE-DRAFT, not just a warning.
    live_count = sum(f.count for f in hits if f.severity == "WARN")
    if live_count > 2:
        for f in hits:
            if f.severity == "WARN":
                f.severity = "FLAG"
                f.suggestion = "strip the layer/letter-frame - write as prose paragraph"
    r.findings += hits


def mechanical_verdict(r: Report) -> str:
    flags = [f for f in r.findings if f.severity == "FLAG"]
    warns = [f for f in r.findings if f.severity == "WARN"]
    if flags:
        return "RE-DRAFT"
    if len(warns) > 2:
        return "RE-DRAFT"
    return "PASS"


def render(r: Report, as_json: bool) -> str:
    verdict = mechanical_verdict(r)
    if as_json:
        return json.dumps({
            "audience": r.audience,
            "words": r.words,
            "sentences": r.sentences,
            "mechanical_verdict": verdict,
            "sabar_triggered": r.sabar_triggered,
            "sabar_reasons": r.sabar_reasons,
            "gates_mechanical": r.mechanical,
            "judgment_only": r.judgment_only,
            "findings": [f.__dict__ for f in r.findings],
            "disclaimer": (
                "Do not read PASS as a pass of the law. Tension, Peace^2, dS and RASA are "
                "judgment-only. PASS means only: no mechanical AI-speak survived."
            ),
        }, ensure_ascii=False, indent=2)

    L: list[str] = []
    L.append(f"VOICE-GATE  audience={r.audience}  {r.words}w / {r.sentences} sentences")
    L.append(f"mechanical verdict: {verdict}")
    if r.sabar_triggered:
        L.append("")
        L.append("SABAR COOLDOWN REQUIRED:")
        for reason in r.sabar_reasons:
            L.append(f"  - {reason}")
        L.append("  -> acknowledge heat, slow down, common ground, ask a question")
    L.append("")
    L.append("Gates:")
    for k in ("density", "image", "intimacy", "named", "gravity", "delta_s"):
        if k in r.mechanical:
            L.append(f"  {k:<9} {r.mechanical[k]}")
    L.append("")
    if r.findings:
        L.append(f"Findings ({len(r.findings)}):")
        for f in r.findings:
            rep = f" (x{f.count})" if f.count > 1 else ""
            L.append(f"  [{f.severity}] {f.gate}/{f.label}{rep}: {f.match}")
            if f.suggestion:
                L.append(f"          -> {f.suggestion}")
    else:
        L.append("Findings: none mechanical.")
    L.append("")
    L.append("JUDGMENT ONLY (not machine-checkable, you must decide):")
    for j in r.judgment_only:
        L.append(f"  - {j}")
    L.append("")
    L.append("PASS here means only: no mechanical AI-speak survived.")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="VOICE-GOVERNOR mechanical pre-flight (bridge-protocol STAGE 3)")
    ap.add_argument("text", nargs="?", help="reply text (or use --file / stdin)")
    ap.add_argument("--file", "-f", help="read reply text from a file")
    ap.add_argument("--audience", choices=["human", "internal"], default="human")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--thermal", action="store_true", help="report only SABAR heat state")
    args = ap.parse_args(argv)

    if args.file:
        try:
            text = open(args.file, encoding="utf-8").read()
        except OSError as e:
            print(f"voice_gate: cannot read {args.file}: {e}", file=sys.stderr)
            return 3
    elif args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        ap.print_help()
        return 3

    text = text.strip()
    if not text:
        print("voice_gate: empty input", file=sys.stderr)
        return 3

    r = Report(audience=args.audience)
    r.judgment_only = [
        "Tension - is a question or risk left standing?",
        "Peace^2 - Peace_self (no forced narrative) + Peace_other (critique system, not person)",
        "delta-S - does this reduce or add disorder in the reader's mind?",
        "RASA - Resonance, Authenticity, Specificity, Affect (all 4)",
        "Gravity - does the last sentence actually land?",
        "Image - does the anchor fit, or is it decoration?",
    ]

    check_heat(text, r)
    if args.audience == "human":
        check_register(text, r)
        check_intimacy(text, r)
        check_gates(text, r)
        check_structural_frame(text, r)
    else:
        check_gates(text, r)
        check_structural_frame(text, r)

    if args.thermal:
        out = {"sabar_triggered": r.sabar_triggered, "reasons": r.sabar_reasons}
        print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else
              ("SABAR: TRIGGERED\n" + "\n".join("  - " + x for x in r.sabar_reasons)
               if r.sabar_triggered else "SABAR: quiet"))
        return 2 if r.sabar_triggered else 0

    print(render(r, args.json))

    if r.sabar_triggered:
        return 2
    if mechanical_verdict(r) == "PASS":
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
