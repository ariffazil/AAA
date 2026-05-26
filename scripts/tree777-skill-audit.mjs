#!/usr/bin/env node
/**
 * TREE777 Skill Audit
 *
 * Weekly audit of the AAA skill library. Checks:
 * - Every registered skill has a SKILL.md
 * - No orphan skills (directory exists but not registered)
 * - SKILL.md conforms to canonical template
 * - Promotion readiness (examples.md + tests.md present)
 * - Orphan links (broken references)
 *
 * Run: node scripts/tree777-skill-audit.mjs
 */

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { parse as parseYaml } from "yaml";

const root = process.cwd();
const skillsDir = path.join(root, "skills");
const registryPath = "registries/skills.yaml";

function readFile(relativePath) {
  const fullPath = path.join(root, relativePath);
  return fs.readFileSync(fullPath, "utf8");
}

function exists(relativePath) {
  return fs.existsSync(path.join(root, relativePath));
}

function loadYaml(relativePath) {
  return parseYaml(readFile(relativePath));
}

function listSkillDirs() {
  if (!fs.existsSync(skillsDir)) return [];
  return fs
    .readdirSync(skillsDir, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .filter((n) => n !== "spatial-grounding"); // pre-existing, not canonical
}

function parseSkillFrontmatter(skillPath) {
  const content = readFile(skillPath);
  const match = content.match(/^---\n([\s\S]*?)\n---\n/);
  if (!match) return null;
  try {
    return parseYaml(match[1]);
  } catch {
    return null;
  }
}

function findLinks(skillPath) {
  const content = readFile(skillPath);
  // Find markdown links [text](path) and bare paths
  const links = [];
  const mdLinkRe = /\[([^\]]*)\]\(([^)]+)\)/g;
  let m;
  while ((m = mdLinkRe.exec(content)) !== null) {
    links.push(m[2]);
  }
  return links;
}

function isLinkValid(link) {
  // Absolute URLs are considered valid
  if (link.startsWith("http://") || link.startsWith("https://")) return true;
  // Relative paths — check from repo root
  return exists(link);
}

const errors = [];
const warnings = [];
const promotions = [];

const registry = loadYaml(registryPath);
const registeredSkills = registry.skills ?? [];
const registeredIds = new Set(registeredSkills.map((s) => s.id));
const skillDirs = listSkillDirs();

// 1. Registered skills must have SKILL.md
for (const skill of registeredSkills) {
  const skillMdPath = path.join("skills", skill.id, "SKILL.md");
  if (!exists(skillMdPath)) {
    errors.push(`${skill.id}: missing SKILL.md at ${skillMdPath}`);
    continue;
  }

  // 1a. Frontmatter check
  const frontmatter = parseSkillFrontmatter(skillMdPath);
  if (!frontmatter) {
    errors.push(`${skill.id}: SKILL.md missing or malformed YAML frontmatter`);
  } else {
    const requiredFields = ["id", "name", "version", "description", "owner", "risk_tier"];
    for (const field of requiredFields) {
      if (!frontmatter[field]) {
        errors.push(`${skill.id}: frontmatter missing '${field}'`);
      }
    }
    if (frontmatter.id && frontmatter.id !== skill.id) {
      errors.push(`${skill.id}: frontmatter id '${frontmatter.id}' does not match registry`);
    }
  }

  // 1b. Promotion readiness
  const examplesPath = path.join("skills", skill.id, "examples.md");
  const testsPath = path.join("skills", skill.id, "tests.md");
  const hasExamples = exists(examplesPath);
  const hasTests = exists(testsPath);

  if (hasExamples && hasTests) {
    promotions.push({
      id: skill.id,
      status: "ready",
      reason: "examples.md and tests.md present",
    });
  } else {
    warnings.push(
      `${skill.id}: promotion blocked — missing ${!hasExamples ? "examples.md" : ""}${!hasExamples && !hasTests ? " + " : ""}${!hasTests ? "tests.md" : ""}`,
    );
    promotions.push({
      id: skill.id,
      status: "blocked",
      reason: `missing ${!hasExamples ? "examples.md" : ""}${!hasExamples && !hasTests ? ", " : ""}${!hasTests ? "tests.md" : ""}`,
    });
  }

  // 1c. Orphan links
  const links = findLinks(skillMdPath);
  for (const link of links) {
    if (!isLinkValid(link)) {
      warnings.push(`${skill.id}: orphan link '${link}'`);
    }
  }
}

// 2. Orphan skills (directory exists but not registered)
for (const dir of skillDirs) {
  if (!registeredIds.has(dir)) {
    warnings.push(`orphan skill directory: skills/${dir}/ (not in ${registryPath})`);
  }
}

// 3. README and template check
if (!exists("skills/README.md")) {
  errors.push("missing skills/README.md");
}
if (!exists("skills/SKILL_TEMPLATE.md")) {
  errors.push("missing skills/SKILL_TEMPLATE.md");
}

// Report
const report = {
  report_type: "TREE777_SKILL_AUDIT",
  timestamp_utc: new Date().toISOString(),
  summary: {
    registered_skills: registeredSkills.length,
    skill_directories: skillDirs.length,
    errors: errors.length,
    warnings: warnings.length,
    promotions_ready: promotions.filter((p) => p.status === "ready").length,
    promotions_blocked: promotions.filter((p) => p.status === "blocked").length,
  },
  errors,
  warnings,
  promotions,
};

console.log(JSON.stringify(report, null, 2));

if (errors.length > 0) {
  process.exit(1);
}

process.exit(0);
