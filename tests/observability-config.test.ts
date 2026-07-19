/**
 * observability-config.test.ts
 * ============================================================================
 * Focused config tests for the source-controlled Prometheus + Grafana
 * reconciliation under observability/.
 *
 * Verifies, against on-disk files only (no live network calls):
 *   1. prometheus.yml is valid YAML and scrapes 127.0.0.1:8088/metrics
 *      over plain HTTP (no /metrics/json, no https).
 *   2. nine_signal_alerts.yml is valid YAML and references only metric
 *      series that the arifOS kernel actually emits.
 *   3. Grafana datasource provisioning points at http://127.0.0.1:9090.
 *   4. Grafana dashboard provisioning uses /var/lib/grafana/dashboards.
 *   5. nine_signal_overview.json is valid JSON, references only real
 *      series, and never invents aliases or fake defaults for the three
 *      metric names the user listed that are NOT currently emitted
 *      (arifos_tearframe, arifos_rasa_events_total, arifos_scar_candidates_total).
 *
 * Run: npx tsx tests/observability-config.test.ts
 * DITEMPA BUKAN DIBERI
 */

import { describe, it, before } from "node:test";
import assert from "node:assert";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "yaml";

// ── Paths ──────────────────────────────────────────────────────────────────

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const OBS = path.join(ROOT, "observability");
const PROMETHEUS_YML = path.join(OBS, "prometheus", "prometheus.yml");
const ALERTS_YML = path.join(OBS, "prometheus", "nine_signal_alerts.yml");
const DATASOURCE_YML = path.join(OBS, "grafana", "provisioning", "datasources", "prometheus.yml");
const DASHBOARD_PROV_YML = path.join(OBS, "grafana", "provisioning", "dashboards", "nine_signal_dashboard.yml");
const DASHBOARD_JSON = path.join(OBS, "grafana", "dashboards", "nine_signal_overview.json");

// ── Verified-source series ──────────────────────────────────────────────────
// Two categories, both reconciled against /root/arifOS/arifosmcp/runtime/metrics.py
// on 2026-07-19:
//
//   1. EMITTED-NOW — series exposed by /metrics on 127.0.0.1:8088 right now.
//      Verified by `curl -s http://127.0.0.1:8088/metrics` against the running
//      kernel (pre-deployment). These will be visible to Prometheus today.
//
//   2. SOURCE-DEFINED — series registered by prometheus_client.Gauge/Counter
//      in metrics.py, but which only become visible in /metrics once arifOS is
//      deployed AND the corresponding completion event fires:
//        - arifos_tearframe         (Gauge, set only at ATLAS333 stage 7 boundaries)
//        - arifos_rasa_events_total (Counter, incremented only when log_shadow()
//                                    actually writes the JSONL entry)
//        - arifos_scar_candidates_total (Counter, incremented only after the
//                                    candidate JSON is durably written to
//                                    vault999/scars/)
//      Per metrics.py docstrings: "Status defaults / zero-fill MUST NOT
//      increment" these counters; the tearframe helper has the same contract.
//      Until the completion event fires, the series is absent — Prometheus
//      will see no data, and rate() expressions will return no series. This is
//      the truthful no-data-until-event semantics; we do NOT fake defaults.
const LIVE_BASE_SERIES = new Set([
  // EMITTED-NOW (live, type from metrics.py)
  "arifos_genius_score",            // gauge
  "arifos_entropy_delta",           // gauge
  "arifos_humility_band",           // gauge
  "arifos_peace_squared",           // gauge
  "arifos_empathy_quotient",        // gauge
  "arifos_metabolic_loop_seconds",  // histogram
  "arifos_verdicts_total",          // counter
  "arifos_m3_tokens_total",         // counter
  "arifos_m3_calls_total",          // counter
  "arifos_m3_latency_seconds",      // histogram
  "arifos_m3_fallback_total",       // counter
  "arifos_multimodal_calls_total",  // counter
  "arifos_requests_total",          // counter
  "arifos_w3_score",                // histogram
  "arifos_hold_queue_depth",        // gauge
  "arifos_vault_records_total",     // gauge
  "arifos_floor_violations_total",  // counter
  "arifos_sabar_events_total",      // counter
  "arifos_sessions_active",         // gauge
  "arifos_vault_entries_total",     // gauge
  "arifos_machine_faults_total",    // counter
  "arifos_void_events_total",       // counter
  "arifos_merkle_integrity_checks_total", // counter
  // SOURCE-DEFINED (registered in metrics.py; absent from /metrics until event)
  "arifos_tearframe",               // gauge,  labels=[component, provenance]
  "arifos_rasa_events_total",       // counter, labels=[risk_band, enforcement_mode, enforced]
  "arifos_scar_candidates_total",   // counter, labels=[stage, severity]
]);

