import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { parse as parseYaml } from "yaml";

const root = process.cwd();

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

function loadJson(relativePath) {
  return JSON.parse(readFile(relativePath));
}

function expectArray(value, label, errors) {
  if (!Array.isArray(value)) {
    errors.push(`${label} must be an array`);
    return [];
  }
  return value;
}

function pushRefErrors({ ownerId, field, refs, validIds, errors }) {
  for (const ref of refs) {
    if (!validIds.has(ref)) {
      errors.push(`${ownerId}: unknown ${field} reference '${ref}'`);
    }
  }
}

function ensureUniqueIds(items, label, errors) {
  const seen = new Set();
  for (const item of items) {
    if (!item?.id) {
      errors.push(`${label}: item missing id`);
      continue;
    }
    if (seen.has(item.id)) {
      errors.push(`${label}: duplicate id '${item.id}'`);
      continue;
    }
    seen.add(item.id);
  }
}

const errors = [];

const registries = {
  agents: loadYaml("registries/agents.yaml"),
  bundles: loadYaml("registries/bundles.yaml"),
  domains: loadYaml("registries/domains.yaml"),
  hosts: loadYaml("registries/hosts.yaml"),
  integrations: loadYaml("registries/integrations.yaml"),
  servers: loadYaml("registries/servers.yaml"),
  skills: loadYaml("registries/skills.yaml"),
  tools: loadYaml("registries/tools.yaml"),
  workflows: loadYaml("registries/workflows.yaml"),
};

const a2aAgents = loadYaml("a2a/registry/agents.yaml");
const bridge = loadYaml("openclaw/a2a/bridge.yaml");
const authPolicy = loadYaml("a2a/policies/auth.yaml");
const decisionsContract = loadYaml("contracts/decisions/888-999-decisions.yaml");
const governanceContract = loadYaml("contracts/governance/666-777-gates.yaml");
const goalChainContract = loadYaml("contracts/goals/222-goals.yaml");
const initContract = loadYaml("contracts/init/000-init.yaml");
const federationContract = loadYaml("contracts/federation/111-sense.yaml");
const hostContractsCatalog = loadYaml("contracts/hosts/contracts.yaml");
const orgTopologyContract = loadYaml("contracts/org/333-org-units.yaml");
const skillPackagesCatalog = loadYaml("contracts/skills/packages.yaml");
const workflowContractsCatalog = loadYaml("contracts/workflows/contracts.yaml");
const sourceAgentCard = loadJson("a2a/agent-cards/aaa-gateway.json");

const agents = expectArray(registries.agents.agents, "registries/agents.yaml:agents", errors);
const bundles = expectArray(registries.bundles.bundles, "registries/bundles.yaml:bundles", errors);
const domains = expectArray(registries.domains.domains, "registries/domains.yaml:domains", errors);
const hosts = expectArray(registries.hosts.hosts, "registries/hosts.yaml:hosts", errors);
const integrations = expectArray(
  registries.integrations.integrations,
  "registries/integrations.yaml:integrations",
  errors,
);
const servers = expectArray(registries.servers.servers, "registries/servers.yaml:servers", errors);
const skills = expectArray(registries.skills.skills, "registries/skills.yaml:skills", errors);
const tools = expectArray(registries.tools.tools, "registries/tools.yaml:tools", errors);
const workflows = expectArray(
  registries.workflows.workflows,
  "registries/workflows.yaml:workflows",
  errors,
);
const a2aRegistryAgents = expectArray(a2aAgents.agents, "a2a/registry/agents.yaml:agents", errors);
const bridgeBindings = expectArray(bridge.bindings, "openclaw/a2a/bridge.yaml:bindings", errors);
const hostContracts = expectArray(
  hostContractsCatalog.host_contracts,
  "contracts/hosts/contracts.yaml:host_contracts",
  errors,
);
const skillPackages = expectArray(
  skillPackagesCatalog.skill_packages,
  "contracts/skills/packages.yaml:skill_packages",
  errors,
);
const workflowContracts = expectArray(
  workflowContractsCatalog.workflow_contracts,
  "contracts/workflows/contracts.yaml:workflow_contracts",
  errors,
);
const federationPublicSurfaces = expectArray(
  federationContract.public_surfaces,
  "contracts/federation/111-sense.yaml:public_surfaces",
  errors,
);
const federationTrustTiers = expectArray(
  federationContract.trust_tiers,
  "contracts/federation/111-sense.yaml:trust_tiers",
  errors,
);
const federationIngressSurfaces = expectArray(
  federationContract.ingress_surfaces,
  "contracts/federation/111-sense.yaml:ingress_surfaces",
  errors,
);
const governanceGates = expectArray(
  governanceContract.governance_gates,
  "contracts/governance/666-777-gates.yaml:governance_gates",
  errors,
);
const budgets = expectArray(
  governanceContract.budgets,
  "contracts/governance/666-777-gates.yaml:budgets",
  errors,
);
const goals = expectArray(goalChainContract.goals, "contracts/goals/222-goals.yaml:goals", errors);
const goalTasks = expectArray(goalChainContract.tasks, "contracts/goals/222-goals.yaml:tasks", errors);
const goalVerdicts = expectArray(
  goalChainContract.verdicts,
  "contracts/goals/222-goals.yaml:verdicts",
  errors,
);
const initBootSequence = expectArray(
  initContract.boot_sequence,
  "contracts/init/000-init.yaml:boot_sequence",
  errors,
);
const initAnchors = expectArray(
  initContract.state_anchors,
  "contracts/init/000-init.yaml:state_anchors",
  errors,
);
const orgUnits = expectArray(
  orgTopologyContract.org_units,
  "contracts/org/333-org-units.yaml:org_units",
  errors,
);
const topologyEdges = expectArray(
  orgTopologyContract.topology_edges,
  "contracts/org/333-org-units.yaml:topology_edges",
  errors,
);
const decisions = expectArray(
  decisionsContract.decisions,
  "contracts/decisions/888-999-decisions.yaml:decisions",
  errors,
);
const vaultExports = expectArray(
  decisionsContract.vault_exports,
  "contracts/decisions/888-999-decisions.yaml:vault_exports",
  errors,
);

