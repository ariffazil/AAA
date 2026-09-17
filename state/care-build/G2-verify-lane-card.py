#!/usr/bin/env python3
"""G2 verification — exercise lane_switch._lane_card and prove CARE GOVERNOR wiring.

Run:
  /usr/local/lib/hermes-agent/venv/bin/python /root/AAA/state/care-build/G2-verify-lane-card.py

Read-only with respect to production: it points the module's LANES_YAML at a probe
registry built from REAL lane entries in the canonical heritage copy (the live
/root/.hermes/lanes/lanes.yaml is absent — see G2-care-governor.md, Defect 1).
Exit 0 = all assertions pass.
"""
import ast
import importlib.util
import sys
from pathlib import Path

import yaml

PLUGIN = Path("/root/.hermes/profiles/aaa-hermes/plugins/lane_switch/__init__.py")
HERITAGE = Path(
    "/root/.quarantine/zen-20260912/_CANONICAL/"
    "HERMES-heritage-5.3G-20260904/lanes/lanes.yaml"
)
PROBE = Path("/tmp/g2-lanes-probe.yaml")
PROBE_LANES = ("arif", "arif-sado", "syed", "guest")

FULL = "CARE GOVERNOR"
FIXED = "DRAFT_AWAITING_F13"


def build_probe() -> list[str]:
    real = yaml.safe_load(HERITAGE.read_text())
    PROBE.write_text(
        yaml.safe_dump(
            {
                "version": real["version"],
                "default_lane": "arif",
                "lanes": {k: real["lanes"][k] for k in PROBE_LANES},
            },
            sort_keys=False,
        )
    )
    return list(PROBE_LANES)


def load_module():
    ast.parse(PLUGIN.read_text())  # syntax gate
    spec = importlib.util.spec_from_file_location("lane_switch_verify", PLUGIN)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.LANES_YAML = PROBE
    m._registry_mtime = 0.0
    m._registry_cache = {}
    return m


def main() -> int:
    lanes = build_probe()
    m = load_module()
    fails: list[str] = []

    def check(label: str, ok: bool) -> None:
        print(f"{'PASS' if ok else 'FAIL'}  {label}")
        if not ok:
            fails.append(label)

    print(f"ast.parse OK · probe registry lanes: {lanes}\n")
    check("detect_lane 267378578+DM  == arif", m.detect_lane("267378578", "267378578") == "arif")
    check(
        "detect_lane 267378578+SADO == arif-sado",
        m.detect_lane("267378578", "-1003815535761") == "arif-sado",
    )

    cards = {lane: m._lane_card(lane, True) for lane in lanes}
    for lane in ("arif", "arif-sado", "syed"):
        print(f"\n### _lane_card({lane!r}, include_memory=True) [{len(cards[lane])} chars]")
        print(cards[lane][:1200])
    print(f"\n### _lane_card('guest', include_memory=True) [{len(cards['guest'])} chars]")
    print(cards["guest"])

    arif = cards["arif"]
    for needle, label in (
        ("Never emit a directive about a third party's body", "rule 1 third-party body"),
        ("HOLD.** Do not answer for them", "rule 2 hold on @-address"),
        ("Never compute and emit a person's schedule", "rule 3 no schedule"),
        ("Relaying is service, not authorship", "rule 4 relay in his voice"),
        ("Never present a mechanism as a finding", "rule 5 mechanism banned"),
        ("Nothing about a person is ever scored, ranked, or modelled as an interior", "rule 7 no scoring"),
        (FIXED, "status line"),
        ("governed-uncertainty", "skill governed-uncertainty"),
        ("loved-one-worry-support", "skill loved-one-worry-support"),
        ("relationship-kernel", "skill relationship-kernel"),
        ("/root/AAA/instructions/care-governor.md", "fragment path named"),
    ):
        check(f"arif card carries: {label}", needle in arif)

    check("arif card has care governor", FULL in arif)
    check("arif-sado card has care governor", FULL in cards["arif-sado"])
    check("syed card has care governor", FULL in cards["syed"])
    check("guest card has NO care governor (F13 zero-data)", FULL not in cards["guest"])
    check(
        "card ordering: Authority < CARE GOVERNOR < CAPABILITY MAP",
        arif.index("Authority:") < arif.index(FULL) < arif.index("CAPABILITY MAP"),
    )
    check(
        "sovereign opt-out honoured (doctrines.care_governor: false)",
        m._care_governor_block("syed", {"doctrines": {"care_governor": False}}) == "",
    )
    # Degrade path: fragment unreadable -> the reference line must still be emitted.
    from pathlib import Path as _P

    real_fragment, m.CARE_GOVERNOR_FRAGMENT = m.CARE_GOVERNOR_FRAGMENT, _P("/tmp/__g2_no_such_fragment__")
    try:
        degraded = m._care_governor_block("syed", {})
    finally:
        m.CARE_GOVERNOR_FRAGMENT = real_fragment
    check(
        "missing fragment degrades to a path reference, never to silence",
        "READ that file" in degraded and "/tmp/__g2_no_such_fragment__" in degraded,
    )

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} failed) -> {fails}")
        return 1
    print("RESULT: PASS — all assertions green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