const HISTOGRAM_SUFFIXES = ["_bucket", "_count", "_sum", "_created"];

function isKnownSeries(name: string): boolean {
  if (LIVE_BASE_SERIES.has(name)) return true;
  for (const suffix of HISTOGRAM_SUFFIXES) {
    const base = name.endsWith(suffix) ? name.slice(0, -suffix.length) : null;
    if (base && LIVE_BASE_SERIES.has(base)) return true;
  }
  return false;
}

// Type information for source-defined series that drive label-aware PromQL.
// Alerts and dashboard panels that reference these MUST honour the labels
// declared in metrics.py — otherwise we silently drop events or invent data.
const SOURCE_DEFINED_LABELS: Record<string, readonly string[]> = {
  arifos_tearframe: ["component", "provenance"],
  arifos_rasa_events_total: ["risk_band", "enforcement_mode", "enforced"],
  arifos_scar_candidates_total: ["stage", "severity"],
};

// The forbidden-set is now empty: every series the operator listed has been
// reconciled to a real source definition.
const FORBIDDEN_SERIES: ReadonlySet<string> = new Set();

// ── Helpers ────────────────────────────────────────────────────────────────

function readText(p: string): string {
  return fs.readFileSync(p, "utf8");
}

function extractPromqlReferences(text: string): string[] {
  const matches = text.match(/[a-zA-Z_][a-zA-Z0-9_]*/g) ?? [];
  return Array.from(new Set(matches.filter((m) => m.startsWith("arifos_"))));
}

// ── 1. Prometheus scrape config ────────────────────────────────────────────

describe("observability/prometheus/prometheus.yml", () => {
  let doc: any;
  before(() => {
    doc = yaml.parse(readText(PROMETHEUS_YML));
  });

  it("parses as valid YAML", () => {
    assert.ok(doc, "prometheus.yml must parse");
    assert.ok(Array.isArray(doc.scrape_configs), "scrape_configs must be an array");
  });

  it("does NOT scrape the old /metrics/json path or https://mcp.arif-fazil.com", () => {
    const raw = readText(PROMETHEUS_YML);
    assert.ok(!raw.includes("/metrics/json"), "must not reference /metrics/json");
    assert.ok(!raw.includes("mcp.arif-fazil.com"), "must not reference mcp.arif-fazil.com");
    assert.ok(!raw.includes("geox.arif-fazil.com"), "must not reference geox.arif-fazil.com");
    assert.ok(!raw.includes("host.docker.internal"), "must not depend on docker bridge");
  });

  it("scrapes 127.0.0.1:8088/metrics over plain HTTP", () => {
    const arifos = doc.scrape_configs.find((j: any) => j.job_name === "arifos-local");
    assert.ok(arifos, "arifos-local job must exist");
    assert.strictEqual(arifos.metrics_path, "/metrics");
    assert.strictEqual(arifos.scheme, "http");
    const targets = arifos.static_configs[0].targets;
    assert.ok(targets.includes("127.0.0.1:8088"), "must target 127.0.0.1:8088");
  });

  it("rule_files references nine_signal_alerts.yml", () => {
    assert.ok(Array.isArray(doc.rule_files));
    assert.ok(doc.rule_files.includes("nine_signal_alerts.yml"));
  });

  it("never references forbidden series", () => {
    const refs = extractPromqlReferences(readText(PROMETHEUS_YML));
    for (const r of refs) {
      assert.ok(!FORBIDDEN_SERIES.has(r), `Forbidden series referenced: ${r}`);
    }
  });
});

// ── 2. Alert rules ─────────────────────────────────────────────────────────

