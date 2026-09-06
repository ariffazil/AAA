#!/usr/bin/env python3
"""Fixture test runner — AAA-video-emd-pipeline.

Two modes:
  --validate                     Self-test: fixture packages complete, media hashes match
                                 manifests, job requests validate against the frozen
                                 video-job schema. Works TODAY (no model calls).
  --evaluate FIXTURE_ID RESULT   Full assertion evaluation of a video_result.json against
                                 expected.assertions.yaml + video-result schema. Ready for
                                 the executor when it exists.

Both modes emit machine-readable receipts to tests/receipts/. Non-zero exit on failure.
Invariants are tested, never model prose (stochastic outputs get semantic conditions).
"""

import hashlib
import json
import sys
from pathlib import Path

import jsonschema
import yaml

HERE = Path(__file__).parent
SKILL = HERE.parent
SCHEMAS = SKILL / "schemas"
FIXTURES = HERE / "fixtures" / "video"
RECEIPTS = HERE / "receipts"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()}"


def load_fixture(fid):
    d = FIXTURES / fid
    return {
        "dir": d,
        "manifest": json.loads((d / "manifest.json").read_text()),
        "job": json.loads((d / "request.video-job.json").read_text()),
        "assertions": yaml.safe_load((d / "expected.assertions.yaml").read_text()),
        "f12": json.loads((d / "expected.f12.json").read_text()),
    }


def get_path(obj, path):
    """Dot-notation lookup. Returns (found, value)."""
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return False, None
    return True, cur


def check_cond(obj, cond):
    found, val = get_path(obj, cond["path"])
    op, want = cond["op"], cond.get("value")
    if op == "exists":
        return found
    if not found:
        return False
    if op == "eq":
        return val == want
    if op == "ne":
        return val != want
    if op == "gte":
        return val is not None and val >= want
    if op == "lte":
        return val is not None and val <= want
    if op == "prefix":
        return isinstance(val, str) and val.startswith(want)
    raise ValueError(f"unknown op {op}")


def evaluate_claims(result, claims_spec):
    """Semantic claim-block evaluation."""
    failures = []
    claims = result.get("claims", [])
    material = [
        c for c in claims if c.get("evidence_ids")
    ]  # material = has evidence refs
    if claims_spec.get("any_class"):
        if not any(c.get("class") == claims_spec["any_class"] for c in claims):
            failures.append(f"no claim of class {claims_spec['any_class']}")
    if claims_spec.get("material_time_range") == "all":
        for c in material:
            tr = c.get("time_range_s")
            if not (
                isinstance(tr, list)
                and len(tr) == 2
                and all(isinstance(x, (int, float)) for x in tr)
            ):
                failures.append(
                    f"material claim {c.get('claim_id')} missing time_range_s"
                )
    if claims_spec.get("material_evidence_ids") == "all":
        for c in claims:
            if c.get("time_range_s") and not c.get("evidence_ids"):
                failures.append(
                    f"claim {c.get('claim_id')} has time_range but no evidence_ids"
                )
    caps = claims_spec.get("max_confidence_by_class", {})
    for c in claims:
        cls = c.get("class")
        if cls in caps and c.get("confidence", 1.0) > caps[cls]:
            failures.append(
                f"claim {c.get('claim_id')} class {cls} conf {c.get('confidence')} > cap {caps[cls]}"
            )
        text = (c.get("text") or "").lower()
        if "causal_INT" in caps and any(
            w in text for w in (" caused ", "caused the", "resulted in")
        ):
            if c.get("confidence", 1.0) > caps["causal_INT"]:
                failures.append(
                    f"causal claim {c.get('claim_id')} conf > {caps['causal_INT']}"
                )
    for forbid in claims_spec.get("forbid", []):
        if forbid == "fabricated_transcript_no_audio_track":
            if result.get("evidence", {}).get("transcript_segments", 0) > 0:
                failures.append(
                    "transcript segments present on silent (no-audio) fixture"
                )
    return failures


def validate_mode():
    job_schema = json.loads((SCHEMAS / "video-job.schema.json").read_text())
    fixture_ids = sorted(p.name for p in FIXTURES.iterdir() if p.is_dir())
    summary = {"mode": "validate", "fixtures": [], "pass": 0, "fail": 0}
    for fid in fixture_ids:
        fx = load_fixture(fid)
        errors = []
        media = fx["dir"] / "source.mp4"
        if not media.exists():
            errors.append("source.mp4 missing")
        elif sha256(media) != fx["manifest"]["asset_sha256"]:
            errors.append("media hash mismatch vs manifest")
        try:
            jsonschema.validate(fx["job"], job_schema)
        except jsonschema.ValidationError as e:
            errors.append(f"job schema: {e.message}")
        if not fx["assertions"].get("must"):
            errors.append("assertions empty")
        rec = {
            "fixture": fid,
            "status": fx["manifest"]["fixture_status"],
            "ok": not errors,
            "errors": errors,
        }
        summary["fixtures"].append(rec)
        summary["pass" if not errors else "fail"] += 1 if errors else 0
        summary["pass"] += 0 if errors else 1
        print(
            f"  {'PASS' if not errors else 'FAIL'}  {fid} [{rec['status']}]"
            + (f" — {errors}" if errors else "")
        )
    RECEIPTS.mkdir(exist_ok=True)
    (RECEIPTS / "validate-summary.json").write_text(json.dumps(summary, indent=2))
    print(
        f"\nvalidate: {summary['pass']} pass / {summary['fail']} fail — receipt: tests/receipts/validate-summary.json"
    )
    return 0 if summary["fail"] == 0 else 1


def evaluate_mode(fid, result_path):
    result_schema = json.loads((SCHEMAS / "video-result.schema.json").read_text())
    fx = load_fixture(fid)
    result = json.loads(Path(result_path).read_text())
    errors = []
    try:
        jsonschema.validate(result, result_schema)
    except jsonschema.ValidationError as e:
        errors.append(f"result schema: {e.message}")
    probe = dict(result)
    probe["schema_valid"] = not errors
    for cond in fx["assertions"]["must"]:
        if not check_cond(probe, cond):
            errors.append(f"must failed: {cond}")
    errors += evaluate_claims(result, fx["assertions"].get("claims", {}))
    f12 = fx["f12"]
    spans = result.get("evidence", {}).get("f12_quarantined_spans", [])
    if f12["expect_quarantined_spans_nonempty"] and not spans:
        errors.append("F12: expected quarantined spans, got none")
    if not f12["expect_quarantined_spans_nonempty"] and spans:
        errors.append(f"F12: unexpected quarantined spans {spans}")
    rec = {
        "fixture": fid,
        "result": str(result_path),
        "ok": not errors,
        "errors": errors,
    }
    RECEIPTS.mkdir(exist_ok=True)
    (RECEIPTS / f"{fid}.evaluate.json").write_text(json.dumps(rec, indent=2))
    print(json.dumps(rec, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    if "--validate" in sys.argv:
        sys.exit(validate_mode())
    if "--evaluate" in sys.argv:
        i = sys.argv.index("--evaluate")
        sys.exit(evaluate_mode(sys.argv[i + 1], sys.argv[i + 2]))
    print(__doc__)
    sys.exit(2)
