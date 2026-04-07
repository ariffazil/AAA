# HEARTBEAT.md — WAW Health Checklist

> **DITEMPA BUKAN DIBERI** — Forged, Not Given

## Periodic Checks (Run on heartbeat)

### Website Health
- [ ] `npm run build` succeeds without errors
- [ ] `npm run lint` passes
- [ ] Dev server (`npm run dev`) starts correctly

### Content Sync
- [ ] Verify links to arifOS repo are current
- [ ] Check version numbers match arifOS releases
- [ ] Ensure AGENTS.md reflects current practices

### Dependencies
- [ ] No critical security vulnerabilities (`npm audit`)
- [ ] Major dependencies up to date

## External Checks

- [ ] arif-fazil.com loads correctly
- [ ] arifosmcp.arif-fazil.com/health responds
- [ ] Links to canonical arifOS repo work

---

**Last Updated:** 2026-04-07  
**arifOS Version:** 2026.04.07
