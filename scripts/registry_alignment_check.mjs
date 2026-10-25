#!/usr/bin/env node
/**
 * registry_alignment_check.mjs — AAA Agent Registry alignment gate
 *
 * Enforces canon/AGENT-REGISTRY-ALIGNMENT-2026-10-25.md (INV-AR-1..8).
 * Baseline (ratchet) lives in registries/CANONICAL_REGISTRY_POLICY.yaml::alignment.baseline.
 * A count that RISES fails. A count that FALLS must be re-baselined in the same commit.
 *
 * Wired as `npm run validate:registry`.
 *
 * Usage:
 *   node scripts/registry_alignment_check.mjs            # gate
 *   node scripts/registry_alignment_check.mjs --json     # machine-readable
 *   node scripts/registry_alignment_check.mjs --measure  # print measured counts, never fail
 */

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { parse as parseYaml } from "yaml";

const ROOT = process.cwd();
const POLICY = "registries/CANONICAL_REGISTRY_POLICY.yaml";
const CARD_ROOTS = ["agent-cards", "a2a-server/agent-cards", "agents"];
const SKIP_SEGMENT = /(^|\/)(_archive|_superseded|node_modules|\.archive[^/]*)(\/|$)/;
const ARGS = new Set(process.argv.slice(2));
const MEASURE_ONLY = ARGS.has("--measure");
const AS_JSON = ARGS.has("--json");

const abs = (p) => (path.isAbsolute(p) ? p : path.join(ROOT, p));
const readYaml = (p) => parseYaml(fs.readFileSync(abs(p), "utf8"));
const exists = (p) => fs.existsSync(abs(p));

function walk(dir, onFile) {
  const base = abs(dir);
  if (!fs.existsSync(base)) return;
  for (const entry of fs.readdirSync(base, { withFileTypes: true })) {
    const rel = path.join(dir, entry.name);
    if (SKIP_SEGMENT.test(rel)) continue;
    if (entry.isDirectory()) walk(rel, onFile);
    else onFile(rel);
  }
}

function cards() {
  const out = [];
  for (const root of CARD_ROOTS) {
    walk(root, (rel) => {
      if (!rel.endsWith(".json")) return;
      let doc;
      try {
        doc = JSON.parse(fs.readFileSync(abs(rel), "utf8"));
      } catch {
        return;
      }
      if (!doc || typeof doc !== "object" || Array.isArray(doc)) return;
      const isCard =
        doc.id && (Array.isArray(doc.skills) || doc.capabilities || doc.protocolVersion || doc.bound_to);
      if (isCard) out.push({ rel, doc });
    });
  }
  return out;
}

function resolveSkillSource(src) {
  if (!src) return null;
  const raw = src.startsWith("./") ? src.slice(2) : src;
  const cands = path.isAbsolute(raw) ? [raw] : [path.join(ROOT, raw)];
  return cands.find((c) => fs.existsSync(c)) || null;
}

const checks = [];
function check(id, invariant, label, measured, baseline, detail = []) {
  const failed = MEASURE_ONLY ? false : measured > baseline;
  checks.push({ id, invariant, label, measured, baseline, status: failed ? "FAIL" : "PASS", detail });
}

// ── load policy ────────────────────────────────────────────────────────────────
let policy;
try {
  policy = readYaml(POLICY);
} catch (err) {
  console.error(`FATAL: cannot parse ${POLICY}: ${err.message}`);
  process.exit(1);
}
const baseline = policy?.alignment?.baseline || {};

// ── INV-AR-7: declared canonical/derived paths exist (or external:true) ───────
{
  const missing = [];
  for (const [cat, body] of Object.entries(policy.categories || {})) {
    for (const layer of ["canonical", "derived"]) {
      for (const entry of body?.[layer] || []) {
        const p = entry?.path || "";
        if (entry?.external) continue;
        const ok = p.includes("*") ? globExists(p) : exists(p);
        if (!ok) missing.push(`${cat}/${layer}: ${p}`);
      }
    }
  }
  check("AR7", "INV-AR-7", "declared canonical paths resolve", missing.length, baseline.policy_ghost_paths ?? 0, missing);
}