ensureUniqueIds(agents, "agents", errors);
ensureUniqueIds(bundles, "bundles", errors);
ensureUniqueIds(hosts, "hosts", errors);
ensureUniqueIds(integrations, "integrations", errors);
ensureUniqueIds(servers, "servers", errors);
ensureUniqueIds(skills, "skills", errors);
ensureUniqueIds(tools, "tools", errors);
ensureUniqueIds(workflows, "workflows", errors);
ensureUniqueIds(hostContracts, "host_contracts", errors);
ensureUniqueIds(skillPackages, "skill_packages", errors);
ensureUniqueIds(workflowContracts, "workflow_contracts", errors);
ensureUniqueIds(federationPublicSurfaces, "federation_public_surfaces", errors);
ensureUniqueIds(federationTrustTiers, "federation_trust_tiers", errors);
ensureUniqueIds(federationIngressSurfaces, "federation_ingress_surfaces", errors);
ensureUniqueIds(governanceGates, "governance_gates", errors);
ensureUniqueIds(budgets, "governance_budgets", errors);
ensureUniqueIds(goals, "goal_chain_goals", errors);
ensureUniqueIds(goalTasks, "goal_chain_tasks", errors);
ensureUniqueIds(goalVerdicts, "goal_chain_verdicts", errors);
ensureUniqueIds(initAnchors, "init_state_anchors", errors);
ensureUniqueIds(orgUnits, "org_units", errors);
ensureUniqueIds(topologyEdges, "org_topology_edges", errors);
ensureUniqueIds(decisions, "decision_records", errors);
ensureUniqueIds(vaultExports, "vault_exports", errors);

const agentIds = new Set(agents.map((item) => item.id));
const bundleIds = new Set(bundles.map((item) => item.id));
const domainIds = new Set(domains.map((item) => item.id));
const hostIds = new Set(hosts.map((item) => item.id));
const integrationIds = new Set(integrations.map((item) => item.id));
const serverIds = new Set(servers.map((item) => item.id));
const skillIds = new Set(skills.map((item) => item.id));
const toolIds = new Set(tools.map((item) => item.id));
const workflowIds = new Set(workflows.map((item) => item.id));
const a2aAgentIds = new Set(a2aRegistryAgents.map((item) => item.agent_id));
const hostContractIds = new Set(hostContracts.map((item) => item.id));
const skillPackageIds = new Set(skillPackages.map((item) => item.id));
const workflowContractIds = new Set(workflowContracts.map((item) => item.id));
const requiredRootCanons = new Set(initContract.required_root_canons ?? []);
const authPeerClasses = new Map(Object.entries(authPolicy.peer_classes ?? {}));
const goalIds = new Set(goals.map((item) => item.id));
const goalTaskIds = new Set(goalTasks.map((item) => item.id));
const orgUnitIds = new Set(orgUnits.map((item) => item.id));
const federationTrustTierIds = new Set(federationTrustTiers.map((item) => item.id));
const governanceGateIds = new Set(governanceGates.map((item) => item.id));
const budgetIds = new Set(budgets.map((item) => item.id));
const decisionIds = new Set(decisions.map((item) => item.id));
const vaultExportIds = new Set(vaultExports.map((item) => item.id));

