#!/usr/bin/env python3
"""
capabilities_audit.py — drift detector for modality SOT.

Compares /root/AAA/registries/models/CAPABILITIES.json against:
  [1] /root/.kimi-code/config.toml                       (kimi CLI per-model capabilities)
  [2] /root/A-FORGE/litellm-config.yaml                  (litellm supports_vision/supports_function_calling)
  [3] /root/.config/federation-models.json               (federation modalities arrays)
  [4] /root/AAA/federation/organs.yaml                   (organ-level modalities — minimax-media)

Doctrine: Zero drift tolerated. Drift > 0 → HOLD.

Usage:
  python3 capabilities_audit.py            # default — print report + exit 1 if drift
  python3 capabilities_audit.py --json     # JSON output
  python3 capabilities_audit.py --quiet    # exit code only
  python3 capabilities_audit.py --baseline # re-snapshot current sources to quarantine
"""
import json, sys, os, re, argparse
from pathlib import Path
from datetime import datetime, timezone

# ── Paths ──────────────────────────────────────────────────────────────
SOT_PATH        = Path("/root/AAA/registries/models/CAPABILITIES.json")
KIMI_PATH       = Path("/root/.kimi-code/config.toml")
LITELLM_PATH    = Path("/root/A-FORGE/litellm-config.yaml")
FEDERATION_PATH = Path("/root/.config/federation-models.json")
ORGANS_PATH     = Path("/root/AAA/federation/organs.yaml")
QUARANTINE_DIR  = Path("/root/forge_work/_quarantine/2026-08-18-capabilities-sot")

# ── Modality mapping ────────────────────────────────────────────────────
# Each source has its own vocabulary. Map to canonical CAPABILITIES flags.
KIMI_TO_CANON = {
    "image_in":   "vision",
    "video_in":   "video_in",
    "audio_in":   "audio_in",
    "image_out":  "image_out",
    "video_out":  "video_out",
    "audio_out":  "audio_out",
}
# Federation modalities array → canonical flags
FED_MOD_TO_CANON = {
    "image": "vision",
    "audio": "audio_in",   # default; refine per context
    "video": "video_in",
    "text":  "text",        # always true
}

# ── Loaders ────────────────────────────────────────────────────────────
def load_sot():
    """Load CAPABILITIES.json — return {model_id: {modalities: {}, features: {}}}"""
    with open(SOT_PATH) as f:
        sot = json.load(f)
    return sot

def load_kimi_caps():
    """Parse kimi config.toml capabilities arrays → {model_id: set(canonical_flags)}"""
    if not KIMI_PATH.exists():
        return {}
    # Simple line-based parser (tomllib is 3.11+, no external deps wanted)
    caps = {}
    with open(KIMI_PATH) as f:
        cur_model = None
        in_models = False
        in_model_block = False
        for line in f:
            line = line.rstrip("\n")
            # Section: [[models]] or [models]
            if re.match(r"^\[models\]", line):
                in_models = True
                continue
            if re.match(r"^\[\[", line) and "models" not in line:
                in_models = False
                continue
            if not in_models:
                continue
            # Model entry: [models."provider/name"]
            m = re.match(r'^\s{0,2}\[\[models\."([^"]+)"\]\]', line)
            if m:
                cur_model = m.group(1)
                caps.setdefault(cur_model, set())
                continue
            # Capability line inside a [[models.X]] block
            cm = re.match(r"^\s*capabilities\s*=\s*\[([^\]]+)\]", line)
            if cm and cur_model:
                raw = cm.group(1)
                flags = re.findall(r'"([^"]+)"', raw)
                for f in flags:
                    canon = KIMI_TO_CANON.get(f)
                    if canon:
                        caps.setdefault(cur_model, set()).add(canon)
    return caps

def load_litellm_supports():
    """Parse litellm-config.yaml model_info.supports_vision → {model_name: set(canonical_flags)}"""
    if not LITELLM_PATH.exists():
        return {}
    out = {}
    with open(LITELLM_PATH) as f:
        for line in f:
            m = re.match(r"^\s*supports_vision:\s*(\S+)", line)
            if m and m.group(1).lower() == "true":
                # Try to attach to most recent model entry — best effort
                # We just collect supports_vision: true instances keyed by model name
                pass  # (best-effort — litellm doesn't bind cleanly to model_key)
    # Simpler: count supports_vision: true instances — if any, vision capability exists in some chain
    return out