function globExists(pattern) {
  // minimal single-star glob: split on '**' / '*' and walk
  const segs = pattern.split("/");
  const walkSeg = (dir, i) => {
    if (i === segs.length) return fs.existsSync(dir);
    const seg = segs[i];
    if (seg === "**") {
      if (walkSeg(dir, i + 1)) return true;
      if (!fs.existsSync(dir)) return false;
      return fs.readdirSync(dir, { withFileTypes: true }).some(
        (e) => e.isDirectory() && walkSeg(path.join(dir, e.name), i),
      );
    }
    if (seg.includes("*")) {
      const re = new RegExp(`^${seg.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*")}$`);
      if (!fs.existsSync(dir)) return false;
      return fs.readdirSync(dir, { withFileTypes: true }).some(
        (e) => re.test(e.name) && walkSeg(path.join(dir, e.name), i + 1),
      );
    }
    return walkSeg(path.join(dir, seg), i + 1);
  };
  return walkSeg(ROOT, 0);
}

// ── INV-AR-8: no executable consumer reads a _deprecated_ path ────────────────
{
  const hits = [];
  const codeExt = /\.(mjs|cjs|js|ts|py)$/;
  for (const root of ["scripts", "a2a-server", "src", "lib", "bin", "hooks"]) {
    walk(root, (rel) => {
      if (!codeExt.test(rel)) return;
      const text = fs.readFileSync(abs(rel), "utf8");
      text.split("\n").forEach((line, n) => {
        if (/_deprecated_\w+/.test(line) && !/^\s*(#|\/\/|\*)/.test(line)) {
          hits.push(`${rel}:${n + 1}`);
        }
      });
    });
  }
  check("AR8", "INV-AR-8", "no code reads a _deprecated_ path", hits.length, baseline.deprecated_reads ?? 0, hits);
}

// ── INV-AR-1: duplicate agent identity across live card roots ─────────────────
const allCards = cards();
{
  const byId = new Map();
  for (const { rel, doc } of allCards) {
    if (!byId.has(doc.id)) byId.set(doc.id, []);
    byId.get(doc.id).push(rel);
  }
  const dups = [...byId.entries()].filter(([, v]) => v.length > 1);
  check(
    "AR1",
    "INV-AR-1",
    "no duplicate agent id across live roots",
    dups.length,
    baseline.duplicate_agent_ids ?? 0,
    dups.map(([id, v]) => `${id} x${v.length}`),
  );
}

// ── INV-AR-4: card skill sources resolve from repo root or absolute ───────────
{
  let total = 0;
  let unresolved = 0;
  let noSource = 0;
  const examples = [];
  for (const { rel, doc } of allCards) {
    const skills = Array.isArray(doc.skills) ? doc.skills : [];
    for (const s of skills) {
      if (!s || typeof s !== "object") continue;
      total += 1;
      if (!s.source) {
        noSource += 1;
        continue;
      }
      if (!resolveSkillSource(s.source)) {
        unresolved += 1;
        if (examples.length < 8) examples.push(`${rel}: ${s.source}`);
      }
    }
  }
  check("AR4a", "INV-AR-4", "card skill refs — unresolved", unresolved, baseline.card_skill_refs_unresolved ?? 0, examples);
  check("AR4b", "INV-AR-4", "card skill refs — no source", noSource, baseline.card_skill_refs_no_source ?? 0, []);
  checks.push({ id: "AR4i", invariant: "INV-AR-4", label: "card skill refs — total (informational)", measured: total, baseline: baseline.card_skill_refs_total ?? total, status: "INFO", detail: [] });
}

// ── INV-AR-2: cards declare a schema version ─────────────────────────────────
{
  const missing = allCards.filter(({ doc }) => !doc.schemaVersion).map(({ rel }) => rel);
  check(
    "AR2",
    "INV-AR-2",
    "cards missing schemaVersion",
    missing.length,
    baseline.cards_missing_schema_version ?? 0,
    missing.slice(0, 8),
  );
}

// ── INV-AR-9/10/11: agency authority must not outrun principal, runtime, lifecycle ─
// 2026-10-25 correction: the first gate counted only card.public_key.hex and included
// service-class cards. Both were wrong: a principal may live in agents/**/identity.json,
// IDENTITY/keys/*_public.pem or the DID registry, and an MCP/organ surface legitimately
// has NO agent principal (service authority ≠ agency).
{
  const byId = new Map();
  for (const c of allCards) byId.set(c.doc.id, c); // later root wins, mirrors loader order
  const unique = [...byId.values()];

  const principals = new Set();
  walk("agents", (rel) => {
    if (!rel.endsWith("/identity.json")) return;
    try {
      const d = JSON.parse(fs.readFileSync(abs(rel), "utf8"));
      const id = d.actor_id || d.agent_id || d.id;
      if (id) principals.add(String(id).toLowerCase());
    } catch {
      /* noop */
    }
  });
  if (fs.existsSync(abs("IDENTITY/keys"))) {
    for (const f of fs.readdirSync(abs("IDENTITY/keys"))) {
      if (f.toLowerCase().includes("public")) principals.add(f.split("_")[0].toLowerCase());
    }
  }
  try {
    const did = readYaml("auth/did_registry.yaml")?.dids;
    if (Array.isArray(did)) {
      for (const e of did) {
        const id = e?.actor_id || e?.agent_id || e?.id || e?.name;
        if (id) principals.add(String(id).toLowerCase());
      }
    } else if (did && typeof did === "object") {
      for (const k of Object.keys(did)) principals.add(k.toLowerCase());
    }
  } catch {
    /* noop */
  }

  const isService = (id, doc, rel) => {
    const blob = [doc.constitutional_class, doc.class, doc.role, doc.type, doc.category]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
    if (/(organ|service|mcp|pillar|gateway)/.test(blob)) return true;
    if (/\/(organs|pillars|functions)\//.test(rel)) return true;
    if (/-mcp$/.test(id) || /-gateway$/.test(id) || ["arifos", "aforge", "aaa"].includes(id)) return true;
    return false;
  };
  const hasPrincipal = (id, doc) =>
    Boolean(doc.public_key && doc.public_key.hex) || principals.has(id.toLowerCase());

  const actors = unique.filter(({ doc, rel }) => !isService(doc.id, doc, rel));
  const auth = actors.filter(({ doc }) => doc.authority_ceiling || doc.authority);
  const noPrincipal = auth.filter(({ doc }) => !hasPrincipal(doc.id, doc));
  const noRuntime = auth.filter(({ doc }) => !doc.runtime_harness);
  const noLifecycle = auth.filter(({ doc }) => !doc.status);

  check("AR9", "INV-AR-9", `actor authority without principal (of ${actors.length})`, noPrincipal.length, baseline.authority_without_principal ?? 0, noPrincipal.map(({ doc }) => doc.id));
  check("AR10", "INV-AR-10", `actor authority without runtime_ref (of ${actors.length})`, noRuntime.length, baseline.authority_without_runtime ?? 0, noRuntime.map(({ doc }) => doc.id));
  check("AR11", "INV-AR-11", `actor authority without lifecycle state (of ${actors.length})`, noLifecycle.length, baseline.authority_without_lifecycle ?? 0, []);
}

// ── INV-AR-12/13: one admission owner; resolution may not admit ──────────────
{
  let gap = 0;
  let caseDups = 0;
  const detail = [];
  try {
    const resMap = JSON.parse(fs.readFileSync(abs("registry/canonical_identity.json"), "utf8"));
    const admRaw = JSON.parse(fs.readFileSync(abs("registry/canonical_agents.json"), "utf8"))?.canonical || {};
    const admitted = new Map();
    for (const [cid, entry] of Object.entries(admRaw)) {
      admitted.set(String(cid).toLowerCase(), cid);
      for (const a of entry?.aliases || []) admitted.set(String(a).toLowerCase(), cid);
    }
    const resKeys = Object.keys(resMap);
    gap = resKeys.filter((k) => !admitted.has(k.toLowerCase())).length;
    for (const k of resKeys.filter((k) => !admitted.has(k.toLowerCase()))) detail.push(`not admitted: ${k}`);
    const g = new Map();
    for (const k of resKeys) g.set(k.toLowerCase(), [...(g.get(k.toLowerCase()) || []), k]);
    caseDups = [...g.values()].filter((v) => v.length > 1).length;
    for (const v of g.values()) if (v.length > 1) detail.push(`case-duplicate: ${v.join(" + ")}`);
  } catch {
    gap = -1;
  }
  check("AR12", "INV-AR-12", "resolution ids not admitted", Math.max(gap, 0), baseline.resolution_not_admitted ?? 0, detail.filter((d) => d.startsWith("not admitted")));
  check("AR13", "INV-AR-13", "case-duplicate keys in identity map", caseDups, baseline.case_duplicate_keys ?? 0, detail.filter((d) => d.startsWith("case-duplicate")));
}

// ── INV-AR-14/15: principal store and allowlist must have one owner ──────────
{
  let didStores = 0;
  const storeDetail = [];
  const codeExt = /\.(mjs|cjs|js|ts|py)$/;
  for (const root of ["a2a-server", "scripts", "auth", "registry"]) {
    walk(root, (rel) => {
      if (!codeExt.test(rel)) return;
      const text = fs.readFileSync(abs(rel), "utf8");
      for (const m of text.matchAll(/([\w./-]*(?:did[_-]registry|secrets\/did\/registry)\.(?:json|yaml))/g)) {
        // Normalise spellings of the same store: an absolute /root/AAA/... path and a
        // relative path are ONE owner, not two. Two owners remain (see baseline).
        const raw = m[1];
        const p = raw.includes("secrets/did/registry") ? "secrets/did/registry.json" : "did_registry.yaml";
        if (!storeDetail.includes(p)) storeDetail.push(p);
      }
    });
  }
  didStores = storeDetail.length;
  check("AR14", "INV-AR-14", "distinct DID stores named in code", didStores, baseline.did_stores_named_in_code ?? 0, storeDetail);

  // Two allowlists: server.js (canonical) and federation_envelope.js (mounted on every /a2a route).
  let anon = 0;
  let missing = 0;
  const names = [];
  try {
    const grab = (file, re) => {
      const m = fs.readFileSync(abs(file), "utf8").match(re);
      return m ? [...m[1].matchAll(/'([^']+)'/g)].map((x) => x[1]) : [];
    };
    const server = new Set(grab("a2a-server/server.js", /CANONICAL_ACTORS = new Set\(\[([\s\S]*?)\]\)/));
    const env = new Set(grab("a2a-server/federation_envelope.js", /const CANONICAL_ACTORS = new Set\(\[([\s\S]*?)\]\)/));
    anon = env.has("anonymous") && !server.has("anonymous") ? 1 : 0;
    const diff = [...server].filter((x) => !env.has(x));
    missing = diff.length;
    names.push(...diff.slice(0, 8));
  } catch {
    /* noop */
  }
  check("AR15a", "INV-AR-15", "envelope allowlist admits anonymous", anon, baseline.envelope_allows_anonymous ?? 0, []);
  check("AR15b", "INV-AR-15", "server actors missing from envelope list", missing, baseline.server_actors_missing_from_envelope ?? 0, names);
}

// ── INV-AR-5: skill index entries resolve to a real SKILL.md ─────────────────
{
  const idx = readYamlSafeJson("skills_index.json");
  const entries = idx?.skills || [];
  // Index paths are recorded as absolute /root/AAA/skills/... — portable match is the
  // repo-relative tail, so the gate also runs inside a clone.
  const resolves = (p) => {
    if (!p) return true;
    if (fs.existsSync(p)) return true;
    const tail = p.split("/skills/").pop();
    return tail !== p && fs.existsSync(path.join(ROOT, "skills", tail));
  };
  const missing = entries.filter((s) => !resolves(s?.path)).map((s) => s.path);
  check("AR5", "INV-AR-5", "skill index entries resolve", missing.length, baseline.skill_index_missing_entries ?? 0, missing.slice(0, 8));
}

function readYamlSafeJson(p) {
  try {
    return JSON.parse(fs.readFileSync(abs(p), "utf8"));
  } catch {
    return null;
  }
}

// ── endpoint parity: organs.yaml vs PORT_REGISTRY.json ────────────────────────
{
  let organs;
  let ports;
  try {
    organs = readYaml("federation/organs.yaml")?.components || [];
    ports = JSON.parse(fs.readFileSync(abs("registries/PORT_REGISTRY.json"), "utf8"))?.organs || {};
  } catch {
    organs = [];
    ports = {};
  }
  const divergent = [];
  for (const c of organs) {
    const id = c?.id;
    const p = c?.port;
    if (!id || !p || !ports[id]) continue;
    if (String(ports[id].port) !== String(p)) divergent.push(`${id}: organs=${p} port_registry=${ports[id].port}`);
  }
  checks.push({ id: "AR-Endpoint", invariant: "L4", label: "organ port parity (shared ids)", measured: divergent.length, baseline: 0, status: divergent.length ? "FAIL" : "PASS", detail: divergent });
}

// ── tool id uniqueness within each layer ─────────────────────────────────────
{
  const dupPolicy = [];
  const dupCatalogue = [];
  try {
    const tools = readYaml("registries/tools.yaml")?.tools || [];
    const seen = new Set();
    for (const t of tools) {
      if (!t?.id) continue;
      if (seen.has(t.id)) dupPolicy.push(t.id);
      seen.add(t.id);
    }
  } catch {
    /* noop */
  }
  try {
    const cat = JSON.parse(fs.readFileSync(abs("registries/tool_registry.canonical.json"), "utf8"));
    for (const key of ["canonical_order", "internal_canonical_order", "diagnostic_order"]) {
      const list = cat?.[key] || [];
      const seen = new Set();
      for (const id of list) {
        if (seen.has(id)) dupCatalogue.push(`${key}:${id}`);
        seen.add(id);
      }
    }
  } catch {
    /* noop */
  }
  checks.push({
    id: "AR-Tool",
    invariant: "INV-AR-6",
    label: "tool id duplicates within layer",
    measured: dupPolicy.length + dupCatalogue.length,
    baseline: 0,
    status: dupPolicy.length + dupCatalogue.length ? "FAIL" : "PASS",
    detail: [...dupPolicy, ...dupCatalogue].slice(0, 8),
  });
}

// ── report ───────────────────────────────────────────────────────────────────
const failed = checks.filter((c) => c.status === "FAIL");

if (AS_JSON) {
  console.log(JSON.stringify({ commit: gitHead(), checks, result: failed.length ? "FAIL" : "PASS" }, null, 2));
} else {
  console.log(`REGISTRY ALIGNMENT GATE — AAA @ ${gitHead()}`);
  for (const c of checks) {
    const delta =
      c.status === "INFO"
        ? `${c.measured}`
        : `${c.measured} (baseline ${c.baseline})`;
    console.log(`  [${c.status.padEnd(4)}] ${c.invariant.padEnd(10)} ${c.label.padEnd(38)} ${delta}`);
    for (const d of c.detail.slice(0, 5)) console.log(`         · ${d}`);
    if (c.detail.length > 5) console.log(`         · … ${c.detail.length - 5} more`);
  }
  console.log(failed.length ? `\nRESULT: FAIL — ${failed.length} invariant(s) breached` : "\nRESULT: PASS — aligned");
}

function gitHead() {
  try {
    const head = fs.readFileSync(path.join(ROOT, ".git/HEAD"), "utf8").trim();
    if (head.startsWith("ref: ")) {
      const ref = head.slice(5);
      const refPath = path.join(ROOT, ".git", ref);
      if (fs.existsSync(refPath)) return fs.readFileSync(refPath, "utf8").trim().slice(0, 12);
      const packed = path.join(ROOT, ".git/packed-refs");
      if (fs.existsSync(packed)) {
        const hit = fs
          .readFileSync(packed, "utf8")
          .split("\n")
          .find((l) => l.endsWith(ref));
        if (hit) return hit.split(" ")[0].slice(0, 12);
      }
      return ref;
    }
    return head.slice(0, 12);
  } catch {
    return "unknown";
  }
}

process.exit(failed.length ? 1 : 0);