for (const agent of agents) {
  if (!hostIds.has(agent.host_binding)) {
    errors.push(`${agent.id}: unknown host_binding '${agent.host_binding}'`);
  }
  pushRefErrors({
    ownerId: agent.id,
    field: "tool",
    refs: agent.allowed_tools ?? [],
    validIds: toolIds,
    errors,
  });
  pushRefErrors({
    ownerId: agent.id,
    field: "server",
    refs: agent.allowed_servers ?? [],
    validIds: serverIds,
    errors,
  });
  pushRefErrors({
    ownerId: agent.id,
    field: "peer",
    refs: agent.allowed_peers ?? [],
    validIds: agentIds,
    errors,
  });
  if (agent.intelligence_band !== agent.intelligence_tier) {
    errors.push(`${agent.id}: intelligence_band must match intelligence_tier`);
  }
  if (agent.role === "engineer" && agent.separation_of_duties?.cannot_self_seal !== true) {
    errors.push(`${agent.id}: engineer must set separation_of_duties.cannot_self_seal=true`);
  }
}

for (const server of servers) {
  pushRefErrors({
    ownerId: server.id,
    field: "tool",
    refs: server.tools ?? [],
    validIds: toolIds,
    errors,
  });
}

for (const skill of skills) {
  if (skill.package_ref !== skill.id) {
    errors.push(`${skill.id}: package_ref must match skill id`);
  }
  if (!skillPackageIds.has(skill.package_ref)) {
    errors.push(`${skill.id}: missing skill package '${skill.package_ref}'`);
  }
  pushRefErrors({
    ownerId: skill.id,
    field: "host",
    refs: skill.host_compatibility ?? [],
    validIds: hostIds,
    errors,
  });
  pushRefErrors({
    ownerId: skill.id,
    field: "skill",
    refs: skill.dependencies?.skills ?? [],
    validIds: skillIds,
    errors,
  });
  pushRefErrors({
    ownerId: skill.id,
    field: "server",
    refs: skill.dependencies?.servers ?? [],
    validIds: serverIds,
    errors,
  });
  pushRefErrors({
    ownerId: skill.id,
    field: "tool",
    refs: skill.dependencies?.tools ?? [],
    validIds: toolIds,
    errors,
  });
  for (const hook of skill.install_hooks ?? []) {
    if (!hostIds.has(hook.host_id)) {
      errors.push(`${skill.id}: install hook references unknown host '${hook.host_id}'`);
    }
  }
}

for (const skillPackage of skillPackages) {
  if (!skillIds.has(skillPackage.skill_ref)) {
    errors.push(`${skillPackage.id}: package references unknown skill '${skillPackage.skill_ref}'`);
    continue;
  }
  if (skillPackage.id !== skillPackage.skill_ref) {
    errors.push(`${skillPackage.id}: package id must match skill_ref`);
  }
  const skill = skills.find((item) => item.id === skillPackage.skill_ref);
  if (!skill) {
    continue;
  }
  if (skill.version !== skillPackage.version) {
    errors.push(`${skill.id}: package version does not match skill registry`);
  }
  if (skill.name !== skillPackage.metadata.name) {
    errors.push(`${skill.id}: package metadata.name does not match skill registry`);
  }
  if (skill.description !== skillPackage.metadata.description) {
    errors.push(`${skill.id}: package description does not match skill registry`);
  }
  if (skill.owner !== skillPackage.metadata.owner) {
    errors.push(`${skill.id}: package owner does not match skill registry`);
  }
  if (skill.risk_tier !== skillPackage.metadata.risk_tier) {
    errors.push(`${skill.id}: package risk_tier does not match skill registry`);
  }
  if (JSON.stringify(skill.knowledge_basis) !== JSON.stringify(skillPackage.metadata.knowledge_basis)) {
    errors.push(`${skill.id}: package knowledge_basis does not match skill registry`);
  }
  if (JSON.stringify(skill.dependencies) !== JSON.stringify(skillPackage.dependencies)) {
    errors.push(`${skill.id}: package dependencies do not match skill registry`);
  }
  if (JSON.stringify(skill.host_compatibility) !== JSON.stringify(skillPackage.host_compatibility)) {
    errors.push(`${skill.id}: package host_compatibility does not match skill registry`);
  }
  if (JSON.stringify(skill.install_hooks) !== JSON.stringify(skillPackage.install_hooks)) {
    errors.push(`${skill.id}: package install_hooks do not match skill registry`);
  }
  if (JSON.stringify(skill.examples) !== JSON.stringify(skillPackage.examples)) {
    errors.push(`${skill.id}: package examples do not match skill registry`);
  }
  if (!Array.isArray(skillPackage.runtime_exports) || skillPackage.runtime_exports.length === 0) {
    errors.push(`${skill.id}: package runtime_exports must contain at least one path`);
  }
  if (!Array.isArray(skillPackage.source_paths) || skillPackage.source_paths.length === 0) {
    errors.push(`${skill.id}: package source_paths must contain at least one path`);
  }
  for (const sourcePath of skillPackage.source_paths ?? []) {
    if (!exists(sourcePath)) {
      errors.push(`${skill.id}: package source path missing '${sourcePath}'`);
    }
  }
  if (
    skill.version_lock?.schema_version !== skillPackage.version_lock?.schema_version ||
    skill.version_lock?.artifact_hash !== skillPackage.version_lock?.artifact_hash
  ) {
    errors.push(`${skill.id}: package version_lock does not match skill registry`);
  }
}

