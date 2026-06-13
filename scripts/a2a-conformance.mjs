import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, '..');

process.env.NODE_ENV = 'test';

const { createApp } = await import('../src/gateway/server.ts');

const artifactDir = path.join(repoRoot, 'dist', 'aaa');
const artifactPath = path.join(artifactDir, 'a2a-conformance.json');
const artifactMarkdownPath = path.join(artifactDir, 'a2a-conformance.md');

const failures = [];
const passes = [];

function recordPass(name, detail) {
  passes.push({ name, detail });
}

function recordFailure(name, detail) {
  failures.push({ name, detail });
}

function expect(condition, name, detail) {
  if (condition) {
    recordPass(name, detail);
    return;
  }
  recordFailure(name, detail);
}

async function loadJson(relativePath) {
  const fullPath = path.join(repoRoot, relativePath);
  return JSON.parse(await readFile(fullPath, 'utf8'));
}

async function loadText(relativePath) {
  return readFile(path.join(repoRoot, relativePath), 'utf8');
}

async function checkGatewayDiscovery() {
  const app = createApp();
  const server = await new Promise((resolve) => {
    const instance = app.listen(0, '127.0.0.1', () => resolve(instance));
  });

  const { port } = server.address();
  const baseUrl = `http://127.0.0.1:${port}`;
  const seedCard = await loadJson('src/seed/agent-card.json');
  const seedPolicy = await loadJson('src/seed/discovery-routing-policy.json');

  try {
    for (const discoveryPath of [
      '/.well-known/a2a-discovery.json',
      '/.well-known/agent-card.json',
      '/.well-known/agent.json',
      '/agent-card.json',
      '/agent.json',
      '/a2a/agent-card.json',
      '/a2a/agent.json',
    ]) {
      const response = await fetch(`${baseUrl}${discoveryPath}`);
      expect(response.ok, `gateway ${discoveryPath}`, `expected 200 from ${discoveryPath}`);
      if (!response.ok) {
        continue;
      }
      const payload = await response.json();
      if (discoveryPath === '/.well-known/a2a-discovery.json') {
        expect(
          payload.canonical_agent_card === '/.well-known/agent-card.json',
          'gateway canonical discovery contract',
          'canonical discovery contract must point to /.well-known/agent-card.json'
        );
        continue;
      }
      expect(
        JSON.stringify(payload) === JSON.stringify(seedCard),
        `gateway payload ${discoveryPath}`,
        `${discoveryPath} must match src/seed/agent-card.json`
      );
    }

    for (const policyPath of ['/.well-known/a2a-routing-policy.json', '/a2a/routing-policy.json']) {
      const response = await fetch(`${baseUrl}${policyPath}`);
      expect(response.ok, `gateway ${policyPath}`, `expected 200 from ${policyPath}`);
      if (!response.ok) {
        continue;
      }
      const payload = await response.json();
      expect(
        JSON.stringify(payload) === JSON.stringify(seedPolicy),
        `gateway payload ${policyPath}`,
        `${policyPath} must match src/seed/discovery-routing-policy.json`
      );
    }
  } finally {
    await new Promise((resolve, reject) => {
      server.close((error) => (error ? reject(error) : resolve()));
    });
  }
}

async function checkStaticArtifacts() {
  const seedCard = JSON.stringify(await loadJson('src/seed/agent-card.json'));
  const publicCard = JSON.stringify(await loadJson('public/a2a/agent-card.json'));
  const legacyCard = JSON.stringify(await loadJson('public/a2a/agent.json'));
  const statusJson = await loadJson('public/a2a/status.json');

  expect(publicCard === seedCard, 'public agent card parity', 'public/a2a/agent-card.json must match src/seed/agent-card.json');
  expect(legacyCard === seedCard, 'legacy agent alias parity', 'public/a2a/agent.json must mirror the canonical card');
  expect(
    statusJson.public_surfaces?.canonical_discovery_contract === '/.well-known/a2a-discovery.json',
    'status canonical discovery contract',
    'public/a2a/status.json must declare the canonical discovery contract surface'
  );
  expect(
    statusJson.public_surfaces?.canonical_discovery_surface === '/.well-known/agent-card.json',
    'status canonical discovery',
    'public/a2a/status.json must declare the canonical discovery surface'
  );
  expect(
    statusJson.public_surfaces?.routing_policy === '/.well-known/a2a-routing-policy.json',
    'status routing policy',
    'public/a2a/status.json must publish the routing policy surface'
  );
}

