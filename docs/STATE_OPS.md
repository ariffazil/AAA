# STATE OPS — keep the institution boring

## Daily / after every AAA change

```bash
# 1) Prove state
/root/AAA/scripts/state-probe.sh

# 2) After git commit on AAA (also auto via post-commit hook)
/root/AAA/scripts/sync-deploy-marker.sh

# 3) If registry or a2a-server code changed
systemctl restart aaa-a2a.service
sleep 3
/root/AAA/scripts/state-probe.sh
```

## Green criteria (STATE_READY)

- 8 government ports up
- FED `:4000/health/liveliness`
- AAA `healthy`, `deployment_drift=false`, vault CONNECTED
- G ≥ 0.70, C_dark ≤ 0.30, QDF ≥ 0.90
- CALL_MAP + STATE docs present
- Catalog 3 layers load
- Operators: hermes / openclaw / opencode (optional warn if down)

## Never for “state harden”

- Warga passport ceremony
- New geometry layers
- Putting judge/execute on AAA

## Telephone test (optional weekly)

```bash
opencode run "reply: CALL_MAP_OK"
# or: read /root/AAA/docs/CALL_MAP.md and dispatch via Hermes
```