for (const workflow of workflows) {
  if (workflow.contract_ref !== workflow.id) {
    errors.push(`${workflow.id}: contract_ref must match workflow id`);
  }
  if (!workflowContractIds.has(workflow.contract_ref)) {
    errors.push(`${workflow.id}: missing workflow contract '${workflow.contract_ref}'`);
  }
  for (const step of workflow.steps ?? []) {
    pushRefErrors({
      ownerId: `${workflow.id}/${step.id}`,
      field: "skill",
      refs: step.required_skills ?? [],
      validIds: skillIds,
      errors,
    });
    pushRefErrors({
      ownerId: `${workflow.id}/${step.id}`,
      field: "tool",
      refs: step.required_tools ?? [],
      validIds: toolIds,
      errors,
    });
    pushRefErrors({
      ownerId: `${workflow.id}/${step.id}`,
      field: "server",
      refs: step.required_servers ?? [],
      validIds: serverIds,
      errors,
    });
  }
  if (["high", "critical"].includes(workflow.risk_tier)) {
    const hasAuditStep = (workflow.steps ?? []).some(
      (step) => step.stage === "888" && step.role === "auditor",
    );
    if (!hasAuditStep) {
      errors.push(`${workflow.id}: high-risk workflow must contain an 888 auditor step`);
    }
    if (workflow.requires_arifos_judgment !== true) {
      errors.push(`${workflow.id}: high-risk workflow must require arifOS judgment`);
    }
    if (workflow.requires_vault_seal !== true) {
      errors.push(`${workflow.id}: high-risk workflow must require vault seal`);
    }
    if (workflow.separation_of_duties?.proposer_must_differ_from_approver !== true) {
      errors.push(
        `${workflow.id}: high-risk workflow must enforce proposer_must_differ_from_approver`,
      );
    }
  }
}

for (const workflowContract of workflowContracts) {
  if (!workflowIds.has(workflowContract.workflow_ref)) {
    errors.push(
      `${workflowContract.id}: contract references unknown workflow '${workflowContract.workflow_ref}'`,
    );
    continue;
  }
  if (workflowContract.id !== workflowContract.workflow_ref) {
    errors.push(`${workflowContract.id}: contract id must match workflow_ref`);
  }
  const workflow = workflows.find((item) => item.id === workflowContract.workflow_ref);
  if (!workflow) {
    continue;
  }
  if (workflow.name && !workflowContract.preconditions) {
    errors.push(`${workflow.id}: contract preconditions are required`);
  }
  if (workflow.risk_tier !== workflowContract.risk_tier) {
    errors.push(`${workflow.id}: contract risk_tier does not match workflow registry`);
  }
  if (JSON.stringify(workflow.knowledge_basis) !== JSON.stringify(workflowContract.knowledge_basis)) {
    errors.push(`${workflow.id}: contract knowledge_basis does not match workflow registry`);
  }
  if (
    JSON.stringify(workflow.required_witnesses) !==
    JSON.stringify(workflowContract.required_witnesses)
  ) {
    errors.push(`${workflow.id}: contract required_witnesses do not match workflow registry`);
  }
  if (workflow.requires_arifos_judgment !== workflowContract.requires_arifos_judgment) {
    errors.push(`${workflow.id}: contract requires_arifos_judgment does not match registry`);
  }
  if (workflow.requires_vault_seal !== workflowContract.requires_vault_seal) {
    errors.push(`${workflow.id}: contract requires_vault_seal does not match registry`);
  }
  if (
    JSON.stringify(workflow.separation_of_duties) !==
    JSON.stringify(workflowContract.separation_of_duties)
  ) {
    errors.push(`${workflow.id}: contract separation_of_duties does not match registry`);
  }
  if ((workflow.steps ?? []).length !== (workflowContract.step_contracts ?? []).length) {
    errors.push(`${workflow.id}: contract step count does not match workflow registry`);
    continue;
  }
  const contractStepsById = new Map(workflowContract.step_contracts.map((step) => [step.id, step]));
  for (const step of workflow.steps ?? []) {
    const contractStep = contractStepsById.get(step.id);
    if (!contractStep) {
      errors.push(`${workflow.id}: missing contract step '${step.id}'`);
      continue;
    }
    const fieldsToCompare = [
      "title",
      "stage",
      "role",
      "required_skills",
      "required_tools",
      "required_servers",
      "holds",
      "inputs",
      "outputs",
      "on_error",
      "retry_policy",
    ];
    for (const field of fieldsToCompare) {
      if (JSON.stringify(step[field]) !== JSON.stringify(contractStep[field])) {
        errors.push(`${workflow.id}/${step.id}: contract ${field} does not match registry step`);
      }
    }
  }
  for (const contractStep of workflowContract.step_contracts ?? []) {
    for (const hook of contractStep.approval_hooks ?? []) {
      if (!hook.trigger) {
        errors.push(`${workflow.id}/${contractStep.id}: approval hook trigger is required`);
      }
    }
  }
  if (
    !workflowContract.rollback_strategy ||
    !Array.isArray(workflowContract.rollback_strategy.compensating_actions)
  ) {
    errors.push(`${workflow.id}: rollback_strategy must define compensating_actions`);
  }
  if (!Array.isArray(workflowContract.emitted_events) || workflowContract.emitted_events.length === 0) {
    errors.push(`${workflow.id}: emitted_events must contain at least one event`);
  }
}

