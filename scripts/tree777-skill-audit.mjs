#!/usr/bin/env node
/**
 * TREE777 skill catalog auditor and synchronizer.
 *
 * AAA owns canonical skill bodies. V3 and harness meshes are routing views.
 * `--sync` mechanically rebuilds the deployable registry and package membership
 * from live SKILL.md bodies; the default mode is read-only and CI-safe.
 */

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { parse as parseYaml, stringify as stringifyYaml } from "yaml";

const root = process.cwd();
const skillsRoot = path.join(root, "skills");
const registryPath = path.join(root, "registries/skills.yaml");
const packagesPath = path.join(root, "contracts/skills/packages.yaml");
const syncMode = process.argv.includes("--sync");
const excludedSegments = new Set([
  "_retired",
  "ARCHIVE",
  ".archive-2026-07-11",
  ".archive-openclaw-legacy",
  "node_modules",
]);

function normalizeId(value) {
  return String(value ?? "")
    .normalize("NFKD")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function walkSkillFiles(dir, output = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (excludedSegments.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isSymbolicLink()) {
      const linkedSkill = path.join(full, "SKILL.md");
      if (fs.existsSync(linkedSkill)) output.push(linkedSkill);
      continue;
    }
    if (entry.isDirectory()) walkSkillFiles(full, output);
    else if (entry.name === "SKILL.md") output.push(full);
  }
  return output;
}

function parseFrontmatter(file) {
  const content = fs.readFileSync(file, "utf8");
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!match) return { content, frontmatter: null, error: "missing YAML frontmatter" };
  try {
    return { content, frontmatter: parseYaml(match[1]) ?? {}, error: null };
  } catch (error) {
    return { content, frontmatter: null, error: `malformed YAML frontmatter: ${error.message}` };
  }
}

function firstDescription(content) {
  return (
    content
      .replace(/^---[\s\S]*?---\s*/, "")
      .split(/\r?\n/)
      .map((line) => line.trim())
      .find((line) => line && !line.startsWith("#") && !line.startsWith(">")) ?? ""
  );
}

function packageIdFor(relativePath) {
  const top = relativePath.split(path.sep)[0];
  if (top === ".system") return "system-skills";
  if (top === "substrate") return "substrate";
  if (top === "knowledge") return "knowledge";
  if (top === "reflective") return "reflective";
  if (/^AGI-/i.test(top)) return "agi-reasoning";
  if (/^ASI-|^asi_/i.test(top)) return "asi-governance";
  if (/^APEX-|^apex[_-]/i.test(top)) return "apex-gates";
  if (/^AUDIT-/i.test(top)) return "audit";
  if (/^FORGE-/i.test(top)) return "forge";
  return "domain-and-harness";
}

function discover() {
  const warnings = [];
  const candidates = [];
  // Universal convenience symlinks and their canonical nested bodies share a realpath.
  // Catalog the body once, preferring the physical path over its view.
  const filesByRealpath = new Map();
  for (const file of walkSkillFiles(skillsRoot)) {
    const real = fs.realpathSync(file);
    const current = filesByRealpath.get(real);
    if (!current || file === real) filesByRealpath.set(real, file);
  }
  for (const file of [...filesByRealpath.values()].sort()) {
    const parsed = parseFrontmatter(file);
    const relativePath = path.relative(skillsRoot, file);
    if (parsed.error) {
      warnings.push(`${relativePath}: ${parsed.error}; excluded from active catalog`);
      continue;
    }
    const fm = parsed.frontmatter;
    const directoryId = normalizeId(path.basename(path.dirname(file)));
    const preferredId = normalizeId(fm.id || fm.name || directoryId);
    if (!preferredId) {
      warnings.push(`${relativePath}: no usable id or name; excluded from active catalog`);
      continue;
    }
    candidates.push({ file, relativePath, parsed, fm, preferredId });
  }

  const grouped = new Map();
  for (const candidate of candidates) {
    if (!grouped.has(candidate.preferredId)) grouped.set(candidate.preferredId, []);
    grouped.get(candidate.preferredId).push(candidate);
  }

  const skills = [];
  for (const [preferredId, group] of grouped) {
    group.sort((a, b) => a.relativePath.split(path.sep).length - b.relativePath.split(path.sep).length || a.relativePath.localeCompare(b.relativePath));
    for (const [index, candidate] of group.entries()) {
      const suffix = normalizeId(path.dirname(candidate.relativePath));
      const id = index === 0 ? preferredId : `${preferredId}--${suffix}`;
      const fm = candidate.fm;
      const skill = {
        id,
        name: String(fm.name || fm.id || path.basename(path.dirname(candidate.file))),
        version: String(fm.version || "0.0.0"),
        description: String(fm.description || firstDescription(candidate.parsed.content)),
        owner: String(fm.owner || "AAA"),
        risk_tier: String(fm.risk_tier || "low").toLowerCase(),
        status: String(fm.status || "active").toLowerCase(),
        source_path: `skills/${candidate.relativePath}`,
        package: packageIdFor(candidate.relativePath),
      };
      for (const field of ["superseded_by", "orthogonal_tags", "floor_scope"]) {
        if (fm[field] !== undefined) skill[field] = fm[field];
      }
      skills.push(skill);
    }
  }
  skills.sort((a, b) => a.id.localeCompare(b.id));
  return { skills, warnings };
}

