import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { parse as parseYaml } from "yaml";

const root = process.cwd();
const errors = [];
const warnings = [];

function readFile(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8");
}

function exists(relativePath) {
  return fs.existsSync(path.join(root, relativePath));
}

function loadYaml(relativePath) {
  return parseYaml(readFile(relativePath));
}

function loadJson(relativePath) {
  return JSON.parse(readFile(relativePath));
}

function externalExists(absolutePath) {
  return fs.existsSync(absolutePath);
}

function assertEqual(actual, expected, label) {
  if (actual !== expected) {
    errors.push(`${label}: expected '${expected}', got '${actual}'`);
  }
}

function assertArrayIds(items, label, expectedIds = []) {
  if (!Array.isArray(items)) {
    errors.push(`${label} must be an array`);
    return new Set();
  }
  const ids = new Set();
  for (const item of items) {
    if (!item?.id) {
      errors.push(`${label}: entry missing id`);
      continue;
    }
    if (ids.has(item.id)) {
      errors.push(`${label}: duplicate id '${item.id}'`);
    }
    ids.add(item.id);
  }
  for (const expectedId of expectedIds) {
    if (!ids.has(expectedId)) {
      errors.push(`${label}: missing required id '${expectedId}'`);
    }
  }
  return ids;
}

const rootConfig = loadYaml("ROOT_AGENT_CONFIG.yaml");
const opencodeCard = loadJson("agents/opencode/agent-card.json");
const opencodeToolbench = loadYaml("registries/opencode_toolbench.yaml");
const forgeInstruments = loadYaml("registries/forge_instruments.yaml");
const hosts = loadYaml("registries/hosts.yaml");
const packageJson = loadJson("package.json");

assertEqual(rootConfig.version, 1, "ROOT_AGENT_CONFIG.yaml:version");
assertEqual(rootConfig.root_policy?.root_config_is_source, true, "root_policy.root_config_is_source");
assertEqual(
  rootConfig.root_policy?.per_agent_dirs_are_views,
  true,
  "root_policy.per_agent_dirs_are_views",
);
if (!rootConfig.honest_self_audit?.godel_boundary?.note) {
  errors.push("ROOT_AGENT_CONFIG.yaml must carry honest_self_audit.godel_boundary.note");
}
if (!Array.isArray(rootConfig.honest_self_audit?.uncertain) || rootConfig.honest_self_audit.uncertain.length === 0) {
  errors.push("ROOT_AGENT_CONFIG.yaml must carry at least one honest_self_audit.uncertain item");
}

assertArrayIds(rootConfig.aaa_warga, "aaa_warga", [
  "333-AGI",
  "555-ASI",
  "888-APEX",
  "A-AUDIT",
  "A-ARCHIVE",
]);
assertArrayIds(rootConfig.runtime_peers, "runtime_peers", ["hermes-asi", "openclaw", "777-forge"]);
assertArrayIds(rootConfig.organ_peers, "organ_peers", [
  "arifos-kernel",
  "aforge-executor",
  "geox-witness",
  "wealth-witness",
  "well-mirror",
  "aaa-gateway",
]);
assertArrayIds(rootConfig.forge_instruments, "forge_instruments", ["opencode"]);

const opencodeRoot = rootConfig.forge_instruments.find((item) => item.id === "opencode");
const fi001 = forgeInstruments.instruments.find((item) => item.id === "FI-001");
const opencodeHost = hosts.hosts.find((item) => item.id === "opencode");

if (!opencodeRoot) {
  errors.push("ROOT_AGENT_CONFIG.yaml: missing forge_instruments opencode");
} else {
  for (const localPath of [opencodeRoot.agent_card, opencodeRoot.repo_config_view]) {
    if (!exists(localPath)) {
      errors.push(`opencode: missing local config path '${localPath}'`);
    }
  }

  assertEqual(opencodeCard.id, "opencode", "agents/opencode/agent-card.json:id");
  assertEqual(opencodeCard.version, opencodeRoot.version, "opencode card version");
  assertEqual(opencodeCard.config, opencodeRoot.live_config, "opencode card config");
  assertEqual(opencodeCard.root_config, opencodeRoot.root_config_ref, "opencode card root_config");
  assertEqual(opencodeCard.model, opencodeRoot.model, "opencode card model");

  assertEqual(opencodeToolbench.opencode_version, opencodeRoot.version, "opencode toolbench version");
  assertEqual(opencodeToolbench.opencode_binary, opencodeRoot.binary, "opencode toolbench binary");
  assertEqual(
    opencodeToolbench.config_paths?.root_config,
    `/root/AAA/${opencodeRoot.root_config_ref}`,
    "opencode toolbench root_config",
  );
  assertEqual(
    opencodeToolbench.config_paths?.live_global,
    opencodeRoot.live_config,
    "opencode toolbench live_global",
  );

  if (!fi001) {
    errors.push("registries/forge_instruments.yaml: missing FI-001");
  } else {
    assertEqual(String(fi001.version), opencodeRoot.version, "FI-001 version");
    assertEqual(fi001.binary, opencodeRoot.binary, "FI-001 binary");
    assertEqual(fi001.model, opencodeRoot.model, "FI-001 model");
    assertEqual(fi001.config_path, opencodeRoot.live_config, "FI-001 config_path");
    assertEqual(fi001.root_config_ref, `/root/AAA/${opencodeRoot.root_config_ref}`, "FI-001 root_config_ref");
  }

  if (!opencodeHost) {
    errors.push("registries/hosts.yaml: missing opencode host");
  } else if (!opencodeHost.config_paths?.includes("ROOT_AGENT_CONFIG.yaml")) {
    errors.push("opencode host config_paths must include ROOT_AGENT_CONFIG.yaml");
  }

  if (externalExists(opencodeRoot.live_config)) {
    const live = JSON.parse(fs.readFileSync(opencodeRoot.live_config, "utf8"));
    assertEqual(live.model, opencodeRoot.model, "live opencode model");
    assertEqual(live.small_model, opencodeRoot.small_model, "live opencode small_model");
    const liveMcp = Object.keys(live.mcp ?? {}).sort();
    const rootMcp = [...(opencodeRoot.mcp_servers ?? [])].sort();
    if (JSON.stringify(liveMcp) !== JSON.stringify(rootMcp)) {
      errors.push(`live opencode mcp roster mismatch: expected ${rootMcp.join(",")}, got ${liveMcp.join(",")}`);
    }
  } else {
    warnings.push(`opencode live config not present at ${opencodeRoot.live_config}; skipped local runtime check`);
  }
}

if (!packageJson.scripts?.["validate:root-agents"]) {
  errors.push("package.json missing validate:root-agents script");
}

if (errors.length) {
  console.error("Root agent config validation failed:");
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  if (warnings.length) {
    console.error("Warnings:");
    for (const warning of warnings) {
      console.error(`- ${warning}`);
    }
  }
  process.exit(1);
}

console.log("Root agent config validation passed.");
console.log(
  JSON.stringify(
    {
      aaaWarga: rootConfig.aaa_warga.length,
      runtimePeers: rootConfig.runtime_peers.length,
      organPeers: rootConfig.organ_peers.length,
      forgeInstruments: rootConfig.forge_instruments.length,
      warnings,
    },
    null,
    2,
  ),
);
