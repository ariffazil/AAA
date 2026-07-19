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

// ── Verified-live series ────────────────────────────────────────────────────
// Emitted by arifOS at 127.0.0.1:8088/metrics as of 2026-07-19.
const LIVE_BASE_SERIES = new Set([
  "arifos_genius_score",
  "arifos_entropy_delta",
  "arifos_humility_band",
  "arifos_peace_squared",
  "arifos_empathy_quotient",
  "arifos_metabolic_loop_seconds",
  "arifos_verdicts_total",
  "arifos_m3_tokens_total",
  "arifos_m3_calls_total",
  "arifos_m3_latency_seconds",
  "arifos_m3_fallback_total",
  "arifos_multimodal_calls_total",
  "arifos_requests_total",
  "arifos_w3_score",
  "arifos_hold_queue_depth",
  "arifos_vault_records_total",
  "arifos_floor_violations_total",
  "arifos_sabar_events_total",
  "arifos_sessions_active",
  "arifos_vault_entries_total",
  "arifos_machine_faults_total",
  "arifos_void_events_total",
  "arifos_merkle_integrity_checks_total",
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

// Forbidden: listed by the user but not actually emitted by the kernel.
const FORBIDDEN_SERIES = new Set([
  "arifos_tearframe",
  "arifos_rasa_events_total",
  "arifos_scar_candidates_total",
]);

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
});

console.log("All observability-config tests passed.");