const packageDescriptions = {
  "system-skills": "System-maintained skill creation, installation, and media capabilities.",
  substrate: "Universal BOOT substrate skills loaded before domain work.",
  knowledge: "Universal physics, mathematics, and language grounding skills.",
  reflective: "Sovereign recognition and reflective boundary skills.",
  "agi-reasoning": "Planning, exploration, synthesis, and reasoning skills.",
  "asi-governance": "Agent governance, observability, memory, and constitutional reasoning skills.",
  "apex-gates": "Approval, scope, floor, reversibility, and verdict gate skills.",
  audit: "Independent audit, drift, and catalog verification skills.",
  forge: "Implementation, operations, MCP, repository, and infrastructure skills.",
  "domain-and-harness": "Domain-specific and harness-native skills that remain inside the AAA catalog.",
};

function buildPackages(skills) {
  return Object.entries(packageDescriptions).map(([id, description]) => ({
    id,
    name: id.split("-").map((part) => part[0].toUpperCase() + part.slice(1)).join(" "),
    description,
    skills: skills.filter((skill) => skill.package === id).map((skill) => ({ id: skill.id })),
  })).filter((pkg) => pkg.skills.length > 0);
}

function writeCatalog(skills, packages) {
  const generated = new Date().toISOString();
  const registry = {
    version: 3,
    generated,
    total_active: skills.length,
    source: "canonical-skill-bodies",
    routing_view: "skills/FEDERATED_SKILLS_REGISTRY_V3.yaml",
    alias_view: "skills/SKILL_ALIAS_TABLE.json",
    doctrine: "AAA is the catalog; V3, aliases, packages, and harness meshes are views",
    skills,
  };
  const packagesDocument = {
    version: 2,
    generated,
    source: "registries/skills.yaml",
    metadata_rule: "Skill metadata lives once in the registry; packages contain identity references only",
    packages,
  };
  fs.writeFileSync(registryPath, stringifyYaml(registry, { lineWidth: 100 }));
  fs.writeFileSync(packagesPath, stringifyYaml(packagesDocument, { lineWidth: 100 }));
}

function triggerLint(skill) {
  const content = fs.readFileSync(path.join(root, skill.source_path), "utf8");
  const hasUse = /^##+\s+(use when|when to use)\b/im.test(content);
  const hasExclusion = /^##+\s+(do not use when|when not to use|when not to use this skill)\b/im.test(content);
  const vague = /\b(help|assist|improve|manage|optimize|support)\b/i.test(skill.description);
  const highPower = ["high", "critical"].includes(skill.risk_tier) && /\b(destruct|delete|secret|credential|irreversible|deploy)\w*/i.test(content);
  const governed = /888[_ ]HOLD|arifOS|F13/i.test(content);
  return { hasUse, hasExclusion, vague, l3: highPower && !governed };
}

function audit(discovered, discoveryWarnings) {
  const errors = [];
  const warnings = [...discoveryWarnings];
  const registry = parseYaml(fs.readFileSync(registryPath, "utf8"));
  const packageDocument = parseYaml(fs.readFileSync(packagesPath, "utf8"));
  const registered = registry.skills ?? [];
  const packages = packageDocument.packages ?? [];
  const discoveredIds = new Set(discovered.map((skill) => skill.id));
  const registeredIds = new Set(registered.map((skill) => skill.id));

  if (registeredIds.size !== registered.length) errors.push("registry contains duplicate skill ids");
  if (discoveredIds.size !== discovered.length) errors.push("discovery produced duplicate skill ids");
  for (const id of discoveredIds) if (!registeredIds.has(id)) errors.push(`${id}: body missing from registry`);
  for (const skill of registered) {
    if (!discoveredIds.has(skill.id)) errors.push(`${skill.id}: registry entry has no active body`);
    if (!skill.source_path || !fs.existsSync(path.join(root, skill.source_path))) errors.push(`${skill.id}: source_path is missing`);
  }

  const assignments = new Map();
  for (const pkg of packages) {
    for (const ref of pkg.skills ?? []) {
      if (!registeredIds.has(ref.id)) errors.push(`${pkg.id}: unknown skill '${ref.id}'`);
      if (assignments.has(ref.id)) errors.push(`${ref.id}: assigned to both ${assignments.get(ref.id)} and ${pkg.id}`);
      assignments.set(ref.id, pkg.id);
    }
  }
  for (const skill of registered) if (!assignments.has(skill.id)) errors.push(`${skill.id}: not assigned to a package`);

  const lint = { l1: 0, l2: 0, l3: 0 };
  for (const skill of registered) {
    if (!skill.source_path || !fs.existsSync(path.join(root, skill.source_path))) continue;
    const result = triggerLint(skill);
    if (result.vague) lint.l1 += 1;
    if (!result.hasUse || !result.hasExclusion) lint.l2 += 1;
    if (result.l3) {
      lint.l3 += 1;
      errors.push(`${skill.id}: L3 high-power skill lacks explicit arifOS/888_HOLD/F13 path`);
    }
  }
  if (lint.l1) warnings.push(`${lint.l1} skills have vague description verbs (L1)`);
  if (lint.l2) warnings.push(`${lint.l2} skills lack an explicit Use When or Do Not Use When section (L2)`);

  const report = {
    report_type: "TREE777_SKILL_AUDIT",
    timestamp_utc: new Date().toISOString(),
    summary: {
      discovered_bodies: discovered.length,
      registered_skills: registered.length,
      packages: packages.length,
      errors: errors.length,
      warnings: warnings.length,
      trigger_lint: lint,
    },
    errors,
    warnings,
  };
  console.log(JSON.stringify(report, null, 2));
  return errors.length === 0 ? 0 : 1;
}

const discovered = discover();
if (syncMode) writeCatalog(discovered.skills, buildPackages(discovered.skills));
process.exit(audit(discovered.skills, discovered.warnings));