async function checkSourceContracts() {
  const authSource = await loadText('src/gateway/auth.ts');
  const gatewaySource = await loadText('src/gateway/server.ts');
  const a2aServerSource = await loadText('a2a-server/server.js');
  const dashboardSource = await loadText('../arifOS/static/dashboard/index.html');

  for (const publicPath of [
    '/.well-known/a2a-discovery.json',
    '/.well-known/agent-card.json',
    '/.well-known/agent.json',
    '/.well-known/a2a-routing-policy.json',
    '/a2a/discovery-contract.json',
    '/a2a/agent-card.json',
    '/a2a/agent.json',
    '/a2a/routing-policy.json',
    '/agent-card.json',
    '/agent.json',
  ]) {
    expect(
      authSource.includes(publicPath),
      `auth public path ${publicPath}`,
      `src/gateway/auth.ts must allow public access to ${publicPath}`
    );
  }

  for (const route of [
    '/.well-known/a2a-discovery.json',
    '/.well-known/agent-card.json',
    '/.well-known/agent.json',
    '/.well-known/a2a-routing-policy.json',
    '/a2a/discovery-contract.json',
    '/a2a/agent-card.json',
    '/a2a/agent.json',
    '/a2a/routing-policy.json',
  ]) {
    expect(
      gatewaySource.includes(route),
      `gateway route ${route}`,
      `src/gateway/server.ts must expose ${route}`
    );
    expect(
      a2aServerSource.includes(route),
      `a2a-server route ${route}`,
      `a2a-server/server.js must expose ${route}`
    );
  }

  for (const taskRoute of [
    "app.post('/tasks'",
    "app.get('/tasks/:taskId'",
    "app.get('/tasks/:taskId/stream'",
    "app.post('/tasks/:taskId/cancel'",
    "app.get('/tasks/:taskId/subscribe'",
  ]) {
    expect(
      a2aServerSource.includes(taskRoute),
      `a2a-server task route ${taskRoute}`,
      `a2a-server/server.js must keep ${taskRoute}`
    );
  }

  expect(
    !dashboardSource.includes('EventSource(`${MCP_BASE_URL}/webmcp`)') &&
      !dashboardSource.includes("EventSource('/webmcp')"),
    'dashboard SSE cleanup',
    'arifos dashboard must not advertise WebMCP SSE-only connectivity'
  );
  expect(
    dashboardSource.includes('/mcp'),
    'dashboard streamable http guidance',
    'arifos dashboard must point agents at the streamable HTTP MCP endpoint'
  );
}

function toMarkdownReport(artifact) {
  const lines = [];
  lines.push('# A2A Conformance Report');
  lines.push('');
  lines.push(`Generated: ${artifact.generated_at}`);
  lines.push(`Verdict: ${artifact.verdict.toUpperCase()}`);
  lines.push('');
  lines.push('## Passed Checks');
  lines.push('');
  if (artifact.checks.passed.length === 0) {
    lines.push('- none');
  } else {
    for (const pass of artifact.checks.passed) {
      lines.push(`- ${pass.name}: ${pass.detail}`);
    }
  }
  lines.push('');
  lines.push('## Failed Checks');
  lines.push('');
  if (artifact.checks.failed.length === 0) {
    lines.push('- none');
  } else {
    for (const failure of artifact.checks.failed) {
      lines.push(`- ${failure.name}: ${failure.detail}`);
    }
  }
  lines.push('');
  return `${lines.join('\n')}\n`;
}

async function main() {
  await mkdir(artifactDir, { recursive: true });

  try {
    await checkGatewayDiscovery();
    await checkStaticArtifacts();
    await checkSourceContracts();
  } catch (error) {
    recordFailure('runtime exception', error instanceof Error ? error.message : String(error));
  }

  const artifact = {
    generated_at: new Date().toISOString(),
    verdict: failures.length === 0 ? 'pass' : 'fail',
    checks: {
      passed: passes,
      failed: failures,
    },
  };

  await writeFile(artifactPath, `${JSON.stringify(artifact, null, 2)}\n`, 'utf8');
  await writeFile(artifactMarkdownPath, toMarkdownReport(artifact), 'utf8');

  if (failures.length > 0) {
    console.error(JSON.stringify(artifact, null, 2));
    process.exitCode = 1;
    return;
  }

  console.log(JSON.stringify(artifact, null, 2));
}

await main();
