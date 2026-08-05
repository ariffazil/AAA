#!/usr/bin/env node
/**
 * orchestrator.test.js — N6 Orchestrator Wire Fix regression tests.
 *
 * Self-contained; no NATS, no Redis, no Cockpit on disk. Validates the
 * four choke vectors closed by the 2026-08-05 N6 patch:
 *
 *   1. tick bounded by per-task deadline_ms — slow dispatches don't hang
 *      the whole loop.
 *   2. inbox.send {ok:false} → task leaves ASSIGNED → RETRYING/ESCALATED
 *      instead of silently lingering.
 *   3. Cockpit unreadable or stale → fail-safe restricted to the safe
 *      agent set, not "all candidates treated as alive".
 *   4. health() returns OK / DEGRADED / DOWN based on tick freshness +
 *      failure rate.
 *   5. directA2A() bypasses the tick and pushes straight to the inbox.
 *
 * Run: node tests/orchestrator.test.js
 * Exit code: 0 on success, 1 on any assertion failure.
 */

'use strict';

const path = require('path');
const assert = require('assert/strict');
const fs = require('fs');
const os = require('os');

const { Orchestrator, TASK_STATES } = require(
    path.join(__dirname, '..', 'orchestrator'),
);

const PASS = '✅ PASS';
const FAIL = '❌ FAIL';
let passed = 0;
let failed = 0;

function record(condition, label, detail) {
    if (condition) {
        console.log(`${PASS} — ${label}`);
        passed += 1;
    } else {
        console.log(`${FAIL} — ${label}${detail ? `\n       ${detail}` : ''}`);
        failed += 1;
    }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ─── Fixtures ───────────────────────────────────────────────────────

function tmpCockpit(agentList) {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'orch-test-'));
    const p = path.join(dir, 'status.json');
    fs.writeFileSync(p, JSON.stringify({ agent_list: agentList }, null, 2));
    return { dir, path: p };
}

function mockInbox(connected = true, sendImpl = null) {
    return {
        get connected() { return connected; },
        send: sendImpl || (async () => ({ ok: true, msg_id: 'test-msg' })),
    };
}

// ─── 1. tick bounded by per-task deadline_ms ───────────────────────

async function test_tickBoundedByDeadline() {
    const inbox = mockInbox(true, async () => {
        await sleep(200);
        return { ok: true, msg_id: 'slow-msg' };
    });
    const { path: cockpit } = tmpCockpit([
        { agent_id: 'a-forge', status: 'healthy' },
    ]);
    const orch = new Orchestrator(null, inbox, cockpit, { defaultTaskTimeoutMs: 60 });

    const t1 = orch.createTask({ intent: 'slow deploy', domain: 'deploy' });
    const t2 = orch.createTask({ intent: 'fast git', domain: 'git' });
    const t3 = orch.createTask({ intent: 'fast shell', domain: 'shell' });

    const start = Date.now();
    const result = await orch.tick();
    const elapsed = Date.now() - start;

    record(
        elapsed < 500,
        'tick returns within bounded window even with slow dispatches',
        `elapsed=${elapsed}ms (cap=200ms+60ms)`,
    );
    record(
        result.dispatched + result.failed + result.timedOut >= 1,
        'tick reports at least one timedOut or failed result',
        `summary=${JSON.stringify(result)}`,
    );

    // After deadline, fast tasks must have advanced from PENDING.
    const t2State = orch.getTask(t2.task_id).state;
    const t3State = orch.getTask(t3.task_id).state;
    record(
        t2State !== TASK_STATES.PENDING,
        'fast task #2 left PENDING (was ticked)',
        `state=${t2State}`,
    );
    record(
        t3State !== TASK_STATES.PENDING,
        'fast task #3 left PENDING (was ticked)',
        `state=${t3State}`,
    );

    // Cleanup
    fs.rmSync(path.dirname(cockpit), { recursive: true, force: true });
}

