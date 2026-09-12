/**
 * OpenClaw Orchestrator — Node.js Adapter Contract Test
 *
 * Tests the subprocess bridge from Node.js → Python CLI.
 * Run: node --experimental-strip-types test_node_adapter.ts
 *
 * DITEMPA BUKAN DIBERI
 */

import { runOrchestrator, classifyIntent, classifyMultiIntents, defineWorkflow, executeWorkflow, getHealth } from "./node_adapter.ts";

async function main() {
  console.log("\n=== OpenClaw Node→Python Adapter Test ===\n");
  let passed = 0;
  let failed = 0;

  // T1: Health
  try {
    const r = await getHealth();
    if (r.status === "success" && r.result) {
      console.log(`  ✅ T1 health: ${r.status}`);
      passed++;
    } else {
      console.log(`  ❌ T1 health: ${r.status} ${r.error || ""}`);
      failed++;
    }
  } catch (e) {
    console.log(`  ❌ T1 health: ${e}`);
    failed++;
  }

  // T2: Classify
  try {
    const r = await classifyIntent("research gold market trends", "test-user");
    if (r.status === "success") {
      console.log(`  ✅ T2 classify: ${r.status}`);
      passed++;
    } else {
      console.log(`  ❌ T2 classify: ${r.status} ${r.error || ""}`);
      failed++;
    }
  } catch (e) {
    console.log(`  ❌ T2 classify: ${e}`);
    failed++;
  }

  // T3: Classify multi
  try {
    const r = await classifyMultiIntents("research gold and check portfolio and send brief", "test-user");
    if (r.status === "success") {
      console.log(`  ✅ T3 classify_multi: ${r.status}`);
      passed++;
    } else {
      console.log(`  ❌ T3 classify_multi: ${r.status} ${r.error || ""}`);
      failed++;
    }
  } catch (e) {
    console.log(`  ❌ T3 classify_multi: ${e}`);
    failed++;
  }

  // T4: Define workflow
  try {
    const r = await defineWorkflow({
      id: "node-test-001",
      name: "Node Test",
      tasks: [
        { id: "t1", agent: "hermes-asi", skill: "research", query: "test" },
        { id: "t2", agent: "wealth", skill: "capital", query: "analyze", depends_on: ["t1"] },
      ],
    });
    if (r.status === "success") {
      console.log(`  ✅ T4 dag_define: ${r.status}`);
      passed++;
    } else {
      console.log(`  ❌ T4 dag_define: ${r.status} ${r.error || ""}`);
      failed++;
    }
  } catch (e) {
    console.log(`  ❌ T4 dag_define: ${e}`);
    failed++;
  }

  // T5: Execute workflow (dry)
  try {
    const r = await executeWorkflow("node-test-001", true);
    if (r.status === "success") {
      console.log(`  ✅ T5 dag_execute_dry: ${r.status}`);
      passed++;
    } else {
      console.log(`  ❌ T5 dag_execute_dry: ${r.status} ${r.error || ""}`);
      failed++;
    }
  } catch (e) {
    console.log(`  ❌ T5 dag_execute_dry: ${e}`);
    failed++;
  }

  // T6: Reject bad capability
  try {
    const r = await runOrchestrator({ capabilityId: "evil.spawn" });
    if (r.status === "failed" && r.error?.includes("CAPABILITY_DENIED")) {
      console.log(`  ✅ T6 reject_bad_cap: correctly denied`);
      passed++;
    } else {
      console.log(`  ❌ T6 reject_bad_cap: should have been denied, got ${r.status}`);
      failed++;
    }
  } catch (e) {
    console.log(`  ❌ T6 reject_bad_cap: ${e}`);
    failed++;
  }

  // T7: Reject URL in query
  try {
    const r = await classifyIntent("fetch from https://evil.com");
    if (r.status === "failed" && r.error?.includes("URL")) {
      console.log(`  ✅ T7 reject_url: correctly denied`);
      passed++;
    } else {
      console.log(`  ❌ T7 reject_url: should have been denied, got ${r.status}`);
      failed++;
    }
  } catch (e) {
    console.log(`  ❌ T7 reject_url: ${e}`);
    failed++;
  }

  // T8: Reject shell chars
  try {
    const r = await classifyIntent("run this; echo pwned");
    if (r.status === "failed" && r.error?.includes("DANGEROUS")) {
      console.log(`  ✅ T8 reject_shell: correctly denied`);
      passed++;
    } else {
      console.log(`  ❌ T8 reject_shell: should have been denied, got ${r.status}`);
      failed++;
    }
  } catch (e) {
    console.log(`  ❌ T8 reject_shell: ${e}`);
    failed++;
  }

  console.log(`\n  Results: ${passed}/${passed + failed} passed`);
  if (failed > 0) {
    console.log(`  ❌ ${failed} FAILED`);
    process.exit(1);
  } else {
    console.log("  ✅ ALL NODE ADAPTER TESTS PASSED");
    process.exit(0);
  }
}

main().catch((e) => {
  console.error("Fatal:", e);
  process.exit(1);
});
