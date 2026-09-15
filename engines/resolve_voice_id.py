#!/usr/bin/env python3
"""Voice-id resolver — canonical, fail-CLOSED.

Reads /root/AAA/audio/voice-registry.json (the canonical registry) and resolves a
requested id/alias to a provider voice id. REFUSES revoked ids.

Exit codes:
  0  resolved -> prints provider voice id on stdout
  3  requested id is REVOKED (fail closed, no synthesis)
  4  registry missing/unreadable
  5  id unknown (not in registry) — fail closed, never guess

Usage:  python3 resolve_voice_id.py <requested-id-or-alias>
"""
import json
import os
import sys

REGISTRY = os.environ.get("IARIF_VOICE_REGISTRY", "/root/AAA/audio/voice-registry.json")


def main(argv):
    if len(argv) < 2:
        sys.stderr.write("usage: resolve_voice_id.py <requested-id-or-alias>\n")
        return 2
    requested = argv[1].strip()
    try:
        reg = json.load(open(REGISTRY, encoding="utf-8"))
    except Exception as e:
        sys.stderr.write(f"voice-resolver: registry unreadable ({REGISTRY}): {e}\n")
        return 4

    voices = reg.get("voices", {})
    aliases = reg.get("aliases", {})

    # 1. Hard revocation gate — checked BEFORE any resolution, on raw and aliased forms.
    revoked_ids, revoked_names = set(), set()
    for name, v in voices.items():
        if str(v.get("status", "")).upper() == "REVOKED":
            revoked_names.add(name)
            if v.get("provider_voice_id"):
                revoked_ids.add(v["provider_voice_id"])
    if requested in revoked_ids or requested in revoked_names:
        sys.stderr.write(
            f"voice-resolver: REFUSED — '{requested}' is REVOKED in {REGISTRY}. "
            "Fail-closed: no synthesis.\n")
        return 3

    candidate = aliases.get(requested, requested)

    # 2. Canonical name or direct provider id -> LIVE provider id
    for name, v in voices.items():
        if str(v.get("status", "")).upper() != "LIVE":
            continue
        if candidate == name or candidate == v.get("provider_voice_id"):
            print(v["provider_voice_id"])
            return 0

    # 3. Unknown — fail closed. Never silently pass an unregistered id through.
    known = sorted(set(voices) | set(aliases))
    sys.stderr.write(
        f"voice-resolver: REFUSED — '{requested}' is not a known LIVE voice. "
        f"Known: {known}\n")
    return 5


if __name__ == "__main__":
    sys.exit(main(sys.argv))