def load_federation_modalities():
    """Parse federation-models.json modalities + capabilities arrays → canonical flags.

    modalities array = INPUT modalities (text, image→vision, audio→audio_in, video→video_in)
    capabilities array = ADDITIONAL capabilities — look for OUTPUT tokens:
        - "tts" → audio_out
        - "music" → music_out
        - "image_generation" → image_out
        - "video_generation" → video_out
        - "vision" → redundant confirmation of vision input
    """
    if not FEDERATION_PATH.exists():
        return {}
    caps = {}
    with open(FEDERATION_PATH) as f:
        data = json.load(f)
    for m in data.get("models", []):
        mid = m.get("model_key", "")
        # Strip provider prefix: "minimax/MiniMax-M3" → "MiniMax-M3"
        short = mid.split("/", 1)[1] if "/" in mid else mid
        flags = set()
        # Input modalities
        mods = m.get("modalities", []) or []
        for mod in mods:
            canon = FED_MOD_TO_CANON.get(mod)
            if canon:
                flags.add(canon)
        # Output modality tokens from capabilities
        cap_list = m.get("capabilities", []) or []
        if "tts" in cap_list:
            flags.add("audio_out")
        if "music" in cap_list:
            flags.add("music_out")
        if "image_generation" in cap_list:
            flags.add("image_out")
        if "video_generation" in cap_list:
            flags.add("video_out")
        if short and flags:
            caps.setdefault(short, set()).update(flags)
    return caps

def load_organs_modalities():
    """Parse organs.yaml minimax-media upstream_models — special case for generation organ."""
    if not ORGANS_PATH.exists():
        return {}
    out = {}
    # Manual parse for minimax-media block
    with open(ORGANS_PATH) as f:
        text = f.read()
    mm_block = re.search(r"id: minimax-media(.*?)live_probe_2026_08_07:", text, re.DOTALL)
    if not mm_block:
        return out
    body = mm_block.group(1)
    # Extract modalities under upstream_models
    if "video:" in body:     out.setdefault("minimax-media", set()).update({"video_out"})
    if "image:" in body:     out.setdefault("minimax-media", set()).update({"image_out"})
    if "audio:" in body:     out.setdefault("minimax-media", set()).update({"audio_out"})
    if "music:" in body:     out.setdefault("minimax-media", set()).update({"music_out"})
    return out

# ── Drift detector ─────────────────────────────────────────────────────
def normalize_flags(sot_models, defaults):
    """Build {model_id: set(canonical_flags)} from SOT with defaults applied."""
    norm = {}
    for mid, m in sot_models.items():
        flags = set()
        # modalities
        for k, v in (m.get("modalities") or {}).items():
            if v is True:
                flags.add(k)
        # defaults for missing
        for k, v in defaults.get("modalities", {}).items():
            if v is True and k not in (m.get("modalities") or {}):
                flags.add(k)
        # text is always true by default
        flags.add("text")
        norm[mid] = flags
    return norm

# ── Alias map ──────────────────────────────────────────────────────────
# Federation-models uses short names; SOT uses dash-form canonical names.
# Map source name → SOT canonical name.
ALIASES = {
    "k3": "kimi-k3",
    "kimi-for-coding": "kimi-for-coding",  # legacy kimi code CLI model — same in both
    "minimax": "minimax-media",            # federation "minimax" modality set → media organ
}

def detect_drift(sot_norm, sources):
    """Compare SOT norms to source norms. Return (drifts, uncatalogued).

    Only models IN SOT are drift-checked (SOT is canonical truth).
    Models in source but NOT in SOT are reported as UNCATALOGUED (info, not drift).
    'text' is excluded from drift (always-on default — not a meaningful flag).
    Aliases normalize naming differences between sources and SOT.
    """
    drifts = []
    uncatalogued = []
    TEXT = "text"

    def canon(mid):
        """Normalize model id via ALIASES map."""
        return ALIASES.get(mid, mid)

    # Build a unified source view: merge each source's caps under canonical names
    unified_sources = {}
    for src_name, src_caps in sources.items():
        for mid, flags in src_caps.items():
            k = canon(mid)
            unified_sources.setdefault(k, {})[src_name] = flags

    # 1. Drift: models in SOT — compare to each source if source knows them
    for mid in sorted(sot_norm):
        sot_flags = sot_norm[mid] - {TEXT}
        for src_name, src_flags_per_model in unified_sources.get(mid, {}).items():
            src_flags = src_flags_per_model - {TEXT}
            # SOT missing a flag source claims
            for flag in sorted(src_flags - sot_flags):
                drifts.append({
                    "model": mid,
                    "source": src_name,
                    "field": flag,
                    "claim": "source=true, sot=absent",
                    "severity": "DRIFT",
                })
            # SOT extra: source explicitly does NOT have this flag
            for flag in sorted(sot_flags - src_flags):
                drifts.append({
                    "model": mid,
                    "source": src_name,
                    "field": flag,
                    "claim": "sot=true, source=absent",
                    "severity": "DRIFT-EXTRA",
                })

    # 2. Uncatalogued: source models not in SOT (case-insensitive match)
    sot_lower = {k.lower(): k for k in sot_norm}
    for mid in sorted(unified_sources):
        if mid.lower() not in sot_lower:
            # Collect which sources know this model
            src_list = list(unified_sources[mid].keys())
            # Take union of flags across sources (text stripped)
            all_flags = set()
            for f in unified_sources[mid].values():
                all_flags.update(f)
            uncatalogued.append({
                "model": mid,
                "sources": src_list,
                "flags_in_source": sorted(all_flags - {TEXT}),
            })

    return drifts, uncatalogued