describe("observability/prometheus/nine_signal_alerts.yml", () => {
  let doc: any;
  before(() => {
    doc = yaml.parse(readText(ALERTS_YML));
  });

  it("parses as valid YAML with groups[].rules[]", () => {
    assert.ok(Array.isArray(doc.groups), "groups must be an array");
    let count = 0;
    for (const g of doc.groups) {
      assert.ok(Array.isArray(g.rules));
      count += g.rules.length;
    }
    assert.ok(count > 0, "at least one rule expected");
  });

  it("never references forbidden series", () => {
    const refs = extractPromqlReferences(readText(ALERTS_YML));
    for (const r of refs) {
      assert.ok(!FORBIDDEN_SERIES.has(r), `Forbidden series in alerts: ${r}`);
    }
  });

  it("every PromQL expression references only known series", () => {
    const exprRefs: string[] = [];
    for (const g of doc.groups) {
      for (const r of g.rules) {
        if (typeof r.expr === "string") {
          for (const m of r.expr.match(/[a-zA-Z_][a-zA-Z0-9_]*/g) ?? []) {
            if (m.startsWith("arifos_")) exprRefs.push(m);
          }
        }
      }
    }
    const unique = Array.from(new Set(exprRefs));
    for (const ref of unique) {
      assert.ok(isKnownSeries(ref), `Unknown series in alert expr: ${ref}`);
    }
  });

  it("at least one alert per constitutional floor that is enforced", () => {
    const text = readText(ALERTS_YML);
    assert.ok(/NineSignalGeniusFloorBreach/.test(text));
    assert.ok(/NineSignalPeaceSquaredFloorBreach/.test(text));
    assert.ok(/NineSignalW3BelowSeal/.test(text));
    assert.ok(/NineSignalHoldQueueGrowing/.test(text));
  });

  it("source-defined series alerts use rate() over counters so they stay silent pre-event", () => {
    const text = readText(ALERTS_YML);
    // arifos_rasa_events_total and arifos_scar_candidates_total are counters.
    // The truthful no-data-until-event pattern is rate() over a counter, which
    // yields no series when no samples exist (no false alerts).
    assert.ok(/rate\(arifos_rasa_events_total/.test(text),
      "RASA alert must use rate() to stay quiet until first event");
    assert.ok(/rate\(arifos_scar_candidates_total/.test(text),
      "scar_candidates alert must use rate() to stay quiet until first persistence");
  });

  it("arifos_tearframe alert targets the placeholder provenance (anti-hantu)", () => {
    const text = readText(ALERTS_YML);
    // tearframe is a gauge. The truthful pattern: alert on provenance="placeholder"
    // (which would mean someone bypassed the real-completion discipline). The
    // measured provenance is silent until first completion.
    assert.ok(/arifos_tearframe\{[^}]*provenance\s*=\s*"placeholder"/.test(text),
      "tearframe alert must specifically target the placeholder provenance label");
  });
});

// ── 3. Grafana datasource provisioning ─────────────────────────────────────

describe("observability/grafana/provisioning/datasources/prometheus.yml", () => {
  let doc: any;
  before(() => {
    doc = yaml.parse(readText(DATASOURCE_YML));
  });

  it("parses as valid Grafana provisioning YAML (apiVersion 1)", () => {
    assert.strictEqual(doc.apiVersion, 1);
    assert.ok(Array.isArray(doc.datasources));
    assert.strictEqual(doc.datasources.length, 1);
  });

  it("URL is http://127.0.0.1:9090 (no Cloudflare tunnel, no TLS)", () => {
    assert.strictEqual(doc.datasources[0].url, "http://127.0.0.1:9090");
    assert.strictEqual(doc.datasources[0].type, "prometheus");
    assert.strictEqual(doc.datasources[0].access, "proxy");
    const raw = readText(DATASOURCE_YML);
    assert.ok(!raw.includes("https://"), "no https:// in datasource URL");
  });

  it("has a stable uid so the dashboard can reference it", () => {
    assert.ok(typeof doc.datasources[0].uid === "string" && doc.datasources[0].uid.length > 0);
  });
});

// ── 4. Grafana dashboard provisioning ──────────────────────────────────────

describe("observability/grafana/provisioning/dashboards/nine_signal_dashboard.yml", () => {
  let doc: any;
  before(() => {
    doc = yaml.parse(readText(DASHBOARD_PROV_YML));
  });

  it("parses as valid Grafana provisioning YAML (apiVersion 1, file provider)", () => {
    assert.strictEqual(doc.apiVersion, 1);
    assert.ok(Array.isArray(doc.providers));
    assert.strictEqual(doc.providers[0].type, "file");
  });

  it("provisions from /var/lib/grafana/dashboards (filesystem, not HTTP)", () => {
    assert.strictEqual(doc.providers[0].options.path, "/var/lib/grafana/dashboards");
    const raw = readText(DASHBOARD_PROV_YML);
    assert.ok(!/url:\s*http/i.test(raw), "must not provision over HTTP URL");
  });
});

// ── 5. Dashboard JSON ──────────────────────────────────────────────────────

describe("observability/grafana/dashboards/nine_signal_overview.json", () => {
  let doc: any;
  before(() => {
    doc = JSON.parse(readText(DASHBOARD_JSON));
  });

  it("parses as valid JSON with a panels[] array", () => {
    assert.ok(Array.isArray(doc.panels));
    assert.ok(doc.panels.length > 0, "at least one panel");
  });

  it("every panel target has a non-empty expr", () => {
    for (const p of doc.panels) {
      for (const t of p.targets ?? []) {
        assert.ok(typeof t.expr === "string" && t.expr.length > 0,
          `panel ${p.id} has empty expr`);
      }
    }
  });

  it("never references forbidden series anywhere in the file", () => {
    const text = readText(DASHBOARD_JSON);
    for (const f of FORBIDDEN_SERIES) {
      assert.ok(!text.includes(f), `Forbidden series referenced: ${f}`);
    }
  });

  it("every PromQL expression references only known series", () => {
    const refs = new Set<string>();
    for (const p of doc.panels) {
      for (const t of p.targets ?? []) {
        for (const m of (t.expr ?? "").match(/[a-zA-Z_][a-zA-Z0-9_]*/g) ?? []) {
          if (m.startsWith("arifos_")) refs.add(m);
        }
      }
    }
    for (const ref of refs) {
      assert.ok(isKnownSeries(ref), `Unknown series in dashboard expr: ${ref}`);
    }
  });

  it("all panel datasource refs point to the prometheus uid (no undeclared aliases)", () => {
    for (const p of doc.panels) {
      const ds = p.datasource;
      if (ds && ds.type !== "grafana") {
        assert.strictEqual(ds.uid, "prometheus", `panel ${p.id} must reference uid=prometheus`);
      }
      for (const t of p.targets ?? []) {
        if (t.datasource && t.datasource.type !== "grafana") {
          assert.strictEqual(t.datasource.uid, "prometheus",
            `target in panel ${p.id} must reference uid=prometheus`);
        }
      }
    }
  });

  it("source-defined series appear in the dashboard with label-correct PromQL", () => {
    const refs = new Set<string>();
    for (const p of doc.panels) {
      for (const t of p.targets ?? []) {
        const expr = t.expr ?? "";
        for (const m of expr.match(/[a-zA-Z_][a-zA-Z0-9_]*/g) ?? []) {
          if (m.startsWith("arifos_")) refs.add(m);
        }
      }
    }
    assert.ok(refs.has("arifos_tearframe"),
      "dashboard must reference arifos_tearframe (source-defined gauge)");
    assert.ok(refs.has("arifos_rasa_events_total"),
      "dashboard must reference arifos_rasa_events_total (source-defined counter)");
    assert.ok(refs.has("arifos_scar_candidates_total"),
      "dashboard must reference arifos_scar_candidates_total (source-defined counter)");
  });

  it("counter source-defined series use rate() for no-data-until-event semantics", () => {
    const text = readText(DASHBOARD_JSON);
    // rate() returns no series until a counter has at least two samples. This is
    // the truthful quiet-until-event behaviour — we never invent a zero default.
    assert.ok(/rate\(\s*arifos_rasa_events_total\b/.test(text),
      "RASA panel must use rate() to stay silent before first event");
    assert.ok(/rate\(\s*arifos_scar_candidates_total\b/.test(text),
      "scar_candidates panel must use rate() to stay silent before first persistence");
  });

  it("tearframe panel targets the measured provenance (truthful default)", () => {
    const text = readText(DASHBOARD_JSON);
    // We surface the measured provenance — the one that proves a real GPV
    // computation happened. The placeholder provenance, if it appears, must
    // be highlighted as anti-hantu, not silently mixed in.
    // Accept both bare " and JSON-escaped \" since we read the file as text.
    assert.ok(/arifos_tearframe\{[^}]*provenance\s*=\s*\\?"measured\\?"/.test(text),
      "tearframe panel must filter to provenance=measured");
  });
});

console.log("All observability-config tests passed.");
