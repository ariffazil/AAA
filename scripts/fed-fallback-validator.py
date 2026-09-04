#!/usr/bin/env python3
"""
fed.fallback.v1 validator — T0.6 ledger FED-ZEN-TASK-LEDGER-001
Disiplin LiteLLM pada rantaian federasi: sasaran-wujud / tiada-sendiri / tiada-dupe / semakan-lesen.
READ-ONLY terhadap SOT + litellm-config. Keluaran: laporan JSON + manusia-baca.
Penggunaan: python3 fed-fallback-validator.py [--json]
"""
import json, sys, re, yaml, collections

SOT = "/root/.config/federation-models.json"
LITELLM = "/root/A-FORGE/litellm-config.yaml"

def load_sot():
    d = json.load(open(SOT))
    models = {m["model_key"] for m in d.get("models", [])}
    routes = d.get("model_routes", {})
    # upstream bare names juga sah (litellm rung guna nama hulu)
    providers = {p["provider_id"] for p in d.get("providers", [])}
    return d, models, routes, providers

def load_litellm():
    cfg = yaml.safe_load(open(LITELLM))
    groups = collections.defaultdict(list)
    for ml in cfg.get("model_list", []):
        mg = str(ml.get("model_name", ""))
        m = str(ml.get("litellm_params", {}).get("model", ""))
        envkey = str(ml.get("litellm_params", {}).get("api_key", ""))
        groups[mg].append({"upstream": m, "env_key": envkey})
    return cfg, groups

def main():
    sot, sot_models, routes, providers = load_sot()
    cfg, groups = load_litellm()
    findings = []

    # set semua nama hulu yang "wujud" (model_key SOT + upstream litellm + routes keys)
    upstreams = {r["upstream"] for g in groups.values() for r in g}
    known = sot_models | upstreams | set(routes.keys())

    LICENSE_CODING_ONLY = {"mimo-v2.5-asr", "mimo-v2.5-tts", "mimo-v2.5-tts-voiceclone",
                           "mimo-v2.5-tts-voicedesign", "mimo-v2.5", "mimo-v2.5-pro"}
    HERMES_LANES = {"i-arif", "hermes-asi", "hermes-asi-vision", "fed/audio"}

    for alias, rungs in sorted(groups.items()):
        names = [r["upstream"] for r in rungs]
        # 1. sasaran wujud
        for n in names:
            base = n.split("/", 1)[-1]
            if base not in known and n not in known:
                findings.append({"alias": alias, "rule": "target_must_exist", "target": n,
                                 "severity": "DEAD-RUNG", "note": "tiada dalam SOT models/routes mahupun upstream lain"})
        # 2. tiada dupe
        dupes = [n for n, c in collections.Counter(names).items() if c > 1]
        for dn in dupes:
            findings.append({"alias": alias, "rule": "no_duplicates", "target": dn, "severity": "WARN"})
        # 3. self-fallback (alias == nama hulu)
        for n in names:
            if n == alias or n.split("/")[-1] == alias:
                findings.append({"alias": alias, "rule": "no_self_fallback", "target": n, "severity": "WARN"})
        # 4. semakan lesen: MiMo pada lorong Hermes
        if alias in HERMES_LANES:
            for n in names:
                if any(m in n for m in LICENSE_CODING_ONLY):
                    findings.append({"alias": alias, "rule": "license_scope_check", "target": n,
                                     "severity": "POLICY-BLOCK", "note": "lesen MiMo = alat pengkodan sahaja; Hermes BUKAN"})
        # 5. env-key kelihatan salah (MIMO_APIKEY untuk upstream MiniMax)
        for r in rungs:
            if "minimax" in r["upstream"].lower() or "speech-" in r["upstream"]:
                ek = r["env_key"]
                if "MIMO" in ek.upper() and "MINIMAX" not in ek.upper():
                    findings.append({"alias": alias, "rule": "env_key_typo_suspect", "target": r["upstream"],
                                     "severity": "DEAD-RUNG", "note": f"env {ek} untuk upstream MiniMax — disyaki salah nama"})

    # 6. capability signature FED yang mati di peringkat SOT (tiada model_routes)
    sigs = sot.get("capability_signatures", {})
    sig_items = sigs.items() if isinstance(sigs, dict) else []
    route_suffixes = {k.split("/")[-1] for k in routes}
    for sid, sig in sig_items:
        models_in = (sig or {}).get("models", []) if isinstance(sig, dict) else []
        if models_in:
            orphans = [m for m in models_in
                       if isinstance(m, str) and m not in routes and m.split("/")[-1] not in route_suffixes]
            if orphans:
                findings.append({"alias": f"sig:{sid}", "rule": "signature_orphan_models", "target": orphans,
                                 "severity": "WARN", "note": "model dalam signature tiada kekunci model_routes — fed_route akan No-routes"})

    if "--json" in sys.argv:
        print(json.dumps(findings, indent=2))
    else:
        if not findings:
            print("SEMUA LALUS — tiada pelanggaran disiplin fallback.")
        for f in findings:
            print(f"[{f['severity']:13}] {f['alias']:28} {f['rule']:24} {f.get('target','')}")
    return 0 if findings else 0

if __name__ == "__main__":
    sys.exit(main())