for (const bundle of bundles) {
  pushRefErrors({
    ownerId: bundle.id,
    field: "skill",
    refs: bundle.skills ?? [],
    validIds: skillIds,
    errors,
  });
  pushRefErrors({
    ownerId: bundle.id,
    field: "workflow",
    refs: bundle.workflows ?? [],
    validIds: workflowIds,
    errors,
  });
  pushRefErrors({
    ownerId: bundle.id,
    field: "host",
    refs: bundle.hosts ?? [],
    validIds: hostIds,
    errors,
  });
}

for (const integration of integrations) {
  if (!domainIds.has(integration.domain_plane)) {
    errors.push(`${integration.id}: unknown domain_plane '${integration.domain_plane}'`);
  }
  if (!exists(integration.contract_path)) {
    errors.push(`${integration.id}: missing contract file '${integration.contract_path}'`);
  }
}

if (!exists("contracts/init/000-init.yaml")) {
  errors.push("missing init contract 'contracts/init/000-init.yaml'");
}

if (initContract.id !== "aaa-init-000") {
  errors.push("contracts/init/000-init.yaml: id must be 'aaa-init-000'");
}

if ((initBootSequence[0]?.path ?? "") !== "ROOT_CANON.yaml") {
  errors.push("contracts/init/000-init.yaml: boot sequence must begin with ROOT_CANON.yaml");
}

for (const rootPath of requiredRootCanons) {
  if (!exists(rootPath)) {
    errors.push(`init contract references missing root canon '${rootPath}'`);
  }
}

if (!requiredRootCanons.has("agent-card.json")) {
  errors.push("contracts/init/000-init.yaml: required_root_canons must include agent-card.json");
}

if (!Array.isArray(initContract.invariants) || initContract.invariants.length === 0) {
  errors.push("contracts/init/000-init.yaml: invariants must contain at least one item");
}

const requiredNamedHosts = new Set([
  "claude-code",
  "cursor",
  "codex",
  "copilot-cli",
  "gemini-cli",
  "opencode",
]);

for (const hostId of requiredNamedHosts) {
  if (!hostIds.has(hostId)) {
    errors.push(`hosts registry missing required host '${hostId}'`);
  }
  if (!hostContractIds.has(hostId)) {
    errors.push(`host contracts missing required host '${hostId}'`);
  }
}

for (const contract of hostContracts) {
  if (!hostIds.has(contract.id)) {
    errors.push(`${contract.id}: host contract has no registry entry`);
  }
}

for (const host of hosts) {
  if (host.contract_path !== "contracts/hosts/contracts.yaml") {
    errors.push(`${host.id}: contract_path must be 'contracts/hosts/contracts.yaml'`);
  }
  if (!exists(host.contract_path)) {
    errors.push(`${host.id}: missing contract file '${host.contract_path}'`);
    continue;
  }
  const contract = hostContracts.find((item) => item.id === host.id);
  if (!contract) {
    errors.push(`${host.id}: missing matching host contract`);
    continue;
  }
  if (contract.name !== host.name) {
    errors.push(`${host.id}: host name does not match contract`);
  }
  if (contract.runtime_type !== host.runtime_type) {
    errors.push(`${host.id}: runtime_type does not match contract`);
  }
  if (contract.transport !== host.transport) {
    errors.push(`${host.id}: transport does not match contract`);
  }
  if (JSON.stringify(contract.config_paths) !== JSON.stringify(host.config_paths)) {
    errors.push(`${host.id}: config_paths do not match contract`);
  }
  if (contract.install_method !== host.install_method) {
    errors.push(`${host.id}: install_method does not match contract`);
  }
  if (JSON.stringify(contract.supported_protocols) !== JSON.stringify(host.supported_protocols)) {
    errors.push(`${host.id}: supported_protocols do not match contract`);
  }
  if (
    JSON.stringify(
      contract.permission_profiles.map(({ id, default: isDefault, approval_policy }) => ({
        id,
        default: isDefault,
        approval_policy,
      })),
    ) !== JSON.stringify(host.permission_profiles)
  ) {
    errors.push(`${host.id}: permission_profiles do not match contract`);
  }
}

