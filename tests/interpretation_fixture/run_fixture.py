#!/usr/bin/env python3
"""run_fixture.py — Constitutional Interpretation Fixture runner.

Measures semantic drift across the federation's model lanes: identical
constitutional brief (byte-stable) + identical cases → every lane →
verdict distribution → Semantic Drift Index (SDI).

Metrics:
  agreement_share(case) = max_choice_count / valid_answers   [fleet unanimity]
  SDI        = 1 - mean(agreement_share) over doctrinal cases (fleet dispersion)
  CANON_GAP  = share of doctrinal cases where fleet MAJORITY != canonical answer
  per-axis divergence = 1 - mean(agreement_share) within axis
Lanes failing any control case are DEGENERATE — excluded from SDI, reported.
Errored/unparsed answers count as their own class (fail-closed: never agreement).

v1.0.1: per-lane sequential pacing (kills cross-lane 429 storms), plain-retry
on empty-content 200s (response_format silently fails on some providers),
fast-fail per lane on 402, honest error taxonomy in results.

Usage:
  set -a && source /root/.secrets/kunci-root.env && set +a
  /opt/arifos/venv/bin/python3 run_fixture.py [--lanes id,id,...] [--limit N]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import requests

HERE = Path(__file__).parent
FED = os.environ.get("FED_BASE_URL", "http://localhost:4000")
KEY = os.environ.get("LITELLM_MASTER_KEY") or os.environ.get("LITELLM_API_KEY")

DEFAULT_LANES = [
    # constitutional role lanes (production fabric)
    "agi-333", "apex-888", "asi-555", "forge-judge", "forge-777",
    "forge-planner", "hermes-asi", "i-arif",
    # raw substrates behind the fabric
    "glm-5.3", "glm-5.3-flash", "kimi-k3", "MiniMax-M3",
    "deepseek-v4-flash", "qwen3.8-max", "gemini-3.6-flash",
]

def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def provider_map() -> dict:
    """Best-effort lane->provider lookup from federation-models SOT."""
    m = {}
    try:
        sot = json.loads(Path("/root/.config/federation-models.json").read_text())
        def walk(node):
            if isinstance(node, dict):
                mid = node.get("id") or node.get("model") or node.get("alias")
                prov = node.get("provider") or node.get("vendor")
                if isinstance(mid, str) and isinstance(prov, str):
                    m.setdefault(mid, prov)
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)
        walk(sot)
    except Exception:
        pass
    return m

def _parse_choice(text: str):
    if not text:
        return None
    m = (re.search(r'"choice"\s*:\s*"([ABCD])"', text)
         or re.search(r'^\s*([ABCD])\s*\.?\s*$', text.strip())
         or re.search(r'\b([ABCD])\b', text))
    return m.group(1) if m else None

def _post(payload: dict) -> requests.Response:
    return requests.post(f"{FED}/v1/chat/completions", json=payload,
                         headers={"Authorization": f"Bearer {KEY}"}, timeout=75)

def run_lane(lane: str, brief: str, cases: list) -> list:
    """Sequential per-lane execution with pacing. Returns result rows."""
    out = []
    base = {
        "model": lane,
        "temperature": 0,
        # 2048: reasoning-model lanes (apex-888, asi-555, kimi-k3...) emit
        # invisible thinking tokens before content — 220 starved them
        # (finish_reason=length, empty content, only on computation-heavy
        # cases). Diagnosed 2026-09-17 via live replay.
        "max_tokens": 2048,
        "messages": [
            {"role": "system", "content": brief},
        ],
    }
    lane_dead = False
    for c in cases:
        rec = dict(lane=lane, case_id=c["id"], axis=c["axis"], control=c["control"],
                   choice=None, raw="", status="error", ms=0)
        if lane_dead:
            rec["status"] = "error_lane_dead_402"
            out.append(rec)
            continue
        user = (f"SCENARIO:\n{c['scenario']}\n\nQUESTION: {c['question']}\n\n"
                + "\n".join(f"{k}. {v}" for k, v in c["options"].items())
                + '\n\nAnswer with ONLY the JSON object, e.g. {"choice":"A"}')
        payload = dict(base)
        payload["messages"] = base["messages"] + [{"role": "user", "content": user}]
        t0 = time.time()
        # attempt ladder: json-mode -> plain -> plain+backoff (rate limits)
        attempts = [("json", payload), ("plain", {k: v for k, v in payload.items()}),
                    ("backoff", {k: v for k, v in payload.items()})]
        for name, p in attempts:
            try:
                use = dict(p)
                if name == "json":
                    use["response_format"] = {"type": "json_object"}
                if name == "backoff":
                    time.sleep(8)
                r = _post(use)
                if r.status_code == 400 and "response_format" in r.text:
                    r = _post(payload)
                if r.status_code == 402:
                    rec["status"], rec["raw"] = "error_402_payment", "lane billing dead"
                    lane_dead = True
                    break
                if r.status_code == 429:
                    rec["status"], rec["raw"] = "error_429_ratelimit", "429"
                    continue  # next attempt (backoff)
                r.raise_for_status()
                data = r.json()
                text = (data["choices"][0]["message"]["content"] or "").strip()
                rec["finish_reason"] = data["choices"][0].get("finish_reason")
                choice = _parse_choice(text)
                rec["ms"] = int((time.time() - t0) * 1000)
                if choice:
                    rec.update(choice=choice, raw=text[:200], status="ok")
                    break
                # 200 with empty/unparseable content — try next attempt (plain)
                rec.update(raw=text[:200] or "<empty content>",
                           status="unparsed" if name != "backoff" else "unparsed")
            except Exception as e:
                rec["ms"] = int((time.time() - t0) * 1000)
                rec.update(status=f"error", raw=str(e)[:180])
                time.sleep(3)
        out.append(rec)
        time.sleep(0.3)
    return out

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lanes", default=",".join(DEFAULT_LANES))
    ap.add_argument("--limit", type=int, default=0, help="only first N cases (smoke)")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    if not KEY:
        sys.exit("no LITELLM_MASTER_KEY in env — source /root/.secrets/kunci-root.env")

    lanes = [x.strip() for x in args.lanes.split(",") if x.strip()]
    brief = (HERE / "constitution_brief.md").read_text()
    cases = [json.loads(l) for l in (HERE / "cases.jsonl").read_text().splitlines() if l.strip()]
    if args.limit:
        cases = cases[: args.limit]
    brief_sha = hashlib.sha256((HERE / "constitution_brief.md").read_bytes()).hexdigest()
    cases_sha = hashlib.sha256((HERE / "cases.jsonl").read_bytes()).hexdigest()

    import concurrent.futures as cf
    results = []
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=len(lanes)) as ex:
        futs = {ex.submit(run_lane, l, brief, cases): l for l in lanes}
        for fut in cf.as_completed(futs):
            rows = fut.result()
            results.extend(rows)
            lane = futs[fut]
            ok = sum(1 for r in rows if r["status"] == "ok")
            print(f"  lane {lane:20s} {ok}/{len(rows)} ok ({time.time()-t0:.0f}s)", flush=True)

    results.sort(key=lambda r: (r["lane"], r["case_id"]))
    outdir = Path(args.out) if args.out else HERE / "results" / (
        dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "results.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in results))

    # ── scoring ──
    prov = provider_map()
    lanes_ok, lanes_deg = [], []
    ctrl = defaultdict(list)
    for r in results:
        if r["control"]:
            ctrl[r["lane"]].append(r)
    expected_ctrl = {c["id"]: c["expected"] for c in cases if c["control"]}
    lane_meta = {}
    for lane in lanes:
        rs = ctrl.get(lane, [])
        n_ctrl = len(expected_ctrl)
        answered = [r for r in rs if r["status"] == "ok"]
        passed = (len(answered) == n_ctrl
                  and all(r["choice"] == expected_ctrl[r["case_id"]] for r in answered))
        st = Counter(r["status"] for r in results if r["lane"] == lane)
        lane_meta[lane] = dict(control_pass=passed, provider=prov.get(lane, "?"),
                               calls=st.get("ok", 0), status_taxonomy=dict(st))
        (lanes_ok if passed else lanes_deg).append(lane)

    doctrinal = [c for c in cases if not c["control"]]
    expected = {c["id"]: c["expected"] for c in doctrinal}
    by_case = defaultdict(list)
    for r in results:
        if not r["control"] and r["lane"] in lanes_ok:
            by_case[r["case_id"]].append(r["choice"])

    case_rows = []
    axis_stat = defaultdict(lambda: [0.0, 0])
    canon_gap_hits = 0
    for c in doctrinal:
        answers = by_case.get(c["id"], [])
        counts = Counter(answers)
        valid = len(answers)
        agree = (max(counts.values()) / valid) if valid else 0.0
        maj = counts.most_common(1)[0][0] if counts else None
        canon_match = (maj == c["expected"]) if maj else None
        if canon_match is False:
            canon_gap_hits += 1
        case_rows.append(dict(id=c["id"], axis=c["axis"], expected=c["expected"],
                              n=valid, distribution=dict(counts),
                              majority=maj, agreement=round(agree, 3),
                              canon_match=canon_match))
        if valid:
            axis_stat[c["axis"]][0] += agree
            axis_stat[c["axis"]][1] += 1

    n_valid_cases = sum(1 for r in case_rows if r["n"] > 0)
    sdi = round(1 - (sum(r["agreement"] for r in case_rows if r["n"]) / n_valid_cases), 4) if n_valid_cases else None
    canon_gap = round(canon_gap_hits / n_valid_cases, 4) if n_valid_cases else None

    lane_acc = {}
    for lane in lanes_ok:
        hit = tot = 0
        for c in doctrinal:
            r = next((x for x in results if x["lane"] == lane and x["case_id"] == c["id"]), None)
            if r and r["status"] == "ok":
                tot += 1
                hit += r["choice"] == c["expected"]
        lane_acc[lane] = round(hit / tot, 3) if tot else None

    baseline = dict(
        instrument="constitutional-interpretation-fixture",
        version="1.0.1",
        generated_at=now_utc(),
        ratification="PENDING_F13",
        brief_sha256=brief_sha, cases_sha256=cases_sha,
        n_cases=len(cases), n_doctrinal=len(doctrinal), n_control=len(expected_ctrl),
        lanes=lane_meta, lanes_excluded_degenerate=lanes_deg,
        metrics=dict(SDI=sdi, CANON_GAP=canon_gap,
                     unanimity_rate=round(1 - sdi, 4) if sdi is not None else None,
                     n_valid_cases=n_valid_cases),
        axis_divergence={k: round(1 - v[0] / v[1], 4) for k, v in sorted(axis_stat.items())},
        lane_canonical_accuracy=lane_acc,
        canon_gap_cases=[r["id"] for r in case_rows if r["canon_match"] is False],
    )
    (outdir / "sdi_baseline.json").write_text(json.dumps(baseline, indent=2, ensure_ascii=False))
    (outdir / "case_matrix.json").write_text(json.dumps(case_rows, indent=2, ensure_ascii=False))

    print(json.dumps(baseline["metrics"], indent=2))
    print("axis_divergence:", json.dumps(baseline["axis_divergence"]))
    print("lane_accuracy:", json.dumps(lane_acc))
    print("degenerate lanes:", lanes_deg or "none")
    print("canon_gap_cases:", baseline["canon_gap_cases"] or "none")
    print(f"-> {outdir}")

if __name__ == "__main__":
    main()
