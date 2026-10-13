#!/usr/bin/env node
/**
 * generate-public-claims.cjs — PROPOSAL 2026-10-12 (fi-003). NOT deployed.
 *
 * Compiler for the Public Observation Contract: probes declared sources,
 * derives claim state, emits a conformant observation envelope set to
 * shared/claims.json. Read-only against organs; writes exactly one file.
 *
 * Usage:
 *   node generate-public-claims.cjs [--contract PATH] [--out PATH]
 * Defaults (proposed live paths):
 *   contract = /var/www/html/mcp/shared/controlling-claims.json
 *   out      = /var/www/html/mcp/shared/claims.json
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const DEFAULTS = {
  contract: '/var/www/html/mcp/shared/controlling-claims.json',
  out: '/var/www/html/mcp/shared/claims.json',
};

function arg(flag, def) {
  const i = process.argv.indexOf(flag);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : def;
}

// Probe one HTTP JSON source. curl is used deliberately: it is present on the
// host and avoids adding a fetch/undici dependency to a cron context.
function probe(url) {
  const raw = execFileSync('curl', ['-sS', '--max-time', '12', url], { encoding: 'utf8' });
  return JSON.parse(raw);
}

// Dot-path pick with a special 'length' key for arrays. Returns undefined if
// the path does not resolve (caller decides whether that is a gap).
function pick(obj, expr) {
  if (!expr) return obj;
  return expr.split('.').reduce((acc, key) => {
    if (acc == null) return undefined;
    if (key === 'length') return Array.isArray(acc) || typeof acc === 'string' ? acc.length : undefined;
    return acc[key];
  }, obj);
}

function stateFor(rule, value) {
  switch (rule) {
    case 'nonempty_fail':
      return Array.isArray(value) && value.length > 0 ? 'MEASURED_FAIL' : 'MEASURED_PASS';
    case 'bool_pass':
      return value === true ? 'MEASURED_PASS' : 'MEASURED_FAIL';
    case 'reachable':
      // The source answered and the field resolved — that is REACHABLE, not a
      // verdict. Only nonempty_fail / bool_pass / state_map may assert PASS/FAIL.
      return 'REACHABLE';
    default:
      return 'UNKNOWN';
  }
}

function main() {
  const contractPath = arg('--contract', DEFAULTS.contract);
  const outPath = arg('--out', DEFAULTS.out);
  const contract = JSON.parse(fs.readFileSync(contractPath, 'utf8'));

  // Probe each declared source exactly once (fail soft unless required).
  const sourceData = {};
  for (const [name, src] of Object.entries(contract.sources || {})) {
    try {
      sourceData[name] = { ok: true, data: probe(src.url) };
    } catch (e) {
      sourceData[name] = { ok: false, error: String((e && e.message) || e) };
      if (src.required) process.stderr.write(`WARN required source '${name}' unreachable: ${e.message}\n`);
    }
  }

  const now = new Date().toISOString();
  const claims = [];

  for (const obs of contract.observations || []) {
    const base = {
      metric_id: obs.metric_id,
      plane: obs.plane,
      subject: obs.subject,
      epistemic_class: obs.epistemic_class || 'OBSERVED',
      scope: obs.scope || 'public surface',
      limitation: obs.limitation || null,
      observed_at: now,
    };

    let entry;
    if (obs.probe) {
      const src = sourceData[obs.probe];
      if (!src || !src.ok) {
        entry = { ...base, value: null, state: 'UNREACHABLE', source: `probe:${obs.probe}` };
      } else {
        // Honesty invariant: an unresolved field is UNMEASURED, never a pass.
        // A verdict is asserted only when the binding supplies one (state_map,
        // or a pass/fail rule) — the source merely being reachable is not one.
        const raw = pick(src.data, obs.extract);
        const resolved = raw !== undefined && raw !== null;
        let state;
        if (!resolved) state = 'UNMEASURED';
        else if (obs.state_map) state = obs.state_map[String(raw)] || 'UNKNOWN';
        else state = stateFor(obs.state_rule || 'reachable', raw);
        entry = { ...base, value: resolved ? raw : null, state, source: `probe:${obs.probe}` };
      }
    } else {
      entry = { ...base, value: obs.value, state: obs.state || 'DECLARED', source: obs.source || 'declared' };
    }
    claims.push(entry);
  }

  const payload = {
    _schema: 'arifos://shared/observation-envelope/v1',
    generated_at: now,
    generator: 'generate-public-claims.cjs',
    sources: Object.fromEntries(
      Object.entries(sourceData).map(([k, v]) => [k, v.ok ? 'reachable' : 'unreachable'])
    ),
    claims,
  };

  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(payload, null, 2) + '\n');
  process.stdout.write(`wrote ${outPath} — ${claims.length} claims @ ${now}\n`);
}

if (require.main === module) main();

module.exports = { pick, stateFor };
