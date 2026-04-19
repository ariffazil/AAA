import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { parse as parseYaml } from "yaml";

const root = process.cwd();
const outDir = path.join(root, "dist", "aaa");

function ensureDir(target) {
  fs.mkdirSync(target, { recursive: true });
}

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(root, relativePath), "utf8"));
}

function readYaml(relativePath) {
  return parseYaml(fs.readFileSync(path.join(root, relativePath), "utf8"));
}

function writeJson(relativePath, value) {
  const fullPath = path.join(root, relativePath);
  ensureDir(path.dirname(fullPath));
  fs.writeFileSync(fullPath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

const sources = {
  registries: {
    agents: readYaml("registries/agents.yaml"),
    bundles: readYaml("registries/bundles.yaml"),
    domains: readYaml("registries/domains.yaml"),
    hosts: readYaml("registries/hosts.yaml"),
    integrations: readYaml("registries/integrations.yaml"),
    servers: readYaml("registries/servers.yaml"),
    skills: readYaml("registries/skills.yaml"),
    tools: readYaml("registries/tools.yaml"),
    workflows: readYaml("registries/workflows.yaml"),
  },
  contracts: {
    decisions: readYaml("contracts/decisions/888-999-decisions.yaml"),
    federation: readYaml("contracts/federation/111-sense.yaml"),
    goals: readYaml("contracts/goals/222-goals.yaml"),
    governance: readYaml("contracts/governance/666-777-gates.yaml"),
    init: readYaml("contracts/init/000-init.yaml"),
    hosts: readYaml("contracts/hosts/contracts.yaml"),
    org: readYaml("contracts/org/333-org-units.yaml"),
    skills: readYaml("contracts/skills/packages.yaml"),
    workflows: readYaml("contracts/workflows/contracts.yaml"),
  },
  cockpit: readYaml("contracts/cockpit/model.yaml"),
  schemas: {
    decisionVault: readJson("schemas/decision-vault.schema.json"),
    federation: readJson("schemas/federation-contract.schema.json"),
    goalChain: readJson("schemas/goal-chain.schema.json"),
    governanceGates: readJson("schemas/governance-gates.schema.json"),
    init: readJson("schemas/init-contract.schema.json"),
    cockpit: readJson("schemas/cockpit-model.schema.json"),
    orgTopology: readJson("schemas/org-topology.schema.json"),
  },
};

const index = {
  version: 1,
  export_format: "json",
  authoring_format: "yaml",
  outputs: [
    "dist/aaa/index.json",
    "dist/aaa/contracts.bundle.json",
    "dist/aaa/cockpit-model.json",
  ],
  sections: {
    registries: Object.keys(sources.registries),
    contracts: Object.keys(sources.contracts),
    schemas: Object.keys(sources.schemas),
  },
};

const bundle = {
  version: 1,
  registries: sources.registries,
  contracts: sources.contracts,
  schemas: sources.schemas,
};

writeJson(path.join("dist", "aaa", "index.json"), index);
writeJson(path.join("dist", "aaa", "contracts.bundle.json"), bundle);
writeJson(path.join("dist", "aaa", "cockpit-model.json"), sources.cockpit);

console.log(`AAA JSON export complete: ${outDir}`);
