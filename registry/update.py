#!/usr/bin/env python3
"""
aaa-registry update — bounded agentic update loop for the AAA model supply-chain registry.

Loop:  DISCOVER -> PROBE -> RECONCILE -> VALIDATE -> PROPOSE -> (AUTHORIZE) -> (PUBLISH) -> WITNESS

Authority stops (hard):
  - AUTHORIZE is NEVER self-issued. The updater prepares and validates patches;
    only F13 SOVEREIGN (human) authorizes. There is no authorize verb here.
  - PUBLISH runs only through the governed git-lane + mirror-cycle path, by hand.
  - The updater NEVER mutates production routing, never auto-promotes a model into
    consequential roles, never creates constitutional authorization.

Usage:
  python3 registry/update.py discover
  python3 registry/update.py probe --route zai-coding-openai --model glm-5.3 [--marker PONG] [--models-only]
  python3 registry/update.py reconcile
  python3 registry/update.py validate
  python3 registry/update.py propose [--out FILE]
  python3 registry/update.py witness [--remote origin] [--branch main]

Secrets: credential values are read from env vars named in routes/*.yaml
(credential_env_refs) and are never printed, hashed, committed or logged.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import yaml

REGISTRY = Path(__file__).parent
sys.path.insert(0, str(REGISTRY))
import compile as regcompile  # noqa: E402  (loaders + checks reused deliberately)

PROBE_DIR = REGISTRY / "probes"


# ── verdict grammar (policies/probe-verdict-grammar-v1) ────────────────────────

def verdict_for(requested: str, resolved, http_status, output_validity: dict,
                expected_marker, known_remaps) -> str:
    """Pure verdict function — the single source for probe classification.

    PASS  : 200 + core validity + identity echo (or exact witnessed known_remap -> WARN)
    WARN  : exact match to a known_remaps entry on this route. Nothing else.
    FAIL  : non-200, or 200 with empty/invalid output (empty success is FAIL).
    HOLD  : undocumented resolution mismatch, or unresolved identity on floating alias.
    """
    core_valid = all(bool(output_validity.get(k)) for k in ("non_empty", "schema_valid", "finish_state_valid"))
    marker_required = expected_marker is not None
    marker_ok = (not marker_required) or bool(output_validity.get("expected_marker_present"))

    if http_status != 200:
        return "FAIL"
    if not core_valid:
        return "FAIL"  # regression case C: 200 with empty output

    if resolved is None or resolved != requested:
        remap = None
        for kr in known_remaps or []:
            if kr.get("from") == requested and kr.get("to") == resolved:
                remap = kr
                break
        if remap is not None:
            return "WARN"  # regression case A
        return "HOLD"      # regression case B: undocumented / silent upgrade

    if not marker_ok:
        return "FAIL"
    return "PASS"


def _known_remaps_for(route_ref: str, requested: str) -> list[dict]:
    out = []
    for fp in sorted((REGISTRY / "aliases").glob("*.yaml")):
        a = yaml.safe_load(fp.read_text()) or {}
        if a.get("route_ref") == route_ref or a.get("route_ref") is None:
            out.extend(a.get("known_remaps") or [])
    return out


def _receipt_hash(record: dict) -> str:
    clean = {k: v for k, v in record.items() if k != "receipt_hash"}
    canonical = json.dumps(clean, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ── discover ───────────────────────────────────────────────────────────────────

def cmd_discover(args) -> int:
    entities = regcompile.load_entities()
    sot = Path("/root/.config/federation-models.json")
    print("== DISCOVER ==")
    for d, v in entities.items():
        print(f"  {d}: {len(v)}")
    print(f"  live SOT present: {sot.exists()} ({sot})")
    if sot.exists():
        data = json.loads(sot.read_text())
        provs = data.get("providers", [])
        known = {r.get("endpoint_ref") for r in entities.get("routes", [])}
        print(f"  SOT providers: {len(provs)}; endpoints not covered by registry routes:")
        for p in provs:
            ep = p.get("endpoint_url") or ""
            if ep and ep not in known:
                print(f"    - {p.get('provider_id')}: {ep}")
    print("  catalog files:", len(list((REGISTRY / 'catalog').glob('*.yaml'))) if (REGISTRY / 'catalog').exists() else 0)
    return 0


# ── probe ─────────────────────────────────────────────────────────────────────

def _route(route_id: str) -> dict:
    for fp in sorted((REGISTRY / "routes").glob("*.yaml")):
        r = yaml.safe_load(fp.read_text()) or {}
        if r.get("route_id") == route_id:
            return r
    raise SystemExit(f"unknown route_id: {route_id}")


def _first_available_credential(route: dict):
    for env_name in route.get("credential_env_refs", []):
        val = os.environ.get(env_name)
        if val:
            return env_name, val
    return None, None


def cmd_probe(args) -> int:
    route = _route(args.route)
    endpoint = route.get("endpoint_ref")
    if not endpoint or endpoint == "UNKNOWN":
        print(f"HOLD: route '{args.route}' has no usable endpoint")
        return 2
    cred_name, cred = _first_available_credential(route)
    if route.get("credential_env_refs") and not cred:
        print(f"HOLD: no credential env present ({', '.join(route['credential_env_refs'])}) — refusing to probe with guessed auth")
        return 2

    marker = args.marker
    t0 = time.time()
    http_status, body = None, None
    requested = args.model
    resolved = None
    validity = {"non_empty": False, "schema_valid": False, "finish_state_valid": False, "expected_marker_present": False}
    note = ""

    try:
        if args.models_only:
            url = endpoint.rstrip("/") + "/models"
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {cred}"} if cred else {})
            with urllib.request.urlopen(req, timeout=30) as resp:
                http_status = resp.status
                body = json.loads(resp.read().decode("utf-8"))
            validity["non_empty"] = bool(body.get("data"))
            validity["schema_valid"] = isinstance(body.get("data"), list)
            validity["finish_state_valid"] = True
            resolved = "(models-list)"
            note = "AUTH_VALID / CATALOG_REACHABLE only — NOT inference-alive"
        else:
            url = endpoint.rstrip("/") + "/chat/completions"
            payload = {
                "model": requested,
                "messages": [{"role": "user", "content": f"Reply with exactly this marker and nothing else: {marker or 'PONG'}"}],
                "max_tokens": 2048,
                "stream": False,
            }
            req = urllib.request.Request(
                url, data=json.dumps(payload).encode("utf-8"), method="POST",
                headers={"Content-Type": "application/json", **({"Authorization": f"Bearer {cred}"} if cred else {})},
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                http_status = resp.status
                body = json.loads(resp.read().decode("utf-8"))
            choice = (body.get("choices") or [{}])[0]
            message = choice.get("message") or {}
            content = message.get("content") or ""
            validity["non_empty"] = bool(content.strip())
            validity["schema_valid"] = bool(body.get("choices")) and "message" in choice
            finish = choice.get("finish_reason")
            validity["finish_state_valid"] = finish == "stop"
            if marker:
                validity["expected_marker_present"] = marker in content
            resolved = body.get("model") or (body.get("system_fingerprint") and f"fp:{body['system_fingerprint']}")
            note = f"finish_reason={finish}"
    except urllib.error.HTTPError as e:
        http_status = e.code
        note = f"http_error: {e.code}"
    except Exception as e:  # noqa: BLE001
        note = f"error: {type(e).__name__}"
        http_status = http_status or 0

    latency_ms = int((time.time() - t0) * 1000)
    kr = _known_remaps_for(args.route, requested)
    verdict = verdict_for(requested, resolved, http_status, validity, marker, kr)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dt%H%M%Sz")
    slug = re.sub(r"[^a-z0-9-]+", "-", f"{args.route}-{requested}".lower()).strip("-")
    probe_id = f"probe-{ts}-{slug}"
    record = {
        "schema_version": 1,
        "probe_id": probe_id,
        "route_ref": args.route,
        "requested_model": requested,
        "resolved_model": resolved,
        "http_status": http_status,
        "output_validity": validity,
        "expected_marker": marker,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "latency_ms": latency_ms,
        "response_fingerprint": (body or {}).get("system_fingerprint") if isinstance(body, dict) else None,
        "receipt_hash": None,
        "verdict": verdict,
        "evidence_status": "live",
        "evidence_refs": [f"live probe by {os.environ.get('ARIFOS_AGENT_ID', 'agent-unknown')}"],
        "notes": note,
    }
    record["receipt_hash"] = _receipt_hash(record)

    dest = PROBE_DIR / f"{probe_id}.yaml"
    if dest.exists():
        print("HOLD: probe id collision — probes/ is append-only")
        return 2
    PROBE_DIR.mkdir(parents=True, exist_ok=True)
    dest.write_text(yaml.safe_dump(record, sort_keys=True, allow_unicode=True), encoding="utf-8")

    print(json.dumps({
        "probe_id": probe_id, "route": args.route, "requested": requested,
        "resolved": resolved, "http_status": http_status, "verdict": verdict,
        "latency_ms": latency_ms, "receipt": dest.name,
    }, ensure_ascii=False))
    return 0 if verdict in ("PASS", "WARN") else 1


# ── reconcile ──────────────────────────────────────────────────────────────────

def cmd_reconcile(args) -> int:
    entities = regcompile.load_entities()
    latest: dict[str, dict] = {}
    for p in sorted(entities.get("probes", []), key=lambda x: x.get("observed_at", "")):
        latest[p.get("route_ref")] = p

    print("== RECONCILE: declared vs catalog vs requested vs resolved ==")
    bad = 0
    for a in entities.get("aliases", []):
        rid = a.get("route_ref")
        req = a.get("requested_model")
        exp = a.get("expected_resolution")
        pr = latest.get(rid) if rid else None
        if not pr or pr.get("requested_model") != req:
            status = "NO_PROBE_FOR_ALIAS"
            bad += 1
        else:
            got = pr.get("resolved_model")
            if got == req:
                status = "MATCH"
            elif got == exp and (a.get("resolution_policy") in ("known_remap", "known_compat")):
                status = "WARN_CLASSIFIED"
            else:
                status = f"MISMATCH(got={got})"
                bad += 1
        print(f"  [{status:>22}] {a.get('alias_id')}: requested={req} expected={exp}")
    for r in entities.get("routes", []):
        pr = latest.get(r.get("route_id"))
        print(f"  route {r.get('route_id')}: latest_probe={pr.get('probe_id') if pr else 'NONE'} verdict={pr.get('verdict') if pr else '-'}")
    print(f"reconcile issues: {bad}")
    return 0 if bad == 0 else 1


# ── validate ───────────────────────────────────────────────────────────────────

def cmd_validate(args) -> int:
    print("== VALIDATE (schema / refs / duplicates / conflation / secrets / append-only) ==")
    entities = regcompile.load_entities()
    errors = (
        regcompile.validate_entity_schemas(entities)
        + regcompile.check_duplicate_ids(entities)
        + regcompile.check_references(entities)
        + regcompile.check_conflation(entities)
        + regcompile.check_secrets()
        + regcompile.check_probe_append_only(entities)
    )
    for e in errors:
        print(f"  ❌ {e}")
    print(f"errors: {len(errors)}")
    return 0 if not errors else 1


# ── propose ────────────────────────────────────────────────────────────────────

def cmd_propose(args) -> int:
    print("== PROPOSE (patch preview — authorization is NOT self-issued) ==")
    try:
        st = subprocess.run(["git", "-C", str(REGISTRY), "status", "--porcelain", "--", "registry"],
                            capture_output=True, text=True, timeout=15, check=True).stdout
        diff = subprocess.run(["git", "-C", str(REGISTRY), "diff", "--stat", "--", "registry"],
                              capture_output=True, text=True, timeout=15, check=True).stdout
    except Exception as e:  # noqa: BLE001
        print(f"HOLD: git introspection failed: {e}")
        return 2
    out = ["registry/ working-tree state:", st or "  (clean)", "", "diff --stat:", diff or "  (none)"]
    text = "\n".join(out)
    print(text)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"\nproposal written: {args.out}")
    print("\nNEXT: human (F13) authorizes -> git-lane commit -> mirror-cycle publish -> witness")
    return 0


# ── witness ────────────────────────────────────────────────────────────────────

def cmd_witness(args) -> int:
    print("== WITNESS (post-publish verification) ==")
    ok = True
    try:
        local = subprocess.run(["git", "-C", str(REGISTRY), "rev-parse", "HEAD"],
                               capture_output=True, text=True, timeout=15, check=True).stdout.strip()
        remote = subprocess.run(["git", "-C", str(REGISTRY), "ls-remote", args.remote, f"refs/heads/{args.branch}"],
                                capture_output=True, text=True, timeout=30, check=True).stdout.split()[0]
        match = local == remote
        print(f"  local  HEAD: {local}")
        print(f"  remote {args.branch}: {remote}")
        print(f"  push parity: {'OK' if match else 'MISMATCH'}")
        ok = ok and match
    except Exception as e:  # noqa: BLE001
        print(f"  HOLD: remote introspection failed: {e}")
        ok = False

    manifest_p = REGISTRY / "compiled" / "manifest.json"
    if manifest_p.exists():
        manifest = json.loads(manifest_p.read_text())
        for name, want in manifest.get("hashes", {}).items():
            fp = REGISTRY / ("generated" / name if name.startswith(("catalog", "provider", "family", "route", "agent", "freshness", "drift")) else "compiled" / name)
            if fp.exists():
                got = regcompile.content_hash(fp.read_text(encoding="utf-8"))
                status = "OK" if got == want else "HASH-MISMATCH"
                if got != want:
                    ok = False
                print(f"  {name}: {status}")
    print("WITNESS:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(prog="aaa-registry update")
    sub = ap.add_subparsers(dest="verb", required=True)
    sub.add_parser("discover").set_defaults(fn=cmd_discover)

    p = sub.add_parser("probe")
    p.add_argument("--route", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--marker", default=None)
    p.add_argument("--models-only", action="store_true")
    p.set_defaults(fn=cmd_probe)

    sub.add_parser("reconcile").set_defaults(fn=cmd_reconcile)
    sub.add_parser("validate").set_defaults(fn=cmd_validate)

    p = sub.add_parser("propose")
    p.add_argument("--out", default=None)
    p.set_defaults(fn=cmd_propose)

    p = sub.add_parser("witness")
    p.add_argument("--remote", default="origin")
    p.add_argument("--branch", default="main")
    p.set_defaults(fn=cmd_witness)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
