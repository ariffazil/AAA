# Evidence: Wants= Pattern Is Not Injection

DATE: 2026-08-08

## EMD claim (2026-08-08)
"FRAME wires itself into the federation service graph (arifos/aforge units) with no F1-F13 discipline — this is the exact shape F12 injection defense exists to catch."

## Live evidence
All 9 organs checked for systemd `Wants=` declarations:

```
arifos.service: Wants=network-online.target
geox-mcp.service: Wants=network.target
wealth-organ.service: Wants=network.target
well.service: (none)
frame-organ.service: Wants=arifos.service aforge.service signal-organ.service
```

FRAME is the ONLY one with federation-internal Wants. The others use `Wants=network.target`.

However: FRAME's full service file reveals standard systemd hardening:

```ini
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/opt/frame/app /var/lib/frame
ReadOnlyPaths=/root/.secrets/kunci-mas.flat.env
```

This is **best-in-class hardening** — stricter than arifOS.service (which runs as root with full home access).

FRAME reads secrets via `kunci-mas.flat.env` (ReadOnlyPaths) — same pattern as arifOS, GEOX, WEALTH, WELL.

## Verdict
F12 injection = REJECTED. Wants= = dependency declaration, not exploitation.
FRAME hardening = BETTER than most existing organs. The Wants= pattern is
architecturally consistent (frame depends on arifos+aforge being live) not
an attack vector.