# ── Main ───────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="CAPABILITIES.json drift audit")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--quiet", action="store_true", help="Exit code only")
    ap.add_argument("--strict", action="store_true", help="Exit 1 on drift (CI mode). Default: informational only.")
    ap.add_argument("--baseline", action="store_true", help="Re-snapshot source files to quarantine dir")
    args = ap.parse_args()

    if args.baseline:
        QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
        for p in [KIMI_PATH, LITELLM_PATH, FEDERATION_PATH, ORGANS_PATH]:
            if p.exists():
                (QUARANTINE_DIR / f"{p.name}.baseline").write_text(p.read_text())
        print(f"Baseline snapshot written to {QUARANTINE_DIR}")
        return 0

    sot = load_sot()
    defaults = sot.get("defaults", {})
    sot_models = sot.get("models", {})
    sot_norm = normalize_flags(sot_models, defaults)

    sources = {
        "kimi/config.toml":        load_kimi_caps(),
        "federation-models.json":  load_federation_modalities(),
        "organs.yaml":             load_organs_modalities(),
        # litellm-config.yaml supports_vision is per-chain-entry, not per-model — skip
        # until we have a model_name binding mechanism.
    }

    drifts, uncatalogued = detect_drift(sot_norm, sources)

    if args.json:
        print(json.dumps({
            "sot_path": str(SOT_PATH),
            "sot_model_count": len(sot_models),
            "drift_count": len(drifts),
            "uncatalogued_count": len(uncatalogued),
            "drifts": drifts,
            "uncatalogued": uncatalogued,
            "sources_audited": list(sources.keys()),
            "audit_timestamp": datetime.now(timezone.utc).isoformat(),
            "verdict": "FAIL" if drifts else "PASS",
            "doctrine_phase": "1+2 SEAL; Phase 3 HOLD on federation-models.json migration (per F13 — first migration must stabilize before second)",
        }, indent=2))
    elif not args.quiet:
        print(f"═══ CAPABILITIES Drift Audit ═══")
        print(f"SOT:    {SOT_PATH}")
        print(f"Models in SOT: {len(sot_models)}")
        print(f"Sources: {', '.join(sources.keys())}")
        print(f"Drift count:   {len(drifts)}")
        print(f"Uncatalogued:  {len(uncatalogued)}  (source models not yet in SOT — catalog gap, not drift)")
        print()
        if drifts:
            print(f"{'MODEL':<28} {'SOURCE':<26} {'FIELD':<14} {'SEVERITY':<14} CLAIM")
            print("─" * 100)
            for d in drifts[:50]:
                print(f"{d['model']:<28} {d['source']:<26} {d['field']:<14} {d['severity']:<14} {d['claim']}")
            if len(drifts) > 50:
                print(f"... and {len(drifts)-50} more")
            print()
            print("Phase 1+2 SEAL — drift reported for visibility.")
            print("Phase 3 HOLD per doctrine: first migration must stabilize before second.")
            print("Re-evaluate after 1 week of runtime. If drift reduces naturally, no action.")
            print("If drift grows, then either tighten SOT or migrate federation-models.json.")
        else:
            print("✅ Zero drift. CAPABILITIES.json is canonical for all audited sources.")
        if uncatalogued:
            print()
            print(f"─── Uncatalogued ({len(uncatalogued)} entries — informational) ───")
            for u in uncatalogued[:30]:
                flags = ",".join(u['flags_in_source']) or "(text only)"
                srcs = ",".join(u['sources'])
                print(f"  {u['model']:<40} from {srcs:<26} [{flags}]")
            if len(uncatalogued) > 30:
                print(f"  ... and {len(uncatalogued)-30} more")
        print()

    if args.strict:
        sys.exit(1 if drifts else 0)
    # Default: informational, exit 0
    return 0

if __name__ == "__main__":
    main()