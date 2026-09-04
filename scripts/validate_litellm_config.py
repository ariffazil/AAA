#!/usr/bin/env python3
# validate_litellm_config.py — Read-only validator for FED LiteLLM config integrity.
import sys
import yaml
import hashlib
import json
from pathlib import Path

MANIFEST_PATH = Path("/root/.config/federation-models.json")
PRIMARY_PATH = Path("/root/A-FORGE/litellm-config.yaml")
DEPLOY_PATH = Path("/root/A-FORGE/deploy/fed/litellm-config.yaml")
CONTRACT_PATH = Path("/root/AAA/canon/FEDERATION_CONFIG_CONTRACT.v1.json")

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def inspect_config(path: Path):
    if not path.exists():
        return False, f"File not found: {path}", {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return False, f"YAML parse error in {path}: {e}", {}

    if not isinstance(data, dict):
        return False, f"Expected dict root in {path}", {}

    model_list = data.get("model_list", [])
    active_gemini = 0
    total_active_models = len(model_list)

    for item in model_list:
        if not isinstance(item, dict):
            continue
        params = item.get("litellm_params", {})
        model_target = str(params.get("model", "")).lower()
        if "gemini" in model_target:
            active_gemini += 1

    router_settings = data.get("router_settings", {})
    fallbacks = router_settings.get("fallbacks", [])
    model_group_alias = router_settings.get("model_group_alias", {})

    gemini_fallbacks = 0
    for fb in fallbacks:
        if isinstance(fb, dict):
            for k, v in fb.items():
                if "gemini" in str(k).lower() or any("gemini" in str(x).lower() for x in (v if isinstance(v, list) else [v])):
                    gemini_fallbacks += 1

    gemini_aliases = 0
    for k, v in model_group_alias.items():
        if "gemini" in str(k).lower() or "gemini" in str(v).lower():
            gemini_aliases += 1

    summary = {
        "file": str(path),
        "sha256": sha256_file(path),
        "total_active_models": total_active_models,
        "active_gemini_count": active_gemini,
        "gemini_aliases": gemini_aliases,
        "gemini_fallback_references": gemini_fallbacks
    }

    if active_gemini > 0:
        return False, f"Invariant violation: active_gemini_count={active_gemini} in {path}", summary
    if gemini_aliases > 0:
        return False, f"Invariant violation: gemini_aliases={gemini_aliases} in {path}", summary
    if gemini_fallbacks > 0:
        return False, f"Invariant violation: gemini_fallbacks={gemini_fallbacks} in {path}", summary

    return True, "OK", summary

def main():
    print("=== FED LiteLLM Configuration Validator ===")
    all_ok = True
    summaries = []

    for path in [PRIMARY_PATH, DEPLOY_PATH]:
        ok, msg, summary = inspect_config(path)
        summaries.append(summary)
        status_str = "PASS" if ok else "FAIL"
        print(f"[{status_str}] {path.name}: {msg}")
        if not ok:
            all_ok = False

    if CONTRACT_PATH.exists():
        try:
            with open(CONTRACT_PATH) as f:
                contract = json.load(f)
            sot = contract.get("source_of_truth", {})
            manifest_hash = sha256_file(MANIFEST_PATH)
            primary_hash = sha256_file(PRIMARY_PATH)
            deploy_hash = sha256_file(DEPLOY_PATH)

            manifest_match = manifest_hash == sot.get("manifest_sha256")
            primary_match = primary_hash == sot.get("litellm_primary_sha256")
            deploy_match = deploy_hash == sot.get("litellm_deploy_sha256")

            if manifest_match and primary_match and deploy_match:
                print(f"[PASS] 3/3 SOT contract hash parity verified against {CONTRACT_PATH.name}")
                print(f"       - manifest: {manifest_hash}")
                print(f"       - primary : {primary_hash}")
                print(f"       - deploy  : {deploy_hash}")
            else:
                all_ok = False
                print(f"[FAIL] Contract hash mismatch:")
                if not manifest_match:
                    print(f"       - manifest: {manifest_hash} != {sot.get('manifest_sha256')}")
                if not primary_match:
                    print(f"       - primary : {primary_hash} != {sot.get('litellm_primary_sha256')}")
                if not deploy_match:
                    print(f"       - deploy  : {deploy_hash} != {sot.get('litellm_deploy_sha256')}")
        except Exception as e:
            print(f"[WARN] Contract validation check error: {e}")
            all_ok = False

    print("\nSummary:")
    print(json.dumps(summaries, indent=2))

    if not all_ok:
        sys.exit(1)
    print("\nAll constitutional routing invariants and SOT hashes VERIFIED.")
    sys.exit(0)

if __name__ == "__main__":
    main()