for (const item of a2aRegistryAgents) {
  if (!item.card_path?.startsWith("external://") && !exists(item.card_path)) {
    errors.push(`${item.agent_id}: missing local A2A card '${item.card_path}'`);
  }
  if (!agentIds.has(item.agent_id)) {
    errors.push(`${item.agent_id}: A2A registry references unknown agent`);
  }
}

for (const binding of bridgeBindings) {
  if (!a2aAgentIds.has(binding.agent_id)) {
    errors.push(`${binding.agent_id}: bridge binding references unknown A2A agent`);
  }
}

if (bridge.runtime_policy?.remote_execution_enabled !== false) {
  errors.push("openclaw/a2a/bridge.yaml: remote_execution_enabled must remain false");
}

if (federationContract.id !== "aaa-sense-111") {
  errors.push("contracts/federation/111-sense.yaml: id must be aaa-sense-111");
}

if (federationContract.stage !== "111") {
  errors.push("contracts/federation/111-sense.yaml: stage must be 111");
}

if (federationContract.deployment?.runtime_bridge_ref !== "openclaw/a2a/bridge.yaml") {
  errors.push(
    "contracts/federation/111-sense.yaml: deployment.runtime_bridge_ref must be openclaw/a2a/bridge.yaml",
  );
}

for (const surface of federationPublicSurfaces) {
  if (!exists(surface.path)) {
    errors.push(`${surface.id}: missing public surface '${surface.path}'`);
    continue;
  }
  if (surface.source_path) {
    if (!exists(surface.source_path)) {
      errors.push(`${surface.id}: missing surface source '${surface.source_path}'`);
      continue;
    }
    const published = loadJson(surface.path);
    if (JSON.stringify(published) !== JSON.stringify(sourceAgentCard)) {
      errors.push(`${surface.id}: published surface does not match aaa gateway source card`);
    }
  }
}

if (federationContract.deployment?.hosting_model === "static-site") {
  for (const surface of federationIngressSurfaces) {
    if (surface.status === "live") {
      errors.push(`${surface.id}: static-site deployment cannot claim live ingress`);
    }
  }
}

for (const tier of federationTrustTiers) {
  const peerClass = authPeerClasses.get(tier.id);
  if (!peerClass) {
    errors.push(`${tier.id}: trust tier missing in a2a/policies/auth.yaml`);
    continue;
  }
  if (JSON.stringify(tier.auth_schemes) !== JSON.stringify(peerClass.allowed_schemes ?? [])) {
    errors.push(`${tier.id}: auth_schemes do not match a2a/policies/auth.yaml`);
  }
  if (tier.require_mtls !== Boolean(peerClass.require_mtls)) {
    errors.push(`${tier.id}: require_mtls does not match a2a/policies/auth.yaml`);
  }
}

for (const surface of federationIngressSurfaces) {
  if (!exists(surface.auth_policy_ref)) {
    errors.push(`${surface.id}: missing auth_policy_ref '${surface.auth_policy_ref}'`);
  }
  if (!exists(surface.allowed_peers_ref)) {
    errors.push(`${surface.id}: missing allowed_peers_ref '${surface.allowed_peers_ref}'`);
  }
  if (!exists(surface.skills_exposure_ref)) {
    errors.push(`${surface.id}: missing skills_exposure_ref '${surface.skills_exposure_ref}'`);
  }
  if (!exists(surface.registry_ref)) {
    errors.push(`${surface.id}: missing registry_ref '${surface.registry_ref}'`);
  }
  if (!exists(surface.runtime_bridge_ref)) {
    errors.push(`${surface.id}: missing runtime_bridge_ref '${surface.runtime_bridge_ref}'`);
  }
  if (surface.path !== "/a2a/message") {
    errors.push(`${surface.id}: ingress path must remain /a2a/message`);
  }
}

if (goalChainContract.id !== "aaa-goal-chain-222") {
  errors.push("contracts/goals/222-goals.yaml: id must be aaa-goal-chain-222");
}

if (goalChainContract.stage !== "222") {
  errors.push("contracts/goals/222-goals.yaml: stage must be 222");
}

if (orgTopologyContract.id !== "aaa-org-topology-333") {
  errors.push("contracts/org/333-org-units.yaml: id must be aaa-org-topology-333");
}

if (orgTopologyContract.stage !== "333") {
  errors.push("contracts/org/333-org-units.yaml: stage must be 333");
}