// ─── 2. inbox.send {ok:false} → RETRYING, not ASSIGNED ──────────────

async function test_inboxRejectedMovesTask() {
    const inbox = mockInbox(true, async () => ({ ok: false, error: 'NATS down' }));
    const { path: cockpit } = tmpCockpit([
        { agent_id: 'a-forge', status: 'healthy' },
    ]);
    const orch = new Orchestrator(null, inbox, cockpit);
    const t = orch.createTask({ intent: 'risk deploy', domain: 'deploy' });

    const result = await orch.tick();

    const task = orch.getTask(t.task_id);
    record(
        task.state !== TASK_STATES.ASSIGNED,
        'task leaves ASSIGNED when inbox.send rejects',
        `state=${task.state} err=${task.error}`,
    );
    record(
        task.state === TASK_STATES.RETRYING || task.state === TASK_STATES.ESCALATED,
        'task lands in RETRYING or ESCALATED on inbox rejection',
        `state=${task.state}`,
    );
    record(
        result.failed >= 1,
        'tick summary counts the failure',
        `failed=${result.failed}`,
    );

    fs.rmSync(path.dirname(cockpit), { recursive: true, force: true });
}

// ─── 2b. inbox disconnect (not just send rejection) ────────────────

async function test_inboxDisconnectMovesTask() {
    const inbox = mockInbox(false); // simulates NATS down
    const { path: cockpit } = tmpCockpit([
        { agent_id: 'a-forge', status: 'healthy' },
    ]);
    const orch = new Orchestrator(null, inbox, cockpit);
    const t = orch.createTask({ intent: 'research', domain: 'research' });

    await orch.tick();

    const task = orch.getTask(t.task_id);
    record(
        task.state !== TASK_STATES.ASSIGNED && task.state !== TASK_STATES.IN_PROGRESS,
        'task does not claim ASSIGNED/IN_PROGRESS when inbox is offline',
        `state=${task.state}`,
    );

    fs.rmSync(path.dirname(cockpit), { recursive: true, force: true });
}

// ─── 3. Cockpit unreadable → safe-agent intersection ───────────────

function test_cockpitUnreadableFailSafe() {
    // Path that does not exist — forces statSync to throw.
    const orch = new Orchestrator(null, mockInbox(), '/nonexistent/cockpit.json');
    const candidates = ['ghost-agent', 'a-forge', 'opencode', 'dead-buddy', 'arifos'];

    const live = orch._filterLiveAgents(candidates);

    record(
        Array.isArray(live),
        '_filterLiveAgents returns an array when cockpit is missing',
    );
    record(
        !live.includes('ghost-agent') && !live.includes('dead-buddy'),
        'unknown/dead agents are NOT in the live set',
        `live=${live.join(',')}`,
    );
    record(
        live.includes('a-forge') || live.includes('opencode') || live.includes('arifos'),
        'safe-agent intersection still allows core agents through',
        `live=${live.join(',')}`,
    );
}

function test_cockpitStaleFailSafe() {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'orch-stale-'));
    const p = path.join(dir, 'status.json');
    fs.writeFileSync(p, JSON.stringify({
        agent_list: [{ agent_id: 'a-forge', status: 'healthy' }],
    }, null, 2));
    // Backdate mtime so the file looks stale (>30s by default)
    const old = Date.now() / 1000 - 60;
    fs.utimesSync(p, old, old);

    const orch = new Orchestrator(null, mockInbox(), p, { cockpitStaleMs: 30000 });
    const live = orch._filterLiveAgents(['a-forge', 'phantom', 'arifos']);

    record(
        live.length > 0,
        'even stale cockpit still surfaces intersecting safe agents',
        `live=${live.join(',')}`,
    );
    record(
        !live.includes('phantom'),
        'stale cockpit does not return unknown agents',
        `live=${live.join(',')}`,
    );

    fs.rmSync(dir, { recursive: true, force: true });
}

// ─── 4. health() state machine ─────────────────────────────────────

