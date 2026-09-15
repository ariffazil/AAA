#!/usr/bin/env python3
"""extract.py — SESSION / SCAR / EUREKA → classified capability atoms.

Stage 1+2 of the vNext pipeline:
    SESSION → EUREKA EXTRACTOR → SCAR CLASSIFIER → (atoms.py)

Reads LIVE surfaces, not a transcript of them:
  · /root/.hermes/state.db            (live session store, read-only URI)
  · /root/AAA/scars/candidates/*.md   (auto-scar candidates)
  · /root/AAA/canon/EUREKA-*.md       (canon eurekas)
  · /root/.local/share/arifos/rsi-ledger.jsonl  (existing loop ledger)

Design rule (F2/F9): a heartbeat is not a diagnosis. Only signals that carry a
concrete failure or correction become candidates. "I observed, nothing improved"
is not an atom.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import time
from datetime import datetime, timedelta, timezone

import atoms as A

STATE_DB = "/root/.hermes/state.db"
SCAR_CANDIDATES = "/root/AAA/scars/candidates"
CANON = "/root/AAA/canon"
RSI_LEDGER = "/root/.local/share/arifos/rsi-ledger.jsonl"

MARKERS = {
    # marker → (pattern_type, layer, impact)
    r"Traceback \(most recent call last\)": ("SILENT_FAIL", "skill", "runtime_error"),
    r"\b(No such file or directory|ENOENT)\b": ("PATH_DRIFT", "capability", "path_unresolved"),
    r"\b(skill-not-found|not found in registry|unknown skill)\b": ("REGISTRY_MISMATCH", "capability", "registry_gap"),
    r"\b(404|404 Not Found|no such tool|unknown tool)\b": ("REGISTRY_MISMATCH", "capability", "surface_gap"),
    r"\b(401|403|Unauthorized|Forbidden|permission denied)\b": ("PERMISSION_DRIFT", "capability", "auth_gap"),
    r"\b(timeout|timed out|ETIMEDOUT|Connection refused|ECONNREFUSED)\b": ("SILENT_FAIL", "capability", "transport"),
    r"\bno_change|NO_CHANGE\b": ("QUEUE_BLOCKED", "capability", "no_delta"),
    r"\b(rejected=1|REJECT|blocked)\b.{0,60}\b(same|again|repeat)": ("QUEUE_BLOCKED", "capability", "stuck_retry"),
    r"\bduplicate (source of truth|SOT)\b|\btwo .{0,20}sources of truth\b": ("DUPLICATE_SOT", "capability", "split_truth"),
    r"\bdead pointer|broken symlink|stale (path|dir|directory)\b": ("DEAD_POINTER", "skill", "unresolved_ref"),
    r"\b(self[- ]?(eval|audit|score|graded)|grades its own)\b": ("SELF_EVAL", "policy", "evaluator_contamination"),
    r"\b(proxy reality|transcript pretending|config pretending|narrative pretending)\b": ("PROXY_REALITY", "policy", "layer_confusion"),
    r"\b(copy[- ]paste|run this|paste into|terminal)\b.{0,80}\b(arif|sovereign|hang)\b": ("HUMAN_BURDEN", "policy", "sovereign_burden"),
    r"\b(truncat|head \+ tail|silently cut|omitted middle)\b": ("TRUNCATION_LOSS", "skill", "evidence_loss"),
}

# User-signal corrections (Arif steering). These are judgment-tier material.
CORRECTION = re.compile(
    r"\b(jangan|cakap baku|salah|tak betul|bukan macam tu|x betul|"
    r"hate the terminal|kau ni|ni salah|tu salah|tak sama|bukan itu)\b", re.I)

def _is_dead_field_signature(text: str) -> bool:
    return bool(re.search(r"\b(last_delta_s|improvements?)\b", text)) and \
        bool(re.search(r"\b0\b|zero|unmeasurable", text, re.I))


def _normalise(s: str) -> str:
    """Collapse volatile parts so the same failure yields the same signature."""
    s = re.sub(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "<uuid>", s)
    s = re.sub(r"\b[0-9a-f]{12,64}\b", "<hash>", s)
    s = re.sub(r"/root/\S+", "<path>", s)
    s = re.sub(r"\d+", "<n>", s)
    return s.strip()[:200]


def _coerce(content) -> str:
    if content is None:
        return ""
    if isinstance(content, (bytes, bytearray)):
        try:
            return content.decode("utf-8", "replace")
        except Exception:
            return ""
    if isinstance(content, str):
        return content
    return str(content)


def read_sessions(days: int, limit: int = 4000) -> list[dict]:
    """Read live session messages inside the window."""
    if not os.path.exists(STATE_DB):
        return []
    since = time.time() - days * 86400
    rows = []
    try:
        con = sqlite3.connect(f"file:{STATE_DB}?mode=ro", uri=True, timeout=10)
        cur = con.execute(
            "select m.session_id, m.role, m.tool_name, m.content, m.timestamp, s.source "
            "from messages m left join sessions s on s.id = m.session_id "
            "where m.timestamp >= ? and m.active = 1 "
            "order by m.timestamp desc limit ?", (since, limit))
        for r in cur:
            rows.append({"session_id": r[0], "role": r[1], "tool": r[2],
                         "content": _coerce(r[3]), "ts": r[4], "source": r[5]})
        con.close()
    except Exception as exc:
        rows.append({"session_id": None, "role": "system",
                     "content": f"state.db read failed: {exc}", "ts": time.time()})
    return rows


def extract_from_sessions(rows: list[dict]) -> list[dict]:
    cands = []
    for r in rows:
        text = r["content"]
        if not text or len(text) < 12:
            continue
        where = r["role"] or "?"
        for pat, (ptype, layer, impact) in MARKERS.items():
            m = re.search(pat, text, re.I)
            if not m:
                continue
            if ptype == "QUEUE_BLOCKED" and _is_dead_field_signature(text):
                continue
            snippet = text[max(0, m.start() - 120):m.end() + 220]
            cands.append({
                "source": f"session:{where}" + (f":{r['tool']}" if r["tool"] else ""),
                "session_id": r["session_id"],
                "pattern_type": ptype,
                "layer": layer,
                "impact": impact,
                "snippet": snippet.strip(),
                "signature": _normalise(f"{ptype}|{m.group(0).lower()}|{where}"),
            })
        if r["role"] == "user" and CORRECTION.search(text) and len(text) < 400:
            snippet = text[:400]
            cands.append({
                "source": "session:user-correction",
                "session_id": r["session_id"],
                "pattern_type": "HUMAN_BURDEN",
                "layer": "judgment",
                "impact": "sovereign_attention",
                "snippet": snippet.strip(),
                "signature": _normalise(f"HUMAN_BURDEN|{_correction_key(snippet)}"),
            })
    return cands


def _correction_key(text: str) -> str:
    """Group corrections by WHAT was corrected, not by the words used.

    Grouping on raw text made 33 near-duplicate atoms out of ordinary chat;
    grouping on the matched correction token plus the surrounding instruction
    keeps recurrence measurable without inflating it.
    """
    m = CORRECTION.search(text)
    token = m.group(0).lower() if m else "?"
    tail = re.sub(r"\W+", " ", text[m.end():m.end() + 60] if m else "").strip().lower()
    return f"{token}|{tail[:48]}"


def extract_from_scars() -> list[dict]:
    out = []
    if not os.path.isdir(SCAR_CANDIDATES):
        return out
    for name in sorted(os.listdir(SCAR_CANDIDATES)):
        if not name.endswith(".md") or ".dup-" in name:
            continue
        path = os.path.join(SCAR_CANDIDATES, name)
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        # A scar file often names its own failure class — scan it with the same
        # taxonomy before falling back to UNCLASSIFIED.
        ptype, layer, impact = "UNCLASSIFIED", "capability", "scar_recorded"
        for pat, (pt, ly, im) in MARKERS.items():
            if re.search(pat, text, re.I):
                ptype, layer, impact = pt, ly, im
                break
        out.append({
            "source": f"scar:{name}",
            "session_id": None,
            "pattern_type": ptype,
            "layer": layer,
            "impact": impact,
            "snippet": text[:400].strip(),
            "signature": _normalise(f"{ptype}|scar|{_scar_title(text)}"),
        })
    return out


def _scar_title(text: str) -> str:
    m = re.search(r"^#\s*(.+)$", text, re.M)
    return (m.group(1).strip() if m else text[:80])[:120]


def extract_from_eurekas() -> list[dict]:
    out = []
    if not os.path.isdir(CANON):
        return out
    for name in sorted(os.listdir(CANON)):
        if not name.startswith("EUREKA-") or not name.endswith(".md"):
            continue
        try:
            text = open(os.path.join(CANON, name), encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        out.append({
            "source": f"eureka:{name}",
            "session_id": None,
            "pattern_type": "UNCLASSIFIED",
            "layer": "judgment",
            "impact": "doctrine_candidate",
            "snippet": text[:400].strip(),
            "signature": _normalise(f"EUREKA|{name}|{text[:300]}"),
        })
    return out


def classify(cands: list[dict]) -> list[dict]:
    """Aggregate candidates into atoms. Frequency is measured, not asserted."""
    groups: dict[str, dict] = {}
    for c in cands:
        key = c["signature"]
        g = groups.setdefault(key, {
            "signature": key,
            "pattern_type": c["pattern_type"],
            "layer": c["layer"],
            "impact": c["impact"],
            "evidence": [],
            "sessions": [],
            "sources": [],
        })
        if len(g["evidence"]) < 5:
            g["evidence"].append({
                "layer": _evidence_layer(c["pattern_type"], c["source"]),
                "source": c["source"],
                "excerpt": c["snippet"][:300],
            })
        if c.get("session_id") and c["session_id"] not in g["sessions"]:
            g["sessions"].append(c["session_id"])
        if c["source"] not in g["sources"]:
            g["sources"].append(c["source"])

    built = []
    for g in groups.values():
        freq = len(g["sources"]) if g["sources"] else 1
        built.append(A.make_atom(
            signature=g["signature"],
            pattern_type=g["pattern_type"],
            layer=g["layer"],
            claim=_claim(g),
            evidence=g["evidence"],
            falsifier=_falsifier(g),
            actor="hermes-rsi-extractor",
            session_ids=g["sessions"],
            frequency=freq,
            impact=g["impact"],
            target=_target(g["pattern_type"]),
        ))
    built.sort(key=lambda a: (-a["frequency"], a["pattern_type"]))
    return built


def _evidence_layer(pattern_type: str, source: str) -> str:
    if source.startswith("scar:") or source.startswith("eureka:"):
        return "artifact"
    if pattern_type in ("PATH_DRIFT", "REGISTRY_MISMATCH", "DEAD_POINTER"):
        return "artifact"
    if pattern_type in ("SILENT_FAIL", "QUEUE_BLOCKED", "TRUNCATION_LOSS"):
        return "runtime"
    if pattern_type in ("PERMISSION_DRIFT",):
        return "security"
    if pattern_type in ("HUMAN_BURDEN", "SELF_EVAL", "PROXY_REALITY", "LAYER_MISMATCH"):
        return "authority"
    return "operational"


def _target(pattern_type: str) -> str:
    return {
        "PATH_DRIFT": "capability.path_discovery",
        "REGISTRY_MISMATCH": "capability.registry_truth",
        "DUPLICATE_SOT": "capability.single_source_of_truth",
        "DEAD_POINTER": "capability.reference_integrity",
        "QUEUE_BLOCKED": "capability.loop_exhale",
        "SILENT_FAIL": "capability.failure_surfacing",
        "SELF_EVAL": "capability.independent_verification",
        "PROXY_REALITY": "capability.layer_ownership",
        "LAYER_MISMATCH": "capability.layer_ownership",
        "HUMAN_BURDEN": "policy.sovereign_attention_floor",
        "RESOURCE_WASTE": "capability.inventory_completeness",
        "PERMISSION_DRIFT": "capability.authority_binding",
        "TRUNCATION_LOSS": "capability.evidence_completeness",
    }.get(pattern_type, "capability.unclassified")


def _claim(g: dict) -> str:
    return (f"{g['pattern_type']} observed {len(g['sources'])}x — "
            f"impact={g.get('impact','unknown')}. "
            f"First surface: {g['sources'][0] if g['sources'] else 'unknown'}")


def _falsifier(g: dict) -> str:
    return {
        "PATH_DRIFT": "Every cited path resolves on the live filesystem by exact name.",
        "REGISTRY_MISMATCH": "The live surface equals the declared registry, item for item.",
        "DUPLICATE_SOT": "One and only one artifact is read as authoritative for this fact.",
        "DEAD_POINTER": "Each cited reference resolves; the sweep reports zero dead pointers.",
        "QUEUE_BLOCKED": "The queue drains: processed count rises, no unit repeats in-window.",
        "SILENT_FAIL": "The failure surfaces as a non-zero exit or an explicit refusal.",
        "SELF_EVAL": "Producer identity != evaluator identity for this artifact.",
        "PROXY_REALITY": "The evidence class matches the claim class.",
        "LAYER_MISMATCH": "Claim layer == evidence layer for every item in the atom.",
        "HUMAN_BURDEN": "No sovereign-facing turn contains a terminal instruction.",
        "RESOURCE_WASTE": "Every paid/idle capability appears in the inventory sweep.",
        "PERMISSION_DRIFT": "Declared authority == effective authority at the live gate.",
        "TRUNCATION_LOSS": "The artifact is read whole; no silent head/tail cut.",
    }.get(g["pattern_type"], "A live probe contradicts the observation.")


def run(days: int = 7) -> list[dict]:
    rows = read_sessions(days)
    cands = extract_from_sessions(rows)
    cands += extract_from_scars()
    cands += extract_from_eurekas()
    return classify(cands)


if __name__ == "__main__":
    import sys
    d = int(sys.argv[sys.argv.index("--window") + 1].rstrip("d")) if "--window" in sys.argv else 7
    got = run(d)
    print(f"atoms={len(got)}")
    for a in got[:15]:
        print(f"  {a['pattern_type']:<18} layer={a['layer']:<10} freq={a['frequency']:<3} {a['atom_id']}")