for (const unit of orgUnits) {
  if (unit.parent_org_unit && !orgUnitIds.has(unit.parent_org_unit)) {
    errors.push(`${unit.id}: unknown parent_org_unit '${unit.parent_org_unit}'`);
  }
  if (unit.parent_org_unit === unit.id) {
    errors.push(`${unit.id}: parent_org_unit cannot reference itself`);
  }
  if (!federationTrustTierIds.has(unit.trust_tier)) {
    errors.push(`${unit.id}: unknown trust_tier '${unit.trust_tier}'`);
  }
  pushRefErrors({
    ownerId: unit.id,
    field: "member",
    refs: unit.members ?? [],
    validIds: agentIds,
    errors,
  });
  pushRefErrors({
    ownerId: unit.id,
    field: "workflow",
    refs: unit.workflow_scope ?? [],
    validIds: workflowIds,
    errors,
  });
  pushRefErrors({
    ownerId: unit.id,
    field: "domain",
    refs: unit.owned_domain_planes ?? [],
    validIds: domainIds,
    errors,
  });
  if (unit.lead_agent) {
    if (!agentIds.has(unit.lead_agent)) {
      errors.push(`${unit.id}: unknown lead_agent '${unit.lead_agent}'`);
    } else if (!(unit.members ?? []).includes(unit.lead_agent)) {
      errors.push(`${unit.id}: lead_agent must be included in members`);
    }
  }
}

for (const edge of topologyEdges) {
  if (!orgUnitIds.has(edge.from_org_unit)) {
    errors.push(`${edge.id}: unknown from_org_unit '${edge.from_org_unit}'`);
  }
  if (!orgUnitIds.has(edge.to_org_unit)) {
    errors.push(`${edge.id}: unknown to_org_unit '${edge.to_org_unit}'`);
  }
  if (!federationTrustTierIds.has(edge.trust_tier)) {
    errors.push(`${edge.id}: unknown trust_tier '${edge.trust_tier}'`);
  }
  pushRefErrors({
    ownerId: edge.id,
    field: "workflow",
    refs: edge.workflow_refs ?? [],
    validIds: workflowIds,
    errors,
  });
}

for (const goal of goals) {
  if (!orgUnitIds.has(goal.owner_org_unit)) {
    errors.push(`${goal.id}: unknown owner_org_unit '${goal.owner_org_unit}'`);
  }
  if (!agentIds.has(goal.sponsor_agent)) {
    errors.push(`${goal.id}: unknown sponsor_agent '${goal.sponsor_agent}'`);
  }
}

for (const task of goalTasks) {
  if (!goalIds.has(task.goal_ref)) {
    errors.push(`${task.id}: unknown goal_ref '${task.goal_ref}'`);
  }
  if (!orgUnitIds.has(task.assigned_org_unit)) {
    errors.push(`${task.id}: unknown assigned_org_unit '${task.assigned_org_unit}'`);
  }
  if (!agentIds.has(task.assigned_agent)) {
    errors.push(`${task.id}: unknown assigned_agent '${task.assigned_agent}'`);
  }
  pushRefErrors({
    ownerId: task.id,
    field: "task dependency",
    refs: task.depends_on ?? [],
    validIds: goalTaskIds,
    errors,
  });
  pushRefErrors({
    ownerId: task.id,
    field: "tool",
    refs: task.required_tools ?? [],
    validIds: toolIds,
    errors,
  });
  pushRefErrors({
    ownerId: task.id,
    field: "server",
    refs: task.required_servers ?? [],
    validIds: serverIds,
    errors,
  });
  const assignedUnit = orgUnits.find((item) => item.id === task.assigned_org_unit);
  if (assignedUnit && !(assignedUnit.members ?? []).includes(task.assigned_agent)) {
    errors.push(`${task.id}: assigned_agent must belong to assigned_org_unit`);
  }
}

for (const verdict of goalVerdicts) {
  if (!goalIds.has(verdict.goal_ref)) {
    errors.push(`${verdict.id}: unknown goal_ref '${verdict.goal_ref}'`);
  }
  if (!goalTaskIds.has(verdict.task_ref)) {
    errors.push(`${verdict.id}: unknown task_ref '${verdict.task_ref}'`);
  } else {
    const verdictTask = goalTasks.find((item) => item.id === verdict.task_ref);
    if (verdictTask?.goal_ref !== verdict.goal_ref) {
      errors.push(`${verdict.id}: task_ref must belong to goal_ref`);
    }
  }
  pushRefErrors({
    ownerId: verdict.id,
    field: "signer",
    refs: verdict.signers ?? [],
    validIds: agentIds,
    errors,
  });
}

if (governanceContract.id !== "aaa-governance-gates-666-777") {
  errors.push("contracts/governance/666-777-gates.yaml: id must be aaa-governance-gates-666-777");
}

if (governanceContract.stage_band !== "666-777") {
  errors.push("contracts/governance/666-777-gates.yaml: stage_band must be 666-777");
}