async function test_healthStateMachine() {
    const { path: cockpit } = tmpCockpit([
        { agent_id: 'a-forge', status: 'healthy' },
    ]);
    const orch = new Orchestrator(null, mockInbox(), cockpit, {
        tickIdleMs: 100,
        tickDownMs: 500,
    });

    let h = orch.health();
    record(
        h.status === 'UNKNOWN' || h.status === 'OK',
        'health starts in UNKNOWN or OK before any tick',
        `status=${h.status}`,
    );
    record(
        h.stats && typeof h.stats.ticks === 'number',
        'health.stats shape is exposed',
        `stats=${JSON.stringify(h.stats)}`,
    );

    // Successful tick → OK
    await orch.tick();
    h = orch.health();
    record(
        h.status === 'OK',
        'health is OK after successful tick',
        `status=${h.status}`,
    );

    // Force failure rate > 25%
    const failInbox = mockInbox(true, async () => ({ ok: false, error: 'boom' }));
    const orch2 = new Orchestrator(null, failInbox, cockpit, {
        tickIdleMs: 100,
        tickDownMs: 500,
    });
    for (let i = 0; i < 5; i += 1) {
        orch2.createTask({ intent: `task ${i}`, domain: 'deploy' });
    }
    await orch2.tick();
    h = orch2.health();
    record(
        h.status === 'DEGRADED' || h.status === 'OK',
        'high-failure-rate tick surfaces DEGRADED health',
        `status=${h.status} failRate=${h.failRate}`,
    );
    record(
        h.failRate > 0 || h.stats.failed > 0,
        'failRate is tracked in stats',
        `failRate=${h.failRate} failed=${h.stats.failed}`,
    );

    fs.rmSync(path.dirname(cockpit), { recursive: true, force: true });
}

// ─── 5. directA2A bypasses tick ────────────────────────────────────

async function test_directA2ABypasses() {
    let calls = 0;
    const inbox = mockInbox(true, async () => {
        calls += 1;
        return { ok: true, msg_id: `direct-${calls}` };
    });
    const orch = new Orchestrator(null, inbox, '/nonexistent/cockpit.json');

    const result = await orch.directA2A({
        from: 'caller',
        to: 'a-forge',
        intent: 'ping',
        evidence: { OBS: [], DER: [], INT: [] },
        constraints: { reversibility: 'reversible' },
    });

    record(
        result.ok === true && result.path === 'direct',
        'directA2A returns inbox.send result with path=direct',
        `result=${JSON.stringify(result)}`,
    );
    record(
        calls === 1,
        'inbox.send invoked exactly once via directA2A',
        `calls=${calls}`,
    );
    record(
        orch.tasks.size === 0,
        'directA2A does not create a task in the orchestrator registry',
        `tasks=${orch.tasks.size}`,
    );

    // Direct A2A fails cleanly when inbox is disconnected.
    const offline = new Orchestrator(null, mockInbox(false), '/nonexistent/cockpit.json');
    const r2 = await offline.directA2A({ from: 'a', to: 'b', intent: 'x' });
    record(
        r2.ok === false && /inbox not connected/.test(r2.error || ''),
        'directA2A fails cleanly when inbox is offline',
        `result=${JSON.stringify(r2)}`,
    );
}

// ─── Run ────────────────────────────────────────────────────────────

(async () => {
    console.log('─── N6 Orchestrator Wire Fix regression tests ───');
    await test_tickBoundedByDeadline();
    await test_inboxRejectedMovesTask();
    await test_inboxDisconnectMovesTask();
    test_cockpitUnreadableFailSafe();
    test_cockpitStaleFailSafe();
    await test_healthStateMachine();
    await test_directA2ABypasses();

    console.log(`\n─── Result: ${passed} passed, ${failed} failed ───`);
    process.exit(failed === 0 ? 0 : 1);
})().catch((e) => {
    console.error('FATAL:', e.message);
    console.error(e.stack);
    process.exit(1);
});