for (const budget of budgets) {
  if (budget.warning_threshold >= budget.hard_stop_threshold) {
    errors.push(`${budget.id}: warning_threshold must be lower than hard_stop_threshold`);
  }
  if (budget.scope_type === "org-unit" && !orgUnitIds.has(budget.scope_ref)) {
    errors.push(`${budget.id}: org-unit budget scope_ref must reference a known org unit`);
  }
  if (budget.scope_type === "agent" && !agentIds.has(budget.scope_ref)) {
    errors.push(`${budget.id}: agent budget scope_ref must reference a known agent`);
  }
  pushRefErrors({
    ownerId: budget.id,
    field: "budget agent",
    refs: budget.applies_to_agents ?? [],
    validIds: agentIds,
    errors,
  });
}

for (const gate of governanceGates) {
  if (!goalIds.has(gate.goal_ref)) {
    errors.push(`${gate.id}: unknown goal_ref '${gate.goal_ref}'`);
  }
  if (!orgUnitIds.has(gate.owner_org_unit)) {
    errors.push(`${gate.id}: unknown owner_org_unit '${gate.owner_org_unit}'`);
  }
  if (!workflowIds.has(gate.workflow_ref)) {
    errors.push(`${gate.id}: unknown workflow_ref '${gate.workflow_ref}'`);
  }
  if (!budgetIds.has(gate.budget_policy_ref)) {
    errors.push(`${gate.id}: unknown budget_policy_ref '${gate.budget_policy_ref}'`);
  }
  for (const evidenceRef of gate.evidence_inputs ?? []) {
    if (!exists(evidenceRef)) {
      errors.push(`${gate.id}: missing evidence input '${evidenceRef}'`);
    }
  }
}

if (decisionsContract.id !== "aaa-decisions-888-999") {
  errors.push("contracts/decisions/888-999-decisions.yaml: id must be aaa-decisions-888-999");
}

if (decisionsContract.stage_band !== "888-999") {
  errors.push("contracts/decisions/888-999-decisions.yaml: stage_band must be 888-999");
}

for (const decision of decisions) {
  if (!goalIds.has(decision.goal_ref)) {
    errors.push(`${decision.id}: unknown goal_ref '${decision.goal_ref}'`);
  }
  if (!governanceGateIds.has(decision.gate_ref)) {
    errors.push(`${decision.id}: unknown gate_ref '${decision.gate_ref}'`);
  }
  if (!orgUnitIds.has(decision.executor_org_unit)) {
    errors.push(`${decision.id}: unknown executor_org_unit '${decision.executor_org_unit}'`);
  }
  if (!vaultExportIds.has(decision.vault_export_ref)) {
    errors.push(`${decision.id}: unknown vault_export_ref '${decision.vault_export_ref}'`);
  }
  for (const evidenceRef of decision.evidence_refs ?? []) {
    if (!exists(evidenceRef)) {
      errors.push(`${decision.id}: missing evidence ref '${evidenceRef}'`);
    }
  }
  pushRefErrors({
    ownerId: decision.id,
    field: "actual signer",
    refs: decision.actual_signers ?? [],
    validIds: agentIds,
    errors,
  });
  for (const signerId of decision.actual_signers ?? []) {
    const signer = agents.find((item) => item.id === signerId);
    if (signer && !decision.required_signer_roles.includes(signer.role)) {
      errors.push(`${decision.id}: actual signer '${signerId}' does not satisfy required_signer_roles`);
    }
  }
  if (["approved", "sealed"].includes(decision.status) && (decision.actual_signers ?? []).length === 0) {
    errors.push(`${decision.id}: approved or sealed decisions must record actual_signers`);
  }
}

for (const vaultExport of vaultExports) {
  if (!decisionIds.has(vaultExport.decision_ref)) {
    errors.push(`${vaultExport.id}: unknown decision_ref '${vaultExport.decision_ref}'`);
  }
  if (!exists(vaultExport.path)) {
    errors.push(`${vaultExport.id}: missing vault export path '${vaultExport.path}'`);
  }
}

if (errors.length > 0) {
  console.error("AAA validation failed:");
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}

const summary = {
  agents: agents.length,
  bundles: bundleIds.size,
  budgets: budgetIds.size,
  decisions: decisionIds.size,
  domains: domainIds.size,
  goals: goalIds.size,
  governanceGates: governanceGateIds.size,
  hosts: hostIds.size,
  integrations: integrationIds.size,
  orgUnits: orgUnitIds.size,
  servers: serverIds.size,
  skills: skillIds.size,
  tools: toolIds.size,
  workflows: workflowIds.size,
  a2aAgents: a2aAgentIds.size,
  federationPublicSurfaces: federationPublicSurfaces.length,
};

console.log("AAA validation passed.");
console.log(JSON.stringify(summary, null, 2));